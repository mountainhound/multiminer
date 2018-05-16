ccminer_algos = ["lyra2rev2","nicehash-lyra2rev2","nicehash-equihash","blake2s",
					"neoscrypt","scrypt","x11","lyra2z","decred","x11gost","nist5","lbry",
					"nicehash-lbry","xevan","nicehash-xevan","phi1612","timetravel10"]

#removed "lyra2rev2" and "nicehash-lyra2rev2", due to segmentation faults with many cards looking for alternative. 

ewbf_algos = ["equihash","nicehash-equihash"]

ethash_algos = ["ethash","nicehash-ethash"]

profit_flag = True

default = "equihash"

profit_interval = 60 #minutes
maintenance_interval = 5 #minutes
