from whattomine_api import ProfitCoin
from flask import Flask, render_template, Response, jsonify, flash, redirect, request, session, abort, send_file
import json
import subprocess
import requests,subprocess,shlex,time,datetime,statistics,configparser,sys,re,fcntl,os,random
from telnetlib import Telnet

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import logging
import atexit
logging.basicConfig()

app = Flask(__name__)

def auto_profit_switch():
	with app.app_context():
		ret = main.profit_switch()

scheduler = BackgroundScheduler()
scheduler.start()
scheduler.add_job(
    func=auto_profit_switch,
    trigger=IntervalTrigger(minutes=30),
    id='Checking Profit',
    name='Check Profit Every X Minutes',
    replace_existing=True)
# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())



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
		if mode in main.supported_algos:
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
		self.setting_path = 'conf.json'
		self.settings = self.get_settings()
		self.app = app
		self.runningProcess = None
		self.profit_api = ProfitCoin()
		self.current_algo = self.settings.get('default')
		ret = None
		
		if self.profit_flag:
			ret = self.profit_switch()
		if not self.runningProcess:
			ret = self.set_mining_mode(self.current_algo)
		
		print ("Starting Mining:{}".format(ret))

	def get_settings(self):
		with open(self.setting_path, 'r') as reader:
			info = reader.readline()
			settings = json.loads(info)
			self.supported_algos = settings.get('algos')
			self.profit_flag = settings.get('profit_flag')
		print (self.supported_algos)
		return settings

	def profit_switch(self):
		if self.profit_flag:
			sorted_list = self.profit_api.most_profitable()
			profit_algo = None
			profit_coin = None
			for coin in sorted_list: 
				if coin.get('algorithm').lower() in self.supported_algos: 
					if not profit_algo and not profit_coin:
						profit_algo = coin.get('algorithm').lower()
						profit_coin = coin.get('coin').lower()
			
			if self.current_algo == profit_algo and sorted_list:
				print ("Already mining most profitable algo")
				return "Already mining most profitable algo"
			elif profit_algo: 
				self.set_mining_mode(profit_algo)
				print ("Profit Switching to Algo: {}".format(profit_algo))
				return "Profit Switching to Algo: {}".format(profit_algo)
			print ("NO ALGO FOUND")
			return ("NO ALGO FOUND")

	def set_mining_mode(self,mining_mode):
		ret = 0
		if mining_mode is not self.current_algo or self.runningProcess is None: 
			if self.runningProcess:
				ret = self.stop_mining()


			time.sleep(1)

			if ret < 0 or self.runningProcess is None:
				cmd = './mine.sh -{}'.format(mining_mode)
				
				self.runningProcess=subprocess.Popen(cmd.split(),stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=1)
				
				print ('setting mining mode')
				
				self.current_algo = mining_mode
				output = self.get_miner_output()
			
			return output

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

	def ccminer_api_output(self):
		try: 
			tn = Telnet("localhost","4068")
			tn.write(b"summary")
			output = tn.read_all().decode("utf-8")
			tn.write(b"^]")
			tn.close()

			print (output)
			return output
		except:
			print ("ERROR IN TELNET")

	def get_miner_output(self,n=10):	
		ret = {}
		miner_output = []
		if self.runningProcess:
			for i in range(n):
				miner_output.append(str(self.runningProcess.stdout.readline()))
			
			ret['miner_output'] = miner_output
			ret['current_algo'] = self.current_algo

			return ret
		return None

	def get_miner_stats(self):
		stat_dict = {}
		if self.current_algo in self.settings.get('ccminer_algos'):
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
				stat_dict['shares_accepted'] = int(output[7][5:])
				stat_dict['shares_rejected'] = int(output[8][4:])
				stat_dict['uptime'] = int(output[14][7:])
				stat_dict['difficulty'] = float(output[10][5:])


			return stat_dict

	def run(self):
		self.app.run(port=5000, host='0.0.0.0',debug = True, use_reloader=False)


if __name__ == "__main__":
	main = multiminer(app)
	main.run()