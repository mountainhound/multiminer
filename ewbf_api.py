import requests

def ewbf_api_output(url = "localhost",port = "4068"):
	try: 
		data = None
		ret = requests.get("http://{}:{}/getstat".format(url,port))
		if ret.status_code == 200: 
			output = ret.json()	
		print (output)
		return output
	except:
		return False
		print ("ERROR IN EWBF HTTP POST")


output =  ewbf_api_output(url = "10.8.0.101")
stat_dict = {}
print (output)
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

print (stat_dict)
