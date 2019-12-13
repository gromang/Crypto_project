from datetime import datetime
import logging
import requests

from accordance import *

logging.basicConfig(filename='parser.log', level=logging.INFO, filemode='w')


def get_data_hitbtc(symbol, interval):
    exchange = 'hitbtc'
    # Забираем из словаря обозначения пары(sym) и интервала(intr)
    sym = exch_pairs[exchange][symbol]
    intr = exch_interval[exchange][interval]
    api_url = 'https://api.hitbtc.com/api/2/public/candles/'
    params = {
        'limit': '5',
        'period': intr,
    }

    try:
        get_data = requests.get(f'{api_url}{sym}', params=params, timeout=5)
        get_data.raise_for_status()
        logging.info(f"HitBTC API : {get_data.url}")
        coin_data = get_data.json()
        logging.info(coin_data)
        candle = coin_data[-1]
        logging.info(f"HitBTC initial candle : {candle}")
        # Преобразование даты в timestamp
        data_time = datetime.strptime(candle['timestamp'], '%Y-%m-%dT%H:%M:%S.%fZ')
        # Преобразование данных к нужному формату
        ohlcv = {
            'Timestamp': round(data_time.timestamp()),
            'Open': round(float(candle['open']), 1),
            'Close': round(float(candle['close']), 1),
            'High': round(float(candle['max']), 1),
            'Low': round(float(candle['min']), 1),
            'Volume': round(float(candle['volume']), 10)
        }

        logging.info(f"HitBTC result : {ohlcv}")
        return ohlcv
    except(requests.RequestException, ValueError):
        print('Сетевая ошибка')
        return False


if __name__ == "__main__":
    print((get_data_hitbtc('BTCUSD', '1m')))
