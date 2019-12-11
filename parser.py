import requests

def get_klines(exchange, pair, interval=1,size=1):
    """Функция возвращает список вида [timestamp,open,close,high,low,volume]
    для текущей криптовалютной пары и интервала.
    В случае неудачного выполнения возвращает  False.
    :param exchange:string - Биржа, к API которой выполняется запрос.
    :param pair:string - Криптовалютная пара
    :interval:int - Временной интервал запрашиваемой свечи
    :size:int - Глубина запроса, по умолчанию последняя свеча
    """


# Прописать timeouts в реквесте