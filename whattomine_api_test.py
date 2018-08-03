import requests


url = "https://whattomine.com/coins.json?utf8=%E2%9C%93&adapt_q_280x=0&adapt_q_380=0&adapt_q_fury=0&adapt_q_470=0&adapt_q_480=3&adapt_q_570=0&adapt_q_580=0&adapt_q_vega56=0&adapt_q_vega64=0&adapt_q_750Ti=0&adapt_q_1050Ti=0&adapt_q_10606=0&adapt_q_1070=0&adapt_q_1070Ti=0&adapt_q_1080=0&adapt_q_1080Ti=1&eth=true&factor%5Beth_hr%5D=1.0&factor%5Beth_p%5D=1.0&zh=true&factor%5Bzh_hr%5D=1000000&factor%5Bzh_p%5D=1.0&phi=true&factor%5Bphi_hr%5D=1.0&factor%5Bphi_p%5D=1.0&cnh=true&factor%5Bcnh_hr%5D=1000000&factor%5Bcnh_p%5D=1.0&cn7=true&factor%5Bcn7_hr%5D=1000000&factor%5Bcn7_p%5D=1.0&eq=true&factor%5Beq_hr%5D=1000000&factor%5Beq_p%5D=1.0&lre=true&factor%5Blrev2_hr%5D=1000&factor%5Blrev2_p%5D=1.0&ns=true&factor%5Bns_hr%5D=1000&factor%5Bns_p%5D=1.0&tt10=true&factor%5Btt10_hr%5D=1.0&factor%5Btt10_p%5D=1.0&x16r=true&factor%5Bx16r_hr%5D=1.0&factor%5Bx16r_p%5D=1.0&l2z=true&factor%5Bl2z_hr%5D=1.0&factor%5Bl2z_p%5D=1.0&phi2=true&factor%5Bphi2_hr%5D=1.0&factor%5Bphi2_p%5D=1.0&xn=true&factor%5Bxn_hr%5D=1.0&factor%5Bxn_p%5D=1.0&factor%5Bcost%5D=0.1&sort=Profitability24&volume=0&revenue=24h&factor%5Bexchanges%5D%5B%5D=&factor%5Bexchanges%5D%5B%5D=binance&factor%5Bexchanges%5D%5B%5D=bitfinex&factor%5Bexchanges%5D%5B%5D=bittrex&factor%5Bexchanges%5D%5B%5D=cryptobridge&factor%5Bexchanges%5D%5B%5D=cryptopia&factor%5Bexchanges%5D%5B%5D=hitbtc&factor%5Bexchanges%5D%5B%5D=poloniex&factor%5Bexchanges%5D%5B%5D=yobit&dataset=Main&commit=Calculate"

hashrate_unit_factors = {'gh/s':1000,'mh/s':1,'kh/s':.001,'h/s':.000001}

whattomine_hashrates = {'ethash':35,'zhash':.000056,'phi1612':33,'cryptonightheavy':.00096,
					'cryptonightV7':.00085,'equihash':.000685,'lyra2rev2':64,'neoscrypt':1.4,
					'timetravel10':30,'x16r':15,'lyra2z':3,'phi2':6,'xevan':5.3}

power_usage = {'ethash':215,'zhash':215,'phi1612':215,'cryptonightheavy':215,
					'cryptonightV7':215,'equihash':215,'lyra2rev2':215,'neoscrypt':215,
					'timetravel10':215,'x16r':215,'lyra2z':215,'phi2':215,'xevan':215}

power_cost = .1 #KW/h

coin_list = []
ret = requests.get(url)
if ret.status_code == 200: 
	ret_dict = ret.json().get('coins')

	for key,value in ret_dict.items():
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
	

		