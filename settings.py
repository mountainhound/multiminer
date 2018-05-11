ccminer_algos = ["lyra2rev2","nicehash-lyra2rev2","equihash","nicehash-equihash","blake2s",
					"neoscrypt","scrypt","x11","lyra2z","decred","x11gost","nist5","lbry",
					"nicehash-lbry","xevan","nicehash-xevan","phi1612","timetravel10"]

#removed "lyra2rev2" and "nicehash-lyra2rev2", due to segmentation faults with many cards looking for alternative. 

ethash_algos = ["ethash","nicehash-ethash"]

profit_flag = True

default = "equihash"

profit_interval = 10 #minutes
maintenance_interval = .5 #minutes
