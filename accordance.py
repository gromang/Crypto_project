# exch_api_kline = {
#     "binance":'https://api.binance.com/api/v3/klines', # ?symbol=BTCUSDT&interval=1m&limit=1
#     "bitfinex":f"https://api-pub.bitfinex.com/v2/candles/trade:{interval}:{symbol}/hist", # ?limit=1
#     "hitbtc":f"https://api.hitbtc.com/api/2/public/candles/{symbol}", # ?period=M1&limit=1
#     "huobi": "https://api.huobi.pro/market/history/kline", # ?period=1min&size=1&symbol=btcusdt
#     "kraken":'https://api.kraken.com/0/public/OHLC', # ?pair=XBTUSD&interval=1&since=Timestamp
# }

# У каждой биржы свои обозначения валютных пар, параметров и их значений.
# Поэтому задаем таблицу соответсвия выбранных нами 
# для проекта валютных пар - парам каждой конкретной биржи.
# Цель - использовать единые аргументы в функциях.
exch_pairs = {
    'binance':{
        'BTCUSD':'BTCUSDT',
        'ETHUSD':'ETHUSDT',
        'LTCUSD':'LTCUSDT',
        'XRPUSD':'XRPUSDT',
        },
    'bitfinex':{
        'BTCUSD':'tBTCUSD',
        'ETHUSD':'tETHUSD',
        'LTCUSD':'tLTCUSD',
        'XRPUSD':'tXRPUSD',
        },
    'hitbtc':{
        'BTCUSD':'BTCUSD',
        'ETHUSD':'ETHUSD',
        'LTCUSD':'LTCUSD',
        'XRPUSD':'XRPUSD',
        },
    'huobi':{
        'BTCUSD':'btcusdt',
        'ETHUSD':'ethusdt',
        'LTCUSD':'ltcusdt',
        'XRPUSD':'xrpusdt',
        },
    'kraken':{
        'BTCUSD':'XBTUSD',
        'ETHUSD':'ETHUSD',
        'LTCUSD':'LTCUSD',
        'XRPUSD':'XRPUSD',
        }
}

exch_interval = {
    'binance':{
        '1m':'1m',
        '5m':'5m',
        '15m':'15m',
        '30m':'30m',
        '1h':'1h',
        '1d':'1d',},
    'bitfinex':{
        '1m':'1m',
        '5m':'5m',
        '15m':'15m',
        '30m':'30m',
        '1h':'1h',
        '1d':'1d',},
    'hitbtc':{
        '1m':'M1',
        '5m':'M5',
        '15m':'M15',
        '30m':'M30',
        '1h':'H1',
        '1d':'D1',},
    'huobi':{
        '1m':'1min',
        '5m':'5min',
        '15m':'15min',
        '30m':'30min',
        '1h':'60min',
        '1d':'1day',},
    'kraken':{
        '1m':1,
        '5m':5,
        '15m':15,
        '30m':30,
        '1h':60,
        '1d':1440,},
}