from decouple import config
from requests import request
from settings import BINANCE_PROCENT
from os import path
import time


class BinanceCoreApi:

    def __init__(self, apikey, secretkey, symbol):
        self.apikey = apikey
        self.secretkey = secretkey
        self.symbol = symbol
        # self.type_v = type_v
        # self.side = side
        # self.quantity = quantity
        # self.timeInForce = timeInForce
        # self.price = price
        self.timestamp = str(int(round(time.time() * 1000)))
        self.head = 'https://api.binance.com'
        self.header = {'X-MBX-APIKEY': self.apikey}

    def test_connectivity(self):
        """

        :return: {}
        """
        body = 'api/v1/ping'

        return request('get', path.join(self.head, body)).json()

    def check_server_time(self):
        """

        :return: {"serverTime": 1499827319559}
        """
        body = 'api/v1/time'

        return request('get', path.join(self.head, body)).json()

    def exchange_information(self):
        """

        :return:{
              "timezone": "UTC",
              "serverTime": 1508631584636,
              "rateLimits": [{
                  "rateLimitType": "REQUESTS",
                  "interval": "MINUTE",
                  "limit": 1200
                },
                {
                  "rateLimitType": "ORDERS",
                  "interval": "SECOND",
                  "limit": 10
                },
                {
                  "rateLimitType": "ORDERS",
                  "interval": "DAY",
                  "limit": 100000
                }
              ],
              "exchangeFilters": [],
              "symbols": [{
                "symbol": "ETHBTC",
                "status": "TRADING",
                "baseAsset": "ETH",
                "baseAssetPrecision": 8,
                "quoteAsset": "BTC",
                "quotePrecision": 8,
                "orderTypes": ["LIMIT", "MARKET"],
                "icebergAllowed": false,
                "filters": [{
                  "filterType": "PRICE_FILTER",
                  "minPrice": "0.00000100",
                  "maxPrice": "100000.00000000",
                  "tickSize": "0.00000100"
                }, {
                  "filterType": "LOT_SIZE",
                  "minQty": "0.00100000",
                  "maxQty": "100000.00000000",
                  "stepSize": "0.00100000"
                }, {
                  "filterType": "MIN_NOTIONAL",
                  "minNotional": "0.00100000"
                }]
              }]
            }
        """
        body = 'api/v1/exchangeInfo'

        return request('get', path.join(self.head, body)).json()

    def order_book(self, limit=100):
        """

        :param limit:
        :return:{
                  "lastUpdateId": 1027024,
                  "bids": [
                    [
                      "4.00000000",     // PRICE
                      "431.00000000",   // QTY
                      []                // Ignore.
                    ]
                  ],
                  "asks": [
                    [
                      "4.00000200",
                      "12.00000000",
                      []
                    ]
                  ]
                }
        """
        body = 'api/v1/depth'
        data = {'symbol': self.symbol, 'limit': limit}

        return request('get', path.join(self.head, body), params=data).json()

    def recent_trades_list(self, limit=500):
        """

        :param limit:
        :return: [
                  {
                    "id": 28457,
                    "price": "4.00000100",
                    "qty": "12.00000000",
                    "time": 1499865549590,
                    "isBuyerMaker": true,
                    "isBestMatch": true
                  }
                ]
        """
        body = 'api/v1/trades'
        data = {'symbol': self.symbol, 'limit': limit}

        return request('get', path.join(self.head, body), params=data).json()

    def old_trade_lookup_market_data(self, limit=500, fromId=None):
        """

        :param limit:
        :param fromId:
        :return: [
                  {
                    "id": 28457,
                    "price": "4.00000100",
                    "qty": "12.00000000",
                    "time": 1499865549590,
                    "isBuyerMaker": true,
                    "isBestMatch": true
                  }
                ]
        """
        body = 'api/v1/historicalTrades'
        data = {'symbol': self.symbol, 'limit': limit, 'fromId': fromId}

        return request('get', path.join(self.head, body), params=data, headers=self.header).json()

    def compressed_aggregate_trades_list(self, fromId=None, startTime=None, endTime=None, limit=500):
        """

        :param fromId:
        :param startTime:
        :param endTime:
        :param limit:
        :return: [
                  {
                    "a": 26129,         // Aggregate tradeId
                    "p": "0.01633102",  // Price
                    "q": "4.70443515",  // Quantity
                    "f": 27781,         // First tradeId
                    "l": 27781,         // Last tradeId
                    "T": 1498793709153, // Timestamp
                    "m": true,          // Was the buyer the maker?
                    "M": true           // Was the trade the best price match?
                  }
                ]
        """
        body = 'api/v1/aggTrades'
        data = {'symbol': self.symbol, 'limit': limit, 'fromId': fromId, 'startTime': startTime, 'endTime': endTime}

        return request('get', path.join(self.head, body), params=data).json()

    def kline_candlestick_data(self, interval, limit=None, startTime=None, endTime=None):
        """

        :param interval:
        :param limit:
        :param startTime:
        :param endTime:
        :return:[
                  [
                    1499040000000,      // Open time
                    "0.01634790",       // Open
                    "0.80000000",       // High
                    "0.01575800",       // Low
                    "0.01577100",       // Close
                    "148976.11427815",  // Volume
                    1499644799999,      // Close time
                    "2434.19055334",    // Quote asset volume
                    308,                // Number of trades
                    "1756.87402397",    // Taker buy base asset volume
                    "28.46694368",      // Taker buy quote asset volume
                    "17928899.62484339" // Ignore
                  ]
                ]
        """
        body = 'api/v1/klines'
        data = {'symbol': self.symbol, 'limit': limit, 'interval': interval, 'startTime': startTime, 'endTime': endTime}

        return request('get', path.join(self.head, body), params=data).json()

if __name__=='__main__':
    o = BinanceCoreApi(
        config('BINANCE_APIKEY'),
        config('BINANCE_SECRETKEY'),
        'ETHBTC'
    )
    print(o.kline_candlestick_data('1M'))
