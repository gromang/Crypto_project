from parser_binance import *
from parser_bitfinex import *
from parser_hitbtc import *
from parser_huobi import *
from parser_kraken import *

from collections import Counter


def final_ohlcv(symbol, interval):
    ohlcv_list = []
    # Получаем последнюю свечу с каждой биржи
    bitfinex_candle = get_data_kraken(symbol, interval)
    binance_candle = get_data_binance(symbol, interval)
    hitbtc_candle = get_data_hitbtc(symbol, interval)
    huobi_candle = get_data_huobi(symbol, interval)
    kraken_candle = get_data_bitfinex(symbol, interval)

    # Формируем список последних свечей
    if bitfinex_candle:
        ohlcv_list.append(bitfinex_candle)
    if binance_candle:
        ohlcv_list.append(binance_candle)
    if hitbtc_candle:
        ohlcv_list.append(hitbtc_candle)
    if huobi_candle:
        ohlcv_list.append(huobi_candle)
    if kraken_candle:
        ohlcv_list.append(kraken_candle)

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
        "Timestamp": ohlcv_list[0]["Timestamp"],
        "Open": round(sum_open, 1),
        "Close": round(sum_close, 1),
        "High": round(sum_high, 1),
        "Low": round(sum_low, 1),
        "Volume": sum_vol,
    }
    logging.info(f"Final {interval} candle for {symbol} equal : {sum_ohlcv}")

    return sum_ohlcv


if __name__ == "__main__":
    print(final_ohlcv("BTCUSD", "1m"))

