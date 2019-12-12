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


def get_data_huobi(trading_couple='btcusdt', time_interval='1min', number_of_data=150):
    try:
        coin_data = get_api_huobi('https://api.huobi.pro/market/history/kline',
                                  time_interval, number_of_data, trading_couple)
        # result_news = []
        print(coin_data)
    except TypeError:
        return False


if __name__=="__main__":
    print(get_data_huobi())