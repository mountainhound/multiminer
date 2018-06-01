import socket
import json

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(5)
s.connect(('10.8.0.101', int(4068)))
#sock.settimeout(None)
command = "miner_getstat1"
message = json.dumps({"id":0,"jsonrpc":"2.0","method":command}) + "\n"
print (type(message))
print (message)
s.sendall(message.encode('utf-8'))
resp = ''
while 1:
     data = s.recv(4096)
     resp += data.decode('utf-8')
     if not data or (len(data) < 4096 and data[-3:] == b']}\n'):
          break
s.close()
print (resp)

ret = json.loads(resp)
print (ret)

stat_dict = {}
output = ret.get('result')
if output: 
	gpu_hashrates = output[3].split(";")
	version = output[0]
	stat_dict['current_miner'] = 'ethminer_{}'.format(version)
	stat_dict['current_server'] = output[7]
	stat_dict['hashrate'] = output[2].split(";")[0]
	stat_dict['hashrate_unit'] = "KHS"
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

print (stat_dict)
