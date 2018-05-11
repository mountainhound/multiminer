""" 
Parse output of nvidia-smi into a python dictionary.
This is very basic!
"""

import subprocess
import xmltodict
import pprint
import json
 
sp = subprocess.Popen(['nvidia-smi', '-q','-x','-f', '~/temp.xml'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

with open('temp.xml') as fd:
    doc = xmltodict.parse(fd.read())

pp = pprint.PrettyPrinter(indent=4)
pp.pprint(json.dumps(doc))

