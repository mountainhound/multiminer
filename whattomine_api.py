
import urllib.request as urllib2
import json
import argparse

#options are current 24hr 3d 7d 

difficulty_period = "current"

SRC_META = {
    'whattomine': {
        'url': "https://whattomine.com/coins.json?utf8=%E2%9C%93&adapt_q_1070=0&adapt_q_1070Ti=0&adapt_q_1080=6&adapt_q_1080Ti=6&adapt_1080Ti=true&eth=true&factor%5Beth_hr%5D=210.0&factor%5Beth_p%5D=840.0&grof=true&factor%5Bgro_hr%5D=348.0&factor%5Bgro_p%5D=1260.0&x11gf=true&factor%5Bx11g_hr%5D=117.0&factor%5Bx11g_p%5D=1020.0&cn=true&factor%5Bcn_hr%5D=4980.0&factor%5Bcn_p%5D=840.0&eq=true&factor%5Beq_hr%5D=4110.0&factor%5Beq_p%5D=1140.0&lre=true&factor%5Blrev2_hr%5D=384000.0&factor%5Blrev2_p%5D=1140.0&ns=true&factor%5Bns_hr%5D=8400.0&factor%5Bns_p%5D=1140.0&lbry=true&factor%5Blbry_hr%5D=2760.0&factor%5Blbry_p%5D=1140.0&bk2bf=true&factor%5Bbk2b_hr%5D=16800.0&factor%5Bbk2b_p%5D=1140.0&bk14=true&factor%5Bbk14_hr%5D=26100.0&factor%5Bbk14_p%5D=1260.0&pas=true&factor%5Bpas_hr%5D=10200.0&factor%5Bpas_p%5D=1260.0&skh=true&factor%5Bskh_hr%5D=285.0&factor%5Bskh_p%5D=1140.0&n5=true&factor%5Bn5_hr%5D=450.0&factor%5Bn5_p%5D=1140.0&factor%5Bl2z_hr%5D=420.0&factor%5Bl2z_p%5D=300.0&factor%5Bcost%5D=0.1&sort=Profit&volume=0&revenue={}&factor%5Bexchanges%5D%5B%5D=&factor%5Bexchanges%5D%5B%5D=abucoins&factor%5Bexchanges%5D%5B%5D=bitfinex&factor%5Bexchanges%5D%5B%5D=bittrex&factor%5Bexchanges%5D%5B%5D=cryptopia&factor%5Bexchanges%5D%5B%5D=hitbtc&factor%5Bexchanges%5D%5B%5D=poloniex&factor%5Bexchanges%5D%5B%5D=yobit&dataset=Main&commit=Calculate",
        'sort_key': 'profitability',
        'reverse': False
    },
    'nicehash': {
        'url': '',
        'sort_key': 'profitability',
        'reverse': True
    }
}


class ProfitCoin(object):
    '''
    This class handles retrieving a list of most
    profitable coins to mine and returning the data
    '''
    def __init__(self, src='whattomine',diff_period='current'):
        self.src = src
        self.url = SRC_META[src]['url'].format(diff_period)
        self.sort_key = SRC_META[src]['sort_key']
        self.get_coin_list()

    def get_json(self):
        url_opener = urllib2.build_opener()
        url_opener.addheaders = [('User-Agent', 'Mozilla/5.0')]
        try:
            response = url_opener.open(self.url)
            string = response.read().decode('utf-8')
            json_obj = json.loads(string)
        except:
            json_obj = {'coins': {}}
        return json_obj

    def print_json(self, json_obj):
        print (json.dumps(json_obj, indent=4, sort_keys=True))

    def get_coin_list(self):
        coin_list = []
        self.json_obj = self.get_json()
        if self.src=='whattomine':
            # coins_list = [v for k,v in json_obj['coins'].iteritems()]
            for coin_set in self.json_obj['coins'].items():
                # we want a dict so get the main data
                coin = coin_set[1]
                # we don't have the name so let's add the key as the coin
                coin['coin'] = coin_set[0]
                # add this coin to the list!
                coin_list.append(coin)
                print (coin_list)
        elif self.src=='nicehash':
            pass
        else:
            pass
        # sort the list of dicts by the key specified
        sorted_list = sorted(coin_list, key=lambda k:k[self.sort_key], reverse=True)
        self.coin_list = sorted_list

    def most_profitable(self):
        self.get_coin_list()
        return self.coin_list


def parse_args():
    parser = argparse.ArgumentParser(description='This script will return the most profitable coin(s) to mine')
    parser.add_argument('-s','--source',
        default='whattomine',
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
    profit_coin=ProfitCoin(args.source,args.diff_period)
    display_count=int(args.num)
    if not profit_coin.coin_list is None:
        print (' '.join([k.get('algorithm')+' , '+k.get('coin')+'\n' for k in profit_coin.coin_list[:display_count]]))
    else:
        print ('')


if __name__ == '__main__':
    main()