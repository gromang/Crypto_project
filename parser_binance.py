import logging
import requests

from accordance import *

logging.basicConfig(filename='parser.log', level=logging.INFO, filemode='w')


def get_data_binance(symbol, interval):
    exchange = 'binance'
    # Забираем из словаря обозначения пары(sym) и интервала(intr)
    sym = exch_pairs[exchange][symbol]
    intr = exch_interval[exchange][interval]
    api_url = 'https://api.binance.com/api/v3/klines'
    params = {
        'symbol': sym,
        'interval': intr,
    }

    try:
        get_data = requests.get(f'{api_url}', params=params, timeout=5)
        get_data.raise_for_status()
        logging.info(f"BINANCE API : {get_data.url}")
        coin_data = get_data.json()
        candle = coin_data[-1]
        logging.info(f"BINANCE initial candle : {candle}")
        # Преобразование данных к нужному формату
        ohlcv = {
            'Timestamp': round(candle[0] / 1000),
            'Open': round(float(candle[1]), 1),
            'Close': round(float(candle[4]), 1),
            'High': round(float(candle[2]), 1),
            'Low': round(float(candle[3]), 1),
            'Volume': round(float(candle[5]), 10)
        }

        logging.info(f"BINANCE result : {ohlcv}")
        return ohlcv
    except(requests.RequestException, ValueError):
        print('Сетевая ошибка')
        return False


if __name__ == "__main__":
    print(get_data_binance('BTCUSD', '1m'))
