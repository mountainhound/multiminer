from profit_api import ProfitCoin
from flask import Flask, render_template, Response, jsonify, flash, redirect, request, session, abort, send_file
from gevent.wsgi import WSGIServer
import json
import subprocess
import xmltodict
import requests,subprocess,shlex,time,datetime,statistics,configparser,sys,re,fcntl,os,random
from telnetlib import Telnet
import socket
from queue import Queue
from threading import Thread
import settings
from multiminer import multiminer

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import logging
import atexit
import re
import signal
import sys

logging.basicConfig()

app = Flask(__name__)
main = multiminer(app)

def auto_profit_switch():
	url = "http://localhost:5000/profit_switch"
	ret = requests.get(url)
	print (ret.json())

def maintenance():
	stats = main.get_miner_stats()
	maintenance_stats = main.maintenance_stats
	profit_ts = main.profit_ts
	restart_flag = False
	if stats: 
		hashrate = stats.get('hashrate')
		algo = stats.get('algo')

		if hashrate == 0: 
			print ("Miner appears to be hung.. hashrate is 0 forcing restart")
			restart_flag = True
		
		if maintenance_stats: 
			if algo == maintenance_stats.get('algo') and stats.get('shares_accepted') == maintenance_stats.get('shares_accepted'):
				print ("Miner appears to be hung.. No shares in {} minutes forcing restart".format(settings.maintenance_interval))
				restart_flag = True
	else: 
		print ("Miner not returning stats forcing algo change")
		restart_flag = True

	main.maintenance_stats = stats

	if not profit_ts or ((time.time() - profit_ts) >= (settings.profit_interval*60)) or restart_flag:
		ret = main.profit_switch()
		main.profit_ts = time.time()
		if restart_flag:
			main.miner_restart()

	return None

scheduler = BackgroundScheduler()
scheduler.start()
scheduler.add_job(
    func=maintenance,
    trigger=IntervalTrigger(minutes=settings.maintenance_interval),
    id='Checking Profit',
    name='Check Profit Every X Minutes',
    replace_existing=True)


# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())

def sigint_handler(signum, frame):
	print ("Please Wait Stopping The Miners")
	main.stop_mining()
	time.sleep(.5)
	sys.exit()
 
signal.signal(signal.SIGINT, sigint_handler)

@app.route('/profit_switch', methods=['GET'])
def profit_switch():
	ret = main.profit_switch()
	print (ret)
	return jsonify({'message':ret})

@app.route('/mining_mode', methods=['POST'])
def mining_mode(): 
	mode = None
	if request.json:
		mode = request.json.get('mode')
	if request.form: 
		mode = request.form.get('mode')

	print (mode)

	if mode is None: 
		return jsonify({"message":"Mode not given or algo not supported"}),400

	if mode.strip().lower() == "auto":
		main.profit_flag = True
		main.stop_flag = False
		ret = main.profit_switch()
	elif mode.strip().lower() == "stop":
		ret = main.set_mining_mode(mode)
		main.profit_flag = False
		main.stop_flag = True
	elif mode.strip().lower():
		if mode in main.ccminer_algos or mode in main.ethash_algos or mode in main.ewbf_algos:
			ret = main.set_mining_mode(mode)
			main.stop_flag = False
			main.profit_flag = False
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
	jsonify(ret)
	return jsonify({"data":ret}),200


if __name__ == "__main__":
	http_server = WSGIServer(('',5000),app)
	http_server.serve_forever()