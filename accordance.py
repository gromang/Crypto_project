exchanges = ('binance','bitfinex','hitbtc','huobi','kraken')

exchanges_api_kline = {
    "binance":{
        'api':'https://api.binance.com/api/v3/klines', # ?symbol=BTCUSDT&interval=1m&limit=1
        'full_params':True
        },
    "bitfinex": {
        'api': f"https://api-pub.bitfinex.com/v2/candles/trade:{interval}:{symbol}/hist", # ?limit=1
        'full_params':False
        },
    "hitbtc": {
        'api': f"https://api.hitbtc.com/api/2/public/candles/{symbol}", # ?period=M1&limit=1
        'full_params':False
        },   
    "huobi": {
        'api': "https://api.huobi.pro/market/history/kline", # ?period=1min&size=1&symbol=btcusdt
        'full_params':True
        }, 
    "kraken":{
        'api':'https://api.kraken.com/0/public/OHLC', # ?pair=XBTUSD&interval=1&since=Timestamp
         'full_params':True
        },    
}

# У каждой биржы свои обозначения валютных пар, параметров и их значений.
# Поэтому задаем таблицу соответсвия выбранных нами 
# для проекта валютных пар - парам каждой конкретной биржи.
# Цель - использовать единые аргументы в функциях.
pairs_by_exchanges = {
    'binance':{'BTCUSD':'BTCUSDT','ETHUSD':'ETHUSDT','LTCUSD':'LTCUSDT','XRPUSD':'XRPUSDT','EOSUSD':None,},
    'bitfinex':{'BTCUSD':'tBTCUSD','ETHUSD':'tETHUSD','LTCUSD':'tLTCUSD','XRPUSD':'tXRPUSD','EOSUSD':'tEOSUSD',},
    'hitbtc':{'BTCUSD':'BTCUSD','ETHUSD':'ETHUSD','LTCUSD':'LTCUSD','XRPUSD':'XRPUSD','EOSUSD':'EOSUSD',},
    'huobi':{'BTCUSD':'btcusdt','ETHUSD':'ethusdt','LTCUSD':'ltcusdt','XRPUSD':'xrpusdt','EOSUSD':'eosusdt',},
    'kraken':{'BTCUSD':'XBTUSD','ETHUSD':'ETHUSD','LTCUSD':'LTCUSD','XRPUSD':'XRPUSD','EOSUSD':'EOSUSD',}
}

parameters_by_exchanges = {
    'binance':{'symbol':'symbol','interval':'interval','limit':'limit'},
    'bitfinex':{'limit':'limit'},
    'hitbtc':{'interval':'period','limit':'limit'},
    'huobi':{'symbol':'symbol','interval':'period','limit':'size'},
    'kraken':{'symbol':'pair','interval':'interval','limit':'limit'},

}

intervals_by_exchanges = {
    'binance':{'1m':'1m','5m':'5m','15m':'15m','30m':'30m','1h':'1h','1d':'1d',},
    'bitfinex':{'1m':'1m','5m':'5m','15m':'15m','30m':'30m','1h':'1h','1d':'1d',},
    'hitbtc':{'1m':'M1','5m':'M5','15m':'M15','30m':'M30','1h':'H1','1d':'D1',},
    'huobi':{'1m':'1min','5m':'5min','15m':'15min','30m':'30min','1h':'60min','1d':'1day',},
    'kraken':{'1m':1,'5m':5,'15m':15,'30m':30,'1h':60,'1d':1440,},
}