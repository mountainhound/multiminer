import settings
import json
import subprocess
import xmltodict
import requests,subprocess,shlex,time,datetime,statistics,configparser,sys,re,fcntl,os,random
from telnetlib import Telnet
import socket
from queue import Queue
from threading import Thread
import settings

from profit_api import ProfitCoin


class multiminer():
	def __init__(self,app):
		print ("INIT")
		self.maintenance_stats = None
		self.profit_ts = 0
		self.setting_path = 'conf.json'
		self.app = app
		self.ccminer_algos = settings.ccminer_algos
		self.ethash_algos = settings.ethash_algos
		self.ewbf_algos = settings.ewbf_algos
		self.profit_flag = settings.profit_flag
		self.runningProcess = None
		self.profit_api = ProfitCoin()
		self.current_algo = settings.default
		self.output_q = Queue(maxsize = 100)
		self.stop_flag = False
		ret = None
		print ("Testing")
		subprocess.Popen('fuser -k 4068/tcp'.split(),stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=1)
		
		if self.profit_flag:
			ret = self.profit_switch()
		if not self.runningProcess:
			ret = self.set_mining_mode(self.current_algo)
		
		print ("Starting Mining:{}".format(ret))
		

	def profit_switch(self,force_switch = False):
		if self.profit_flag or force_switch:
			if not self.stop_flag: 
				sorted_list = self.profit_api.most_profitable()
				profit_algo = None
				profit_coin = None
				for coin in sorted_list: 
					algo = coin.get('algorithm').lower().replace(" ","").replace("(","").replace(")","")
					coin = coin.get('coin').lower().replace(" ","").replace("(","").replace(")","")

					if algo in self.ccminer_algos or algo in self.ethash_algos or algo in self.ewbf_algos: 
						if not profit_algo and not profit_coin:
							profit_algo = algo
							profit_coin = coin
							if "nicehash" in profit_coin:
								profit_algo = profit_coin

							#Forces a Switch from Current Algo so it will go to the next coin in list
							if self.current_algo == profit_algo and force_switch:
								profit_algo = None
								profit_coin = None
								
				if self.current_algo == profit_algo and sorted_list:
					print ("Already mining most profitable algo")
					return "Already mining most profitable algo"
				elif profit_algo: 
					self.set_mining_mode(profit_algo)
					print ("Profit Switching to Algo: {}".format(profit_algo))
					return "Profit Switching to Algo: {}".format(profit_algo)
				print ("NO ALGO FOUND")
				return ("NO ALGO FOUND")
		print ("Mode is not auto")
		return ("mode is not auto")

	def miner_restart(self):
		ret = 0
		if self.runningProcess:
			ret = self.stop_mining()

		time.sleep(1)

		if ret < 0 or self.runningProcess is None:
			cmd = './mine.sh -{}'.format(self.current_algo)
			
			self.runningProcess=subprocess.Popen(cmd.split(),stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=1)
			
			time.sleep(1)
			t = Thread(target=self.output_reader, args=(self.runningProcess, self.output_q))
			t.start()
			
			print ('restarting miner')
		
		return "Mining Mode Set To {}".format(self.current_algo)

	def output_reader(self,proc, output_q):
		for line in iter(proc.stdout.readline, b''):
			if proc is not None:
				if output_q.full(): 
					output_q.get()
				output_q.put(line.decode('utf-8'))
				print (line.decode('utf-8'))
				if proc.poll() is not None: 
					print ("breaking output reader")
					break
			else:
				print ("proc.poll = {}".format(proc.poll()))
				print ("proc = {}".format(proc))
				print ("breaking output reader")
				break

	def set_mining_mode(self,mining_mode):
		ret = 0
		if mining_mode is not self.current_algo or self.runningProcess is None: 
			if self.runningProcess:
				ret = self.stop_mining()

			time.sleep(1)

			if ret < 0 or self.runningProcess is None:
				cmd = './mine.sh -{}'.format(mining_mode)
				
				self.runningProcess=subprocess.Popen(cmd.split(),stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=1)
				
				time.sleep(1)
				t = Thread(target=self.output_reader, args=(self.runningProcess, self.output_q))
				t.start()
				
				print ('setting mining mode')
				
				self.current_algo = mining_mode
			
			return "Mining Mode Set To {}".format(self.current_algo)

		return "Algo already running"

	def stop_mining(self):

		if self.runningProcess: 
			self.runningProcess.terminate()
			time.sleep(1)
			self.runningProcess.kill()
			ret = self.runningProcess.poll()	
			subprocess.Popen('fuser -k 4068/tcp'.split(),stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=1)
			time.sleep(2)
			self.runningProcess = None

			return ret
		return "No Algo Running"

	def nvidia_temp_output(self):
		try: 
			sp = subprocess.run(['nvidia-smi', '-q','-x','-f','temp.xml'],timeout = 25)

			with open('temp.xml') as fd:
				doc = xmltodict.parse(fd.read())

			doc = dict(doc)
			gpu_list = doc.get('nvidia_smi_log').get('gpu')
			temp_list = []

			if isinstance(gpu_list, dict): 
				temp_dict = gpu_list.get('temperature')
				temp_list.append(temp_dict.get('gpu_temp'))
				
			elif isinstance(gpu_list,list):
				for gpu in gpu_list:
					temp_dict = gpu.get('temperature')
					temp_list.append(temp_dict.get('gpu_temp'))

			sp = subprocess.run(['rm','temp.xml'])

			return temp_list
			
		except Exception as err: 
			print (err)
			return None

		except subprocess.TimeoutExpired:
			print ("NVIDIA TEMP TIMED OUT")
			return None

	def ccminer_api_output(self,url = "localhost",port = "4068", command = b"summary"):
		try: 
			tn = Telnet(url,port)
			tn.write(command)
			output = tn.read_all().decode("utf-8")
			tn.write(b"^]")
			tn.close()

			print (output)
			return output
		except:
			print ("ERROR IN TELNET")
			return False

	def ewbf_api_output(self,url = "localhost",port = "4068", command = "getstat"):
		try: 
			data = None
			ret = requests.get("http://{}:{}/{}".format(url,port,command))
			if ret.status_code == 200: 
				output = ret.json()	
			print (output)
			return output
		except:
			print ("ERROR IN EWBF HTTP POST")
			return False

	def ethash_api_output(self,url = "localhost",port = 4068, command = "miner_getstat1"):
		try:
			print ("ETHASH API OUTPUT")
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.settimeout(5)
			s.connect((url, int(port)))
			message = json.dumps({"id":0,"jsonrpc":"2.0","method":command}) + "\n"
			s.sendall(message.encode('utf-8'))
			resp = ''
			while 1:
				data = s.recv(4096)
				resp += data.decode('utf-8')
				if not data or (len(data) < 4096 and data[-3:] == b']}\n'):
					break
			s.close()
			print (resp)

			ret = json.loads(resp).get('result')
			return ret
		except Exception as err:
			print ("ERROR IN JSON RPC:{}".format(err))
			return False
			

	def get_miner_output(self,n=10):	
		ret = {}
		miner_output = []
		if self.runningProcess:
			for i in range(n):
				if self.output_q.empty():
					break
				
				line = str(self.output_q.get())
				#Remove trailing newlines and ansi_escape characters
				ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
				line = ansi_escape.sub('', line).rstrip()
				miner_output.append(line)
			
			ret['miner_output'] = miner_output
			ret['current_algo'] = self.current_algo

			return ret
		return None

	def get_miner_stats(self):
		stat_dict = {}
		if self.current_algo in self.ccminer_algos:
			threads_output = self.ccminer_api_output(command = b"threads",url = "localhost")
			if threads_output:
				threads_dict = {}
				threads_list = threads_output.split("|")
				del threads_list[-1]
				for x,gpu_output in enumerate(threads_list): 
					gpu_list = gpu_output.split(";")
					for i,stat in enumerate(gpu_list): 
						gpu_list[i] = stat.split("=")
					threads_dict[x] = dict(gpu_list)

				temp_dict = {}
				gpu_hash_dict = {}
				for key,value in threads_dict.items():
					temp_dict[key] = value.get('TEMP')
					gpu_hash_dict[key] = value.get('KHS')

				stat_dict['temps'] = temp_dict
				stat_dict['gpus'] = gpu_hash_dict

			summary_output = self.ccminer_api_output(command = b"summary",url = "localhost")
			if summary_output:	
				summary_list = summary_output.replace("|","").split(";")

				for i,stat in enumerate(summary_list):
					summary_list[i] = stat.split("=")

				summary_dict = dict(summary_list)

				version = summary_dict.get('VER')
				stat_dict['current_miner'] = 'ccminer_{}'.format(version)
				stat_dict['hashrate'] = summary_dict.get('KHS')
				stat_dict['hashrate_unit'] = 'KHS'
				stat_dict['gpu_num'] = summary_dict.get('GPUS')

				stat_dict['algo'] = summary_dict.get('ALGO')
				stat_dict['shares_accepted'] = summary_dict.get('ACC')
				stat_dict['shares_rejected'] = summary_dict.get('REJ')
				stat_dict['uptime'] = summary_dict.get('UPTIME')
				stat_dict['difficulty'] = summary_dict.get('DIFF')

				print (stat_dict)

		if self.current_algo in self.ethash_algos:
			output =  self.ethash_api_output()
			if output: 
				gpu_hashrates = output[3].split(";")
				version = output[0]
				stat_dict['current_miner'] = 'ethminer_{}'.format(version)
				stat_dict['hashrate'] = output[2].split(";")[0]
				stat_dict['hashrate_unit'] = "KHS"
				stat_dict['current_server'] = output[7]
				stat_dict['gpu_num'] = len(gpu_hashrates)
				stat_dict['algo'] = "ethash"
				stat_dict['shares_accepted'] = output[1]

				gpu_hash_dict = {}
				temp_dict = {}

				for i,gpu_hash in enumerate(gpu_hashrates):
					gpu_hash_dict[i] = gpu_hash

				for i,temp in enumerate(output[6].split("; ")):
					temp_dict[i] = temp.split(";")[0]

				stat_dict['temps'] = temp_dict
				stat_dict['gpus'] = gpu_hash_dict

		if self.current_algo in self.ewbf_algos:
			output =  self.ewbf_api_output()
			if output: 
				gpu_list = output.get('result')
				stat_dict['current_miner'] = 'ewbf_0.3.4b'
				stat_dict['current_server'] = output.get('current_server')
				if gpu_list: 
					stat_dict['gpu_num'] = len(gpu_list)
					stat_dict['gpus'] = {}
					stat_dict['temps'] = {}
					for i,gpu in enumerate(gpu_list): 
						if not stat_dict.get('shares_accepted'):
							stat_dict['shares_accepted'] = gpu.get('accepted_shares')
							stat_dict['shares_rejected'] = gpu.get('rejected_shares')
							stat_dict['hashrate'] = gpu.get('speed_sps')
						else:
							stat_dict['shares_accepted'] += gpu.get('accepted_shares')
							stat_dict['shares_rejected'] += gpu.get('rejected_shares')
							stat_dict['hashrate'] += gpu.get('speed_sps')

						stat_dict['hashrate_unit'] = "S/S"
						stat_dict['gpus'][i] = gpu.get('speed_sps')
						stat_dict['temps'][i] = gpu.get('temperature')
						stat_dict['algo'] = "equihash"

		return stat_dict