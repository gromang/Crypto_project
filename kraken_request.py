import requests

kraken_url='https://api.kraken.com/0/public/OHLC'
params = {
    'pair':'XBTUSD',
    'interval':1
}

try:
    result = requests.get(kraken_url,params=params)
    result.raise_for_status()
    print(result.json())
except(requests.RequestException, ValueError):
    print('Что то не так')
