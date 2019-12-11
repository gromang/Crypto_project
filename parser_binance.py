import requests


def get_api_binance(url, trading_couple, time_interval):
    params = {
        'symbol': trading_couple,
        'interval': time_interval,
    }

    try:
        result = requests.get(url, params=params)
        result.raise_for_status()
        return result.json()
    except(requests.RequestException, ValueError):
        print("Сетевая ошибка")
        return False


def get_data_binance(trading_couple='BTCUSDT', time_interval='1m'):
    try:
        coin_data = get_api_binance('https://api.binance.com/api/v3/klines', trading_couple, time_interval)

        result_news = []
        for coin_results in coin_data:
            result_news.append({
                'Timestamp': coin_results[0],
                'Open': float(coin_results[1]),
                'Close': float(coin_results[4]),
                'High': float(coin_results[2]),
                'Low': float(coin_results[3]),
                'Volume': float(coin_results[5]),
            })

        return result_news
    except TypeError:
        print('Объект не найден')
        return False


if __name__ == "__main__":
    print(get_data_binance())
