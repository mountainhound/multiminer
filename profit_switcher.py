from profit_api import ProfitCoin
from flask import Flask, render_template, Response, jsonify, flash, redirect, request, session, abort, send_file
from gevent.wsgi import WSGIServer
import json
import subprocess
import requests,subprocess,shlex,time,datetime,statistics,configparser,sys,re,fcntl,os,random
from telnetlib import Telnet
from queue import Queue
from threading import Thread
import settings

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import logging
import atexit
import re

logging.basicConfig()

app = Flask(__name__)



def auto_profit_switch():
	url = "http://localhost:5000/profit_switch"
	ret = requests.get(url)
	print (ret.json())

def maintenance():
	stats = main.get_miner_stats()
	restart_flag = False
	if stats: 
		hashrate = stats.get('hashrate')
		if hashrate == 0: 
			restart_flag = True
	else: 
		restart_flag = True

	ret = main.profit_switch(force_switch = restart_flag)


scheduler = BackgroundScheduler()
scheduler.start()
scheduler.add_job(
    func=maintenance,
    trigger=IntervalTrigger(minutes=10),
    id='Checking Profit',
    name='Check Profit Every X Minutes',
    replace_existing=True)


# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())

@app.route('/profit_switch', methods=['GET'])
def profit_switch():
	ret = main.profit_switch()
	print (ret)
	return jsonify({'message':ret})

@app.route('/mining_mode', methods=['POST'])
def mining_mode(): 
	mode = request.json.get('mode')
	print (mode)

	if mode is None: 
		return jsonify({"message":"Mode not given or algo not supported"}),400

	if mode.strip().lower() == "auto":
		main.profit_flag = True
		ret = main.profit_switch()
	elif mode:
		if mode in main.ccminer_algos or main.ethash_algos:
			ret = main.set_mining_mode(mode)
		else:
			return jsonify({"message":"Algo not supported: {}".format(mode)}),200
	return jsonify({"message":"Mining Mode set to {}".format(mode), "response":"{}".format(ret)}),200

@app.route('/miner_output', methods=['GET'])
def miner_output(): 
	n = int(request.args.get('n',10))
	print (n)
	ret = main.get_miner_output(n)

	return jsonify({"data":"{}".format(ret)}),200

@app.route('/miner_stats', methods=['GET'])
def miner_stats(): 
	ret = main.get_miner_stats()

	return jsonify({"data":"{}".format(ret)}),200


class multiminer():
	def __init__(self,app):
		print ("INIT")
		self.setting_path = 'conf.json'
		self.app = app
		self.ccminer_algos = settings.ccminer_algos
		self.ethash_algos = settings.ethash_algos
		self.profit_flag = settings.profit_flag
		self.runningProcess = None
		self.profit_api = ProfitCoin()
		self.current_algo = settings.default
		self.output_q = Queue(maxsize = 100)
		ret = None
		print ("Testing")
		subprocess.Popen('fuser -k 4068/tcp'.split(),stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=1)
		
		if self.profit_flag:
			ret = self.profit_switch()
		if not self.runningProcess:
			ret = self.set_mining_mode(self.current_algo)
		
		print ("Starting Mining:{}".format(ret))
		

	def profit_switch(self,force_switch = False):
		if self.profit_flag:
			sorted_list = self.profit_api.most_profitable()
			profit_algo = None
			profit_coin = None
			for coin in sorted_list: 
				algo = coin.get('algorithm').lower().replace(" ","").replace("(","").replace(")","")
				coin = coin.get('coin').lower().replace(" ","").replace("(","").replace(")","")

				if algo in self.ccminer_algos or self.ethash_algos: 
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

	def output_reader(self,proc, output_q):
		for line in iter(proc.stdout.readline, b''):
			if proc is not None and proc.poll() is None: 
				if output_q.full(): 
					output_q.get()
				output_q.put(line.decode('utf-8'))
				print (line.decode('utf-8'))
			else:
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

	def ccminer_api_output(self,command = b"summary"):
		try: 
			tn = Telnet("localhost","4068")
			tn.write(command)
			output = tn.read_all().decode("utf-8")
			tn.write(b"^]")
			tn.close()

			print (output)
			return output
		except:
			return False
			print ("ERROR IN TELNET")

	def ethash_api_output(self):
		try:
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.connect(('micciminer', 4068))
			s.sendall('{"id":0,"jsonrpc":"2.0","method":"miner_getstat1"}\n'.encode('utf-8'))
			resp = ''
			while 1:
				data = s.recv(4096)
				resp += data.decode('utf-8')
				if not data or (len(data) < 4096 and data[-3:] == b']}\n'):
					break
			s.close()
			
			ret = json.loads().get('result')

		except:
			return False
			print ("ERROR IN JSON RPC")

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
			output =  self.ccminer_api_output()
			if output:
				output = output.replace(";",",")
				output = output.replace("=",":")
				output = output.split(",")
				print (output)

				version = output[1][4:]
				stat_dict['current_miner'] = 'ccminer_{}'.format(version)
				stat_dict['hashrate'] = float(output[5][4:])
				stat_dict['hashrate_unit'] = output[5][:3]
				stat_dict['gpus'] = int(output[4][5:])
				stat_dict['algo'] = output[3][5:]
				stat_dict['shares_accepted'] = int(output[7][4:])
				stat_dict['shares_rejected'] = int(output[8][4:])
				stat_dict['uptime'] = int(output[14][7:])
				stat_dict['difficulty'] = float(output[10][5:])

				thread_output =  self.ccminer_api_output()
				thread_output = thread_output.split(";")

		if self.current_algo in settings.ethash_algos:
			output =  self.ethash_api_output()
			if output: 
				gpu_hashrates = output[3].split(";")
				version = output[0]
				stat_dict['current_miner'] = 'ethminer_{}'.format(version)
				stat_dict['hashrate'] = output[2].split(";")[0]
				stat_dict['hashrate_unit'] = "KHS"
				stat_dict['gpu_num'] = len(gpu_hashrates)
				stat_dict['gpus'] = gpu_hashrates
				stat_dict['algo'] = "ethash"
				stat_dict['shares_accepted'] = output[1]

		return stat_dict

	def run(self):

		http_server = WSGIServer(('',5000),self.app)
		http_server.serve_forever()

		#self.app.run(host='0.0.0.0', port = 5001, debug=False, use_reloader=False, threaded=True)

if __name__ == "__main__":
	main = multiminer(app)
	main.run()