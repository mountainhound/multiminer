""" 
Parse output of nvidia-smi into a python dictionary.
This is very basic!
"""

import subprocess
import xmltodict
import pprint
import json

 
sp = subprocess.Popen(['nvidia-smi', '-q','-x','-f','temp.xml'])
sp.wait()

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
		
return temp_list

sp = subprocess.Popen(['rm','temp.xml'])
sp.wait()