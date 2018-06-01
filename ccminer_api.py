from telnetlib import Telnet




def ccminer_api_output(command = b"summary",url = "localhost",port = "4068"):
	try: 
		tn = Telnet(url,port)
		tn.write(command)
		output = tn.read_all().decode("utf-8")
		tn.write(b"^]")
		tn.close()

		print (output)
		return output
	except:
		return None
		print ("ERROR IN TELNET")



stat_dict = {}

threads_output = ccminer_api_output(command = b"threads",url = "10.8.0.101")
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

summary_output = ccminer_api_output(command = b"summary",url = "10.8.0.101")
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
#threads output:
#GPU=0;BUS=11;CARD=EVGA GTX 1080 Ti;TEMP=64.0;POWER=189634;FAN=37;RPM=0;FREQ=1670;MEMFREQ=5505;GPUF=1833;MEMF=5005;KHS=31085.91;KHW=163.92585;PLIM=200000;ACC=64;REJ=0;HWF=0;I=20.0;THR=1048576|GPU=1;BUS=12;CARD=EVGA GTX 1080 Ti;TEMP=61.0;POWER=191282;FAN=30;RPM=0;FREQ=1670;MEMFREQ=5505;GPUF=1808;MEMF=5005;KHS=30789.46;KHW=160.96371;PLIM=200000;ACC=78;REJ=1;HWF=0;I=20.0;THR=1048576|GPU=2;BUS=13;CARD=EVGA GTX 1080 Ti;TEMP=65.0;POWER=189230;FAN=40;RPM=0;FREQ=1670;MEMFREQ=5505;GPUF=1827;MEMF=5005;KHS=31326.04;KHW=165.54478;PLIM=200000;ACC=61;REJ=0;HWF=0;I=20.0;THR=1048576|
#summary output:
