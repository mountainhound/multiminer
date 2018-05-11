""" 
Parse output of nvidia-smi into a python dictionary.
This is very basic!
"""

import subprocess

sp = subprocess.Popen(['nvidia-smi', '-q'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

out_str = sp.communicate()
out_str = str(out_str)
out_list = out_str.split('\\n')
print (out_str)
print (out_list)
out_dict = {}

for item in out_list:
    try:
        key, val = item.split(':')
        key, val = key.strip(), val.strip()
        out_dict[key] = val
    except:
        pass

print(out_dict)
