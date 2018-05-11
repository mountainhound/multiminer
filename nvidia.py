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

if isinstance(gpu_list, dict): 
	print (gpu_list.get('temperature'))
else:
	print (gpu_list)
	for gpu in gpu_list:
		print (gpu.get('temperature'))

		