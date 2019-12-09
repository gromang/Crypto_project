## Crypto_project

Данный проект представляет собой приложение, собирающее торговые котировки с основных крупных криптобирж и суммирующее эти данные по настраиваемым алгоритмам. Результат переносится в базу данных. С результирующими котировками в базе данных работает телеграмм-бот, и, в перспективе - торговый алгоритм.

### Определение требуемых данных для построения графика цены
Результат работы системы - построение "суммарных" свечных графиков. 
Свечной график представляет собой последовательное расположение вдоль временной оси японских свечей.
Каждая свеча строится на основе следующих данных:
* цена открытия      - Open
* цена закрытия      - Close
* минимальная цена   - Low
* максимальная цена  - High
* время цены open    - Open time
* интервал свечи     - Interval (1 min, 2 min, 5 min etc.)
Для построения суммарного свечного графика требуется еще один параметр:
* объем свечи        - Volume

### Какие данные может отдать биржа?

Для получения вышеописанных данных, как оказалось, не требуются token`ы или api secret key.
Данные получаются через публичные API бирж. 
В свою очередь, token и secret key, понадобятся на моменте реализации интерфеса для отправки торговых приказов.

По данным ссылкам 4 из 5 выбранных бирж отдают минутные свечи по паре BTCUSD с различной глубиной истории
```
https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=1m

https://api.hitbtc.com/api/2/public/candles/BTCUSD?period=M1

https://api-pub.bitfinex.com/v2/candles/trade:1m:tBTCUSD/hist

https://api.huobi.pro/market/history/kline?period=1min&size=200&symbol=btcusdt
```
Пятая биржа - Kraken - отдает через https://api.kraken.com/0/public/OHLC с параметрами pair, interval и since
```
https://www.kraken.com/features/api#get-ohlc-data
```
### Разбор возвращаемых данных по каждой бирже:

#### __Binance__ возвращает список списков следующего вида:
```
[
  [
    1575886740000,         // Open time  в микросекундах
    "7465.85000000",       // Open
    "7471.98000000",       // High
    "7465.36000000",       // Low
    "7469.56000000",       // Close
    "25.70697900",         // Volume - объём базовой валюты BTC
    1575886799999,         // Close time в микросекундах
    "192005.89262087",     // Quote asset volume - объём котируемой валюты USD
    326,                   // Number of trades - не требуется
    "14.89451100",         // Taker buy base asset volume - не требуется
    "111259.13678615",     // Taker buy quote asset volume - не требуется
    "0"                    // Ignore. - не требуется
  ],
  [
    ...
  ],
]
```
Порядок данных в массиве - восходящий, от старых к новым.
Параметры запроса:

| Имя  	| Тип  	| Обязательный  	| Описание  	|
|---	|---	|---	|---	|
|  symbol	|  string 	|  да 	|   	|
| interval  	| enum  	|  да 	|   	|
| startTime  	| long  	|  нет 	|   	|
| endTime  	|  long 	|   нет	|   	|
| limit  	|  long 	|  нет 	| Default 500; max 1000.  	|



#### __Hitbtc__ возвращает JSON вида:

```json
[
  {
    "timestamp": "2019-12-09T16:44:00.000Z",
    "open": "7416.81",
    "close": "7417.10",
    "min": "7412.88",
    "max": "7419.35",
    "volume": "2.47167",
    "volumeQuote": "18330.3675566"
  },
  {

  }
]
```
Порядок данных - настраиваемый
Параметры запроса:

| Имя  	| Тип  	| Обязательный  	| Описание  	|
|---	|---	|---	|---	|
|  period	|  string 	|  да 	|   	|
| sort  	| string  	|  да 	|   	|
| from  	| Datetime или Number  	|  нет 	| Interval initial value. If sorting by timestamp is used, then Datetime, otherwise Number of index value.  	|
| till  	|  long 	|   нет	| Interval end value. If sorting by timestamp is used, then Datetime, otherwise Number of index value.  	|
| limit  	|  long 	|  нет 	| Limit of candles . Default value: 100 Max value: 1000  	|
| offset 	|  long 	|  нет 	| Default value: 0  Max value: 100000  	|
