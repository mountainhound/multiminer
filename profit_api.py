
import urllib.request as urllib2
import json
import argparse

#options are current 24hr 3d 7d 

difficulty_period = "current"



nicehash_algos = {0:"Scrypt",1:"SHA256",2 :"ScryptNf",3:"X11",4:"X13",5:'Keccak',6:'X15',7:'Nist5',8:'NeoScrypt',9:'Lyra2RE',10:'WhirlpoolX',
                        11 : 'Qubit',12: 'Quark',13: 'Axiom',14: 'Lyra2REv2',15: 'ScryptJaneNf16',16: 'Blake256r8',
                        17: 'Blake256r14',18: 'Blake256r8vnl',19:'Hodl',20: 'DaggerHashimoto',21 : 'Decred',22 : 'CryptoNight',
                        23 : 'Lbry',24 : 'Equihash',25 : 'Pascal',26 : 'X11Gost',27 : 'Sia',28 : 'Blake2s',29 : 'Skunk',
                        30 : 'CryptoNightV7'}

#1080ti
hashrates = {'NeoScrypt':.0014,'Lyra2REv2':.064,'Equihash':.000000685,'CryptoNightV7':.000000830,'CryptoNight':.00000083,
                        'X11Gost':.0195,'DaggerHashimoto':.046,'Nist5':.075,'Skunk':.0475,'Pascal':1.7,'Lbry':.475,'Decred':4.35}

SRC_META = {
    'whattomine': {
        'url': "http://whattomine.com/coins.json?utf8=%E2%9C%93&adapt_q_280x=0&adapt_q_380=0&adapt_q_fury=0&adapt_q_470=0&adapt_q_480=3&adapt_q_570=1&adapt_q_580=1&adapt_q_vega56=1&adapt_q_vega64=1&adapt_q_750Ti=1&adapt_q_1050Ti=1&adapt_q_10606=1&adapt_q_1070=0&adapt_q_1070Ti=0&adapt_q_1080=6&adapt_q_1080Ti=1&eth=true&factor%5Beth_hr%5D=46&factor%5Beth_p%5D=140.0&grof=true&factor%5Bgro_hr%5D=58.0&factor%5Bgro_p%5D=210.0&x11gf=true&factor%5Bx11g_hr%5D=19.5&factor%5Bx11g_p%5D=170.0&cn=true&factor%5Bcn_hr%5D=830.0&factor%5Bcn_p%5D=140.0&cn7=true&factor%5Bcn7_hr%5D=830.0&factor%5Bcn7_p%5D=140.0&eq=true&factor%5Beq_hr%5D=685.0&factor%5Beq_p%5D=190.0&lre=true&factor%5Blrev2_hr%5D=64000.0&factor%5Blrev2_p%5D=190.0&ns=true&factor%5Bns_hr%5D=1400.0&factor%5Bns_p%5D=190.0&tt10=true&factor%5Btt10_hr%5D=30.0&factor%5Btt10_p%5D=200.0&x16r=true&factor%5Bx16r_hr%5D=15.0&factor%5Bx16r_p%5D=190.0&skh=true&factor%5Bskh_hr%5D=47.5&factor%5Bskh_p%5D=190.0&n5=true&factor%5Bn5_hr%5D=75.0&factor%5Bn5_p%5D=190.0&xn=true&factor%5Bxn_hr%5D=5.3&factor%5Bxn_p%5D=190.0&factor%5Bcost%5D=0.1&sort=Profit&volume=0&revenue=current&factor%5Bexchanges%5D%5B%5D=&factor%5Bexchanges%5D%5B%5D=bitfinex&factor%5Bexchanges%5D%5B%5D=bittrex&factor%5Bexchanges%5D%5B%5D=cryptopia&factor%5Bexchanges%5D%5B%5D=hitbtc&factor%5Bexchanges%5D%5B%5D=yobit&dataset=Main&commit=Calculate",
    },
    'nicehash': {
        'url': 'https://api.nicehash.com/api?method=simplemultialgo.info&location=1',
    },
    'sort_key': 'btc_revenue'
}


class ProfitCoin(object):
    '''
    This class handles retrieving a list of most
    profitable coins to mine and returning the data
    '''
    def __init__(self,diff_period='current',src = None):
        self.src = src
        self.whattomine_url = SRC_META['whattomine']['url'].format(diff_period)
        self.nicehash_url = SRC_META['nicehash']['url'].format(diff_period)
        self.sort_key = SRC_META['sort_key']
        self.get_coin_list()

    def get_json(self,url):
        url_opener = urllib2.build_opener()
        url_opener.addheaders = [('User-Agent', 'Mozilla/5.0')]
        try:
            response = url_opener.open(url)
            string = response.read().decode('utf-8')
            json_obj = json.loads(string)
        except:
            json_obj = {'coins': {},'result':{}}
        return json_obj

    def print_json(self, json_obj):
        print (json.dumps(json_obj, indent=4, sort_keys=True))

    def get_coin_list(self):
        coin_list = []
        if self.src is not "nicehash":
            self.json_obj = self.get_json(self.whattomine_url)
            # coins_list = [v for k,v in json_obj['coins'].iteritems()]

            for coin_set in self.json_obj['coins'].items():
                coin_dict = {}
                # we want a dict so get the main data
                coin = coin_set[1]
                # we don't have the name so let's add the key as the coin
                coin_dict['algorithm'] = coin.get('algorithm')
                coin_dict['btc_revenue'] = float(coin.get('btc_revenue'))
                coin_dict['coin'] = coin_set[0]
                # add this coin to the list!
                coin_list.append(coin_dict)

        if self.src is not "whattomine":
            self.json_obj = self.get_json(self.nicehash_url)
            algo_list = self.json_obj.get('result').get('simplemultialgo')

            if algo_list is not None: 
                for algo in algo_list:
                    algo_dict = {}
                    algo_num = algo.get('algo')
                    paying = float(algo.get('paying'))
                    algo_name = nicehash_algos.get(algo_num)
                    algo_hashrate = hashrates.get(algo_name)
                    if algo_hashrate: 
                        revenue = paying * algo_hashrate
                        algo_dict['algorithm'] = "nicehash-"+algo_name
                        algo_dict['coin'] = "nicehash-"+algo_name
                        algo_dict['btc_revenue'] = revenue
                        coin_list.append(algo_dict)

            #print (coin_list)

        # sort the list of dicts by the key specified
        sorted_list = sorted(coin_list, key=lambda k:k[self.sort_key], reverse=True)
        self.coin_list = sorted_list
        #print (self.coin_list)

    def most_profitable(self):
        self.get_coin_list()
        return self.coin_list


def parse_args():
    parser = argparse.ArgumentParser(description='This script will return the most profitable coin(s) to mine')
    parser.add_argument('-s','--source',
        default=None,
        help='Data Source - a url to a JSON datasource')
    parser.add_argument('-num','--num',
        default=1,
        type = int,
        help='Number of coins to display',
        )
    parser.add_argument('-diff_period','--diff_period',
        default="current",
        type = str,
        help='Can be either current, 24hr, 3d, 7d'
        )
    args = parser.parse_args()
    # if not (opts.plot_file or opts.csv_file):
    #     parser.error("You have to specify either a --csv-file or --plot-file!")
    return args


def main():
    args = parse_args()
    profit_coin=ProfitCoin(args.diff_period,args.source)
    display_count=int(args.num)
    if not profit_coin.coin_list is None:
        print (' '.join([k.get('algorithm')+' , '+k.get('coin')+'\n' for k in profit_coin.coin_list[:display_count]]))
    else:
        print ('')


if __name__ == '__main__':
    main()