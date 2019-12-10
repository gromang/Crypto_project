import requests


def get_ip_binance(url):
    try:
        result = requests.get(url)
        result.raise_for_status()
        return result.json()
    except(requests.RequestException, ValueError):
        print("Сетевая ошибка")
        return False


def get_btc_usdt():
    coin_data = get_ip_binance('https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=1m')
    result_news = []
    for coin_results in coin_data:
        result_news.append({
            'Open_time': coin_results[0],
            'Open': coin_results[1],
            'High': coin_results[2],
            'Low': coin_results[3],
            'Close': coin_results[4],
            'Volume': coin_results[5],
            'Close_time': coin_results[6],
            'Quote_asset_volume': coin_results[7]
            })
    return result_news


if __name__ == "__main__":
    print(get_btc_usdt())
