import logging
import requests

from accordance import *

logging.basicConfig(filename="parser.log", level=logging.INFO, filemode="w")


def get_data_huobi(symbol, interval):
    exchange = "huobi"
    # Забираем из словаря обозначения пары(sym) и интервала (intr)
    sym = exch_pairs[exchange][symbol]
    intr = exch_interval[exchange][interval]
    api_url = "https://api.huobi.pro/market/history/kline"
    params = {
        "period": intr,
        "size": "5",
        "symbol": sym,
    }

    try:
        get_data = requests.get(f"{api_url}", params=params, timeout=5)
        get_data.raise_for_status()
        logging.info(f"Huobi API : {get_data.url}")
        coin_data = get_data.json()
        candle = coin_data["data"][1]
        logging.info(f"Huobi initial candle : {candle}")
        # Преобразование данных к нужному формату
        ohlcv = {
            "Timestamp": candle["id"],
            "Open": round(float(candle["open"]), 1),
            "Close": round(float(candle["close"]), 1),
            "High": round(float(candle["high"]), 1),
            "Low": round(float(candle["low"]), 1),
            "Volume": round(float(candle["amount"]), 10),
        }

        logging.info(f"Huobi result : {ohlcv}")
        return ohlcv
    except (requests.RequestException, ValueError):
        print("Сетевая ошибка")
        return False


if __name__ == "__main__":
    print((get_data_huobi("BTCUSD", "1m")))

