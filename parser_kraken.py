import requests
import logging
from  accordance import *

logging.basicConfig(filename="parser.log",level=logging.INFO,filemode='w')

def get_data_kraken(symbol,interval):
    exchange = 'kraken'
    kraken_url='https://api.kraken.com/0/public/OHLC'
    params = {
        'pair':exch_pairs[exchange][symbol],            #забираем из словаря обозначения
        'interval':exch_interval[exchange][interval],   #пары и интервала
    }
    try:
        get_data = requests.get(kraken_url,params=params)
        get_data.raise_for_status()
        logging.info(get_data.url)
        coin_data = get_data.json()
        # Так как в запросе нельзя настроить глубину выдачи данных
        # то запрос отдает несколько сотен свечей. Нам нужна для расчета
        # только последняя. В этом json есть запись в конце вида
        # "last":1576159200 - таймкод последней свечи. По нему и найдем.
        last_minute = coin_data['result']['last']
        ohlcv = from keys in coin_data['result'][last_minute]
        
        
    except(requests.RequestException, ValueError):
        return False

if __name__ == "__main__":
    get_data_kraken("BTCUSD","1m")



# def get_data_binance(trading_couple='BTCUSDT', time_interval='1m'):
#     try:
#         coin_data = get_api_binance('https://api.binance.com/api/v3/klines', trading_couple, time_interval)

#         result_news = []
#         for coin_results in coin_data:
#             result_news.append({
#                 'Timestamp': coin_results[0],
#                 'Open': float(coin_results[1]),
#                 'Close': float(coin_results[4]),
#                 'High': float(coin_results[2]),
#                 'Low': float(coin_results[3]),
#                 'Volume': float(coin_results[5]),
#             })

#         return result_news
#     except TypeError:
#         print('Объект не найден')
#         return False


# if __name__ == "__main__":
#     print(get_data_binance())