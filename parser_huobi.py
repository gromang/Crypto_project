import requests


def get_api_huobi(url, time_interval, number_of_data, trading_couple):
    params = {
        'period': time_interval,
        'size': number_of_data,
        'symbol': trading_couple,
    }

    try:
        result = requests.get(url, params=params)
        print(result)
        result.raise_for_status()
        return result.json()
    except(requests.RequestException, ValueError):
        print('Сетевая ошибка')
        return False


def get_data_huobi(trading_couple='btcusdt', time_interval='1min', number_of_data='150'):
    try:
        coin_data = get_api_huobi('https://api.huobi.pro/market/history/kline',
                                  time_interval, number_of_data, trading_couple)

        result_news = []
        for coin_results in coin_data['data']:
            result_news.append({
                'Timestamp': coin_results['id'],
                'Open': float(coin_results['open']),
                'Close': float(coin_results['close']),
                'High': float(coin_results['high']),
                'Low': float(coin_results['low']),
                'Volume': float(coin_results['amount']),

            })

        return result_news
    except TypeError:
        print('Объект не найден')
        return False


if __name__ == "__main__":
    print(len(get_data_huobi(trading_couple='ethusdt', number_of_data='300')))
