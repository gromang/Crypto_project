import requests
import logging
from accordance import *

logging.basicConfig(filename="parser.log", level=logging.INFO, filemode="w")


def get_data_kraken(symbol, interval):
    exchange = "kraken"
    sym = exch_pairs[exchange][symbol]  # забираем из словаря обозначения
    intr = exch_interval[exchange][interval]  # пары и интервала
    api_url = "https://api.kraken.com/0/public/OHLC"
    params = {
        "pair": sym,
        "interval": intr,
    }
    try:
        get_data = requests.get(api_url, params=params, timeout=5)
        get_data.raise_for_status()
        logging.info(get_data.url)
        coin_data = get_data.json()
        # Так как в запросе нельзя настроить глубину выдачи данных
        # то запрос отдает несколько сотен свечей. Нам нужна для расчета
        # только последняя. В этом json есть запись в конце вида
        # "last":1576159200 - таймкод последней свечи. По нему и найдем.
        last_minute = coin_data["result"]["last"]
        logging.info(f"last minute : {last_minute}",)
        # В получаемом JSON у списка свечей ключ имеет завание 'XXBTZUSD'
        # то есть имя валютной пары разбито на X_XBT_Z_USD
        for candle in coin_data["result"][f"X{sym[:3]}Z{sym[3:]}"]:
            if candle[0] == last_minute:
                logging.info(candle)
                ohlcv = {
                    "Timestamp": candle[0],
                    "Open": float(candle[1]),
                    "Close": float(candle[4]),
                    "High": float(candle[2]),
                    "Low": float(candle[3]),
                    "Volume": float(candle[6]),
                }
                logging.info(f"candle from kraken : {ohlcv}")
                return ohlcv

    except (requests.RequestException, ValueError):
        return False


if __name__ == "__main__":
    print(get_data_kraken("BTCUSD", "1m"))

