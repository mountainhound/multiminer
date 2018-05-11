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

print (doc.get('nvidia_smi_log').get('gpu').get('temperature'))

