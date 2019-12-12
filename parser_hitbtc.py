from datetime import datetime
import requests


def get_api_hitbtc(url, number_of_data, time_interval):
    params = {

        'period': time_interval,
        'limit': number_of_data
    }

    try:
        result = requests.get(url, params=params)
        result.raise_for_status()
        return result.json()
    except(requests.RequestException, ValueError):
        print('Сетевая ошибка')
        return False


def get_data_hitbtc(trading_couple='BTCUSD', time_interval='M1', number_of_data='150'):
    try:
        coin_data = get_api_hitbtc('https://api.hitbtc.com/api/2/public/candles/' + trading_couple,
                                   number_of_data, time_interval)

        result_news = []
        for coin_results in coin_data:
            data_time = datetime.strptime(coin_results['timestamp'], '%Y-%m-%dT%H:%M:%S.%fZ')
            result_news.append({
                'Timestamp': round(data_time.timestamp()),
                'Open': float(coin_results['open']),
                'Close': float(coin_results['close']),
                'High': float(coin_results['max']),
                'Low': float(coin_results['min']),
                'Volume': round(float(coin_results['volume']), 10),
            })

        return result_news
    except TypeError:
        print('Объект не найден')
        return False


if __name__ == "__main__":
    print(len(get_data_hitbtc(trading_couple='ETHBTC')))
