import requests
import logging
from accordance import *

logging.basicConfig(filename="parser.log", level=logging.INFO, filemode="w", )


def get_data_bitfinex(symbol, interval):
    exchange = "bitfinex"
    sym = exch_pairs[exchange][symbol]  # забираем из словаря обозначения
    intr = exch_interval[exchange][interval]  # пары и интервала
    api_url = "https://api-pub.bitfinex.com/v2/candles/trade:"
    try:
        get_data = requests.get(f"{api_url}{intr}:{sym}/hist?limit=2", timeout=5)
        get_data.raise_for_status()
        logging.info(f"BITFINEX API : {get_data.url}")
        coin_data = get_data.json()
        candle = coin_data[-1]
        logging.info(f"BITFINEX initial candle : {candle}")
        ohlcv = {
            "Timestamp": int(candle[0] / 1000),
            "Open": round(candle[1], 1),
            "Close": round(candle[2], 1),
            "High": round(candle[3], 1),
            "Low": round(candle[4], 1),
            "Volume": round(candle[5], 10),
        }
        logging.info(f"BITFINEX result : {ohlcv}")
        return ohlcv

    except (requests.RequestException, ValueError) as err:
        logging.info(err)
        return False


if __name__ == "__main__":
    print(get_data_bitfinex("BTCUSD", "1m"))
