from datetime import datetime
import json
import logging
import psycopg2
import requests

from config import database

logging.basicConfig(filename="parser.log", level=logging.INFO, filemode="w")


class CryptoCandle:
    def __init__(self, symbol, interval="1m", settings_path="relations.json"):
        self.symbol = symbol.upper()
        self.interval = interval.lower()
        self.data = {}
        self.settings_path = settings_path
        with open(self.settings_path, "r") as json_file:
            self.relation = json.load(json_file)

    def binance(self):
        exchange = "binance"
        sym = self.relation[exchange][self.symbol]
        intr = self.relation[exchange][self.interval]
        api_url = self.relation[exchange]["candle_api"]
        params = {
            "symbol": sym,
            "interval": intr,
        }
        try:
            get_data = requests.get(f"{api_url}", params=params, timeout=5)
            get_data.raise_for_status()
        except (
                requests.exceptions.RequestException,
                requests.exceptions.HTTPError,
        ) as err:
            logging.error(f"{exchange.upper()} ERROR: {err}")
            return False
        logging.info(f"{exchange.upper()} API : {get_data.url}")
        coin_data = get_data.json()
        candle = coin_data[-2]
        logging.info(f"{exchange.upper()} initial candle : {candle}")
        # Преобразование данных к нужному формату
        ohlcv = {
            "Timestamp": round(candle[0] / 1000),
            "Open": round(float(candle[1]), 1),
            "Close": round(float(candle[4]), 1),
            "High": round(float(candle[2]), 1),
            "Low": round(float(candle[3]), 1),
            "Volume": round(float(candle[5]), 10),
        }
        logging.info(f"{exchange.upper()} result : {ohlcv}")
        return ohlcv

    def bitfinex(self):
        exchange = "bitfinex"
        sym = self.relation[exchange][self.symbol]
        intr = self.relation[exchange][self.interval]
        api_url = self.relation[exchange]["candle_api"]
        try:
            get_data = requests.get(f"{api_url}{intr}:{sym}/hist?limit=2", timeout=5)
            get_data.raise_for_status()
        except (
                requests.exceptions.RequestException,
                requests.exceptions.HTTPError,
        ) as err:
            logging.error(f"{exchange.upper()} ERROR: {err}")
            return False
        logging.info(f"{exchange.upper()} API : {get_data.url}")
        coin_data = get_data.json()
        logging.info(coin_data)
        candle = coin_data[-1]
        logging.info(f"{exchange.upper()} initial candle : {candle}")
        ohlcv = {
            "Timestamp": int(candle[0] / 1000),
            "Open": round(candle[1], 1),
            "Close": round(candle[2], 1),
            "High": round(candle[3], 1),
            "Low": round(candle[4], 1),
            "Volume": round(candle[5], 10),
        }
        logging.info(f"{exchange.upper()} result : {ohlcv}")
        return ohlcv

    def hitbtc(self):
        exchange = "hitbtc"
        sym = self.relation[exchange][self.symbol]
        intr = self.relation[exchange][self.interval]
        api_url = self.relation[exchange]["candle_api"]
        params = {
            "limit": "5",
            "period": intr,
        }
        try:
            get_data = requests.get(f"{api_url}{sym}", params=params, timeout=5)
            get_data.raise_for_status()
        except (
                requests.exceptions.RequestException,
                requests.exceptions.HTTPError,
        ) as err:
            logging.error(f"{exchange.upper()} ERROR: {err}")
            return False
        logging.info(f"{exchange.upper()} API : {get_data.url}")
        coin_data = get_data.json()
        logging.info(coin_data)
        candle = coin_data[-2]
        logging.info(f"{exchange.upper()} initial candle : {candle}")
        data_time = datetime.strptime(candle["timestamp"], "%Y-%m-%dT%H:%M:%S.%fZ")
        ohlcv = {
            "Timestamp": round(data_time.timestamp() + 10800),
            "Open": round(float(candle["open"]), 1),
            "Close": round(float(candle["close"]), 1),
            "High": round(float(candle["max"]), 1),
            "Low": round(float(candle["min"]), 1),
            "Volume": round(float(candle["volume"]), 10),
        }
        logging.info(f"{exchange.upper()} result : {ohlcv}")
        return ohlcv

    def huobi(self):
        exchange = "huobi"
        sym = self.relation[exchange][self.symbol]
        intr = self.relation[exchange][self.interval]
        api_url = self.relation[exchange]["candle_api"]
        params = {
            "period": intr,
            "size": "5",
            "symbol": sym,
        }
        try:
            get_data = requests.get(f"{api_url}", params=params, timeout=5)
            get_data.raise_for_status()
        except (
                requests.exceptions.RequestException,
                requests.exceptions.HTTPError,
        ) as err:
            logging.error(f"{exchange.upper()} ERROR: {err}")
            return False
        logging.info(f"{exchange.upper()} API : {get_data.url}")
        coin_data = get_data.json()
        candle = coin_data["data"][1]
        logging.info(f"{exchange.upper()} initial candle : {candle}")
        ohlcv = {
            "Timestamp": candle["id"],
            "Open": round(float(candle["open"]), 1),
            "Close": round(float(candle["close"]), 1),
            "High": round(float(candle["high"]), 1),
            "Low": round(float(candle["low"]), 1),
            "Volume": round(float(candle["amount"]), 10),
        }
        logging.info(f"{exchange.upper()} result : {ohlcv}")
        return ohlcv

    def kraken(self):
        exchange = "kraken"
        sym = self.relation[exchange][self.symbol]
        intr = self.relation[exchange][self.interval]
        api_url = self.relation[exchange]["candle_api"]
        params = {
            "pair": sym,
            "interval": intr,
        }
        try:
            get_data = requests.get(api_url, params=params, timeout=5)
            get_data.raise_for_status()
        except (
                requests.exceptions.RequestException,
                requests.exceptions.HTTPError,
        ) as err:
            logging.error(f"{exchange.upper()} ERROR: {err}")
            return False
        logging.info(f"{exchange.upper()} API : {get_data.url}")
        coin_data = get_data.json()
        # Так как в запросе нельзя настроить глубину выдачи данных
        # то запрос отдает несколько сотен свечей. Нам нужна для расчета
        # только последняя. В этом json есть запись в конце вида
        # "last":1576159200 - таймкод последней свечи. По нему и найдем.
        last_minute = coin_data["result"]["last"]
        logging.info(f"{exchange.upper()} last minute : {last_minute}", )
        # В получаемом JSON у списка свечей ключ имеет завание 'XXBTZUSD'
        # то есть имя валютной пары разбито на X_XBT_Z_USD
        for candle in coin_data["result"][f"X{sym[:3]}Z{sym[3:]}"]:
            if candle[0] == last_minute:
                logging.info(f"{exchange.upper()} initial candle : {candle}")
                ohlcv = {
                    "Timestamp": candle[0],
                    "Open": float(candle[1]),
                    "Close": float(candle[4]),
                    "High": float(candle[2]),
                    "Low": float(candle[3]),
                    "Volume": float(candle[6]),
                }
                logging.info(f"{exchange.upper()} result : {ohlcv}")
                return ohlcv

    def get_previous_candle_time(self):
        try:
            get_utc_time = requests.get("https://yandex.com/time/sync.json")
            get_utc_time.raise_for_status()
        except (
                requests.exceptions.RequestException,
                requests.exceptions.HTTPError,
        ) as err:
            logging.error(f"GET TIME ERROR: {err}")
            return False
        get_utc_time = get_utc_time.json()
        # Забираем и форматируем Timestamp (отбрасываем милисекунды)
        utc_ts = int(str(get_utc_time["time"])[:-3])
        # Получаем текущую минуту
        current_minute_time = datetime.fromtimestamp(utc_ts).strftime("%Y-%m-%d %H:%M")
        # Получаем timestamp предыдущей минуты
        ts = int(
            datetime.strptime(current_minute_time, "%Y-%m-%d %H:%M").timestamp() - 60
        )
        logging.info(f"Formed candle time: {ts}")
        return ts

    def result_candle(self):
        candle_time = self.get_previous_candle_time()
        if candle_time:
            ohlcv_list = []
            # Получаем последнюю свечу с каждой биржи
            bitfinex_candle = self.bitfinex()
            binance_candle = self.binance()
            hitbtc_candle = self.hitbtc()
            huobi_candle = self.huobi()
            kraken_candle = self.kraken()

            # Формируем список последних свечей
            if bitfinex_candle and bitfinex_candle["Timestamp"] == candle_time:
                ohlcv_list.append(bitfinex_candle)
            if binance_candle and binance_candle["Timestamp"] == candle_time:
                ohlcv_list.append(binance_candle)
            if hitbtc_candle and hitbtc_candle["Timestamp"] == candle_time:
                ohlcv_list.append(hitbtc_candle)
            if huobi_candle and huobi_candle["Timestamp"] == candle_time:
                ohlcv_list.append(huobi_candle)
            if kraken_candle and kraken_candle["Timestamp"] == candle_time:
                ohlcv_list.append(kraken_candle)

            if len(ohlcv_list) > 0:
                sum_vol = 0
                sum_open = 0
                sum_close = 0
                sum_high = 0
                sum_low = 0
                for c in ohlcv_list:
                    sum_vol += c["Volume"]
                for c in ohlcv_list:
                    sum_open += c["Open"] * c["Volume"] / sum_vol
                    sum_close += c["Close"] * c["Volume"] / sum_vol
                    sum_high += c["High"] * c["Volume"] / sum_vol
                    sum_low += c["Low"] * c["Volume"] / sum_vol
                sum_ohlcv = {
                    "Timestamp": candle_time,
                    "Open": round(sum_open, 1),
                    "Close": round(sum_close, 1),
                    "High": round(sum_high, 1),
                    "Low": round(sum_low, 1),
                    "Volume": round(sum_vol, 1),
                }
                logging.info(
                    f"Final {self.interval} candle for {self.symbol} equal : {sum_ohlcv}"
                )
                return sum_ohlcv
            else:
                logging.error("ohlcv_list is empty")
                return False
        else:
            logging.error("time for the previous candle is not received")
            return False

    def adding_data_to_database(self, table_database: str):
        """Метод принимает название таблицы базы данных, обрабатывает словарь
         и записывает его в базу данных"""

        final_ohlcv = self.result_candle()
        try:
            # Соединение с базой данных
            conn = psycopg2.connect(database=database['database'],
                                    user=database['user'],
                                    password=database['password'],
                                    host=database['host'],
                                    port=database['port'],
                                    )

            logging.info("Database successfully opened")
            if type(final_ohlcv) == dict:
                cur = conn.cursor()
                # Запись в базу данных
                cur.execute(
                    f"""INSERT INTO "{table_database}" ("Timestamp", "Open", "Close", "High", "Low", "Volume") 
                    VALUES(%s,%s,%s,%s,%s,%s)""", (final_ohlcv['Timestamp'], final_ohlcv['Open'], final_ohlcv['Close'],
                                                   final_ohlcv['High'], final_ohlcv['Low'], final_ohlcv['Volume']
                                                   )
                )

                conn.commit()
                logging.info(f"Record successful: {final_ohlcv}")
                conn.close()
            else:
                raise TypeError
        except TypeError:
            logging.info("Data type does not match, error.")
            return False


if __name__ == "__main__":
    candle = CryptoCandle("BTCUSD", "1m")
    candle.adding_data_to_database('Crypto_project')
