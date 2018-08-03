import requests

url = "http://www.coinwarz.com/v1/api/profitability/?apikey=3913a5d5230e451abbc4c0cf8b26a95c&algo=all"


ret = requests.get(url)

print (ret.json())