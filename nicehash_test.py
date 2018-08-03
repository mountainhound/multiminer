url_24hr = "https://api.nicehash.com/api?method=stats.global.24h"
url = "https://api.nicehash.com/api?method=simplemultialgo.info"

import requests

nicehash_algos = {0:"scrypt",1:"sha256",2 :"scryptnf",3:"x11",4:"x13",5:'keccak',6:'x15',7:'nist5',8:'neoscrypt',9:'lyra2re',10:'whirlpoolx',
                        11 : 'qubit',12: 'quark',13: 'axiom',14: 'lyra2rev2',15: 'scryptjanenf16',16: 'blake256r8',
                        17: 'blake256r14',18: 'blake256r8vnl',19:'hodl',20: 'daggerhashimoto',21 : 'decred',22 : 'cryptonight',
                        23 : 'lbry',24 : 'equihash',25 : 'pascal',26 : 'x11gost',27 : 'sia',28 : 'blake2s',29 : 'skunk',
                        30 : 'cryptonightV7',31:'cryptonightheavy',32:'lyra2z',33:'x16r'}

hashrate_unit_factors = {'gh/s':1000,'mh/s':1,'kh/s':.001,'h/s':.000001}

nicehash_hashrates = {'ethash':35,'zhash':.000056,'phi1612':33,'cryptonightheavy':.00096,
					'cryptonightV7':.00085,'daggerhashimoto':.000685,'lyra2rev2':64,'neoscrypt':1.4,
					'timetravel10':30,'x16r':15,'lyra2z':3,'phi2':6,'xevan':5.3,'lbry':470,'pascal':1880,
					'x11gost':16.2,'decred':4770,'sia':2960,'blake2s':6978}

power_usage = {'ethash':215,'zhash':215,'phi1612':215,'cryptonightheavy':215,
					'cryptonightV7':215,'equihash':215,'lyra2rev2':215,'neoscrypt':215,
					'timetravel10':215,'x16r':215,'lyra2z':215,'phi2':215,'xevan':215}

power_cost = .1 #KW/h

coin_list = []
ret = requests.get(url)
if ret.status_code == 200: 
	coin_dict = ret.json().get('result')

	for key,value in coin_dict.items():
		algo = value.get('algorithm').lower()
		value['algorithm'] = algo

		if algo in whattomine_hashrates.keys():
			revenue24_adjusted = (float(value.get('btc_revenue24')) * whattomine_hashrates.get(algo))
			revenue_adjusted = (float(value.get('btc_revenue')) * whattomine_hashrates.get(algo))
			coin_dict = {}
			coin_dict['btc_revenue24'] = revenue24_adjusted
			coin_dict['btc_revenue'] = revenue_adjusted
			coin_dict['power_expense'] = (power_cost * .001 * 24) * power_usage.get(algo)
			coin_dict['algo'] = algo
			coin_dict['coin'] = key.lower()
			coin_list.append(coin_dict)
		
		sorted_list = sorted(coin_list, key=lambda k:k['btc_revenue24'], reverse=True)
		
for coin in sorted_list:
	if 'nicehash' in coin.get('coin'):  
		print (coin)
		print ()