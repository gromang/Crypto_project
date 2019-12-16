import logging
import requests
import json


class crypto_candle:
    def __init__(self, symbol, interval="1m"):
        self.symbol = symbol.upper()
        self.interval = interval.lower()
        self.data = {}
        with open("relations.json", "r") as json_file:
            relation = json.load(json_file)

    def binance(self):
        self.sym = relation["binance"][self.symbol]
        self.intr = relation["binance"][self.interval]
        self.api_url = "https://api.binance.com/api/v3/klines"
        self.params = {
            "symbol": self.sym,
            "interval": self.intr,
        }

        try:
            self.get_data = requests.get(
                f"{self.api_url}", params=self.params, timeout=5
            )
            self.get_data.raise_for_status()
            logging.info(f"BINANCE API : {get_data.url}")
            self.coin_data = self.get_data.json()
            candle = coin_data[-1]
            logging.info(f"BINANCE initial candle : {candle}")
            # Преобразование данных к нужному формату
            ohlcv = {
                "Timestamp": round(candle[0] / 1000),
                "Open": round(float(candle[1]), 1),
                "Close": round(float(candle[4]), 1),
                "High": round(float(candle[2]), 1),
                "Low": round(float(candle[3]), 1),
                "Volume": round(float(candle[5]), 10),
            }

            logging.info(f"BINANCE result : {ohlcv}")
            return ohlcv
        except (requests.RequestException, ValueError):
            print("Сетевая ошибка")
            return False

