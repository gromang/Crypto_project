from parser_bitfinex import *
from parser_kraken import *
from collections import Counter


def final_ohlcv(symbol, interval):
    ohlcv_list = []
    # Получаем последнюю свечу с каждой биржи
    kraken_candle = get_data_bitfinex(symbol, interval)
    bitfinex_candle = get_data_kraken(symbol, interval)
    # Формируем список последних свечей
    if kraken_candle:
        ohlcv_list.append(kraken_candle)
    if bitfinex_candle:
        ohlcv_list.append(bitfinex_candle)
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
    logging.info(f"Finall {interval} candle for {symbol} equal : {sum_ohlcv}")

    return sum_ohlcv


if __name__ == "__main__":
    print(final_ohlcv("BTCUSD", "1m"))

