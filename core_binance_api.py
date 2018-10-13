from requests import request
from os import path
from TOFC_ETH import settings
import time
import hmac
import hashlib


class BinanceCoreApi:

    def __init__(self, apikey, secretkey, symbol, debug_mode=False):
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
        self.debug_mode = debug_mode

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

    def hr24_ticker_price_change_statistics(self):
        """

        :return: {
                  "symbol": "BNBBTC",
                  "priceChange": "-94.99999800",
                  "priceChangePercent": "-95.960",
                  "weightedAvgPrice": "0.29628482",
                  "prevClosePrice": "0.10002000",
                  "lastPrice": "4.00000200",
                  "lastQty": "200.00000000",
                  "bidPrice": "4.00000000",
                  "askPrice": "4.00000200",
                  "openPrice": "99.00000000",
                  "highPrice": "100.00000000",
                  "lowPrice": "0.10000000",
                  "volume": "8913.30000000",
                  "quoteVolume": "15.30000000",
                  "openTime": 1499783499040,
                  "closeTime": 1499869899040,
                  "fristId": 28385,   // First tradeId
                  "lastId": 28460,    // Last tradeId
                  "count": 76         // Trade count
                }
        """
        body = 'api/v1/ticker/24hr'

        return request('get', path.join(self.head, body), params={'symbol': self.symbol}).json()

    def symbol_price_ticker(self):
        """

        :return: {
                  "symbol": "LTCBTC",
                  "price": "4.00000200"
                }
        """
        body = 'api/v3/ticker/price'

        return request('get', path.join(self.head, body), params={'symbol': self.symbol}).json()

    def symbol_order_book_ticker(self):
        """

        :return: {
                  "symbol": "LTCBTC",
                  "bidPrice": "4.00000000",
                  "bidQty": "431.00000000",
                  "askPrice": "4.00000200",
                  "askQty": "9.00000000"
                }
        """
        body = 'api/v3/ticker/bookTicker'

        return request('get', path.join(self.head, body), params={'symbol': self.symbol}).json()

    def new_order(
            self,
            side,
            type,
            timeInForce,
            quantity,
            price,
            stopPrice=0.0,
            icebergQty=0.0,
            newOrderRespType={},
    ):
        """

        :param side:
                    BUY
                    SELL

        :param type:
                    LIMIT
                    MARKET
                    STOP_LOSS
                    STOP_LOSS_LIMIT
                    TAKE_PROFIT
                    TAKE_PROFIT_LIMIT
                    LIMIT_MAKER

        :param timeInForce:
                            GTC
                            IOC
                            FOK

        :param quantity:
        :param price:
        :param stopPrice: Used with STOP_LOSS, STOP_LOSS_LIMIT, TAKE_PROFIT, and TAKE_PROFIT_LIMIT orders.
        :param icebergQty:  Used with LIMIT, STOP_LOSS_LIMIT, and TAKE_PROFIT_LIMIT to create an iceberg order.
        :param newOrderRespType: Set the response JSON. ACK, RESULT, or FULL; default: RESULT.
        :return:
                Response ACK:

                {
                  "symbol": "BTCUSDT",
                  "orderId": 28,
                  "clientOrderId": "6gCrw2kRUAF9CvJDGP16IP",
                  "transactTime": 1507725176595
                }

                Response RESULT:

                {
                  "symbol": "BTCUSDT",
                  "orderId": 28,
                  "clientOrderId": "6gCrw2kRUAF9CvJDGP16IP",
                  "transactTime": 1507725176595,
                  "price": "0.00000000",
                  "origQty": "10.00000000",
                  "executedQty": "10.00000000",
                  "status": "FILLED",
                  "timeInForce": "GTC",
                  "type": "MARKET",
                  "side": "SELL"
                }

                Response FULL:

                {
                  "symbol": "BTCUSDT",
                  "orderId": 28,
                  "clientOrderId": "6gCrw2kRUAF9CvJDGP16IP",
                  "transactTime": 1507725176595,
                  "price": "0.00000000",
                  "origQty": "10.00000000",
                  "executedQty": "10.00000000",
                  "status": "FILLED",
                  "timeInForce": "GTC",
                  "type": "MARKET",
                  "side": "SELL",
                  "fills": [
                    {
                      "price": "4000.00000000",
                      "qty": "1.00000000",
                      "commission": "4.00000000",
                      "commissionAsset": "USDT"
                    },
                    {
                      "price": "3999.00000000",
                      "qty": "5.00000000",
                      "commission": "19.99500000",
                      "commissionAsset": "USDT"
                    },
                    {
                      "price": "3998.00000000",
                      "qty": "2.00000000",
                      "commission": "7.99600000",
                      "commissionAsset": "USDT"
                    },
                    {
                      "price": "3997.00000000",
                      "qty": "1.00000000",
                      "commission": "3.99700000",
                      "commissionAsset": "USDT"
                    },
                    {
                      "price": "3995.00000000",
                      "qty": "1.00000000",
                      "commission": "3.99500000",
                      "commissionAsset": "USDT"
                    }
                  ]
                }
        """
        data = {
            'symbol': self.symbol,
            'side': side,
            'type': type,
            'timeInForce': timeInForce,
            'quantity': quantity,
            'price': price,
            # 'stopPrice': stopPrice,
            # 'icebergQty': icebergQty,
            # 'newOrderRespType': newOrderRespType,
            'timestamp': self.timestamp,
        }

        if not self.debug_mode:
            body = 'api/v3/order'
            # body = 'api/v3/order/test'
            signature = hmac.new(
                    self.secretkey.encode(),
                    '&'.join(['{k}={v}'.format(k=k, v=v) for k, v in data.items()]).encode(),
                    digestmod=hashlib.sha256
                ).hexdigest()

            data.update({'signature': signature})

            return request('post', path.join(self.head, body), data=data, headers=self.header).json()
        return data

    def cancel_order(self, orderId=None):
        """

        :param orderId:
        :return:
                        {
                  "symbol": "LTCBTC",
                  "origClientOrderId": "myOrder1",
                  "orderId": 1,
                  "clientOrderId": "cancelMyOrder1"
                }
        """
        body = 'api/v3/order'
        data = {'symbol': self.symbol, 'timestamp': self.timestamp, 'orderId': orderId}
        signature = hmac.new(
            settings.BINANCE_SECRETKEY.encode(),
            '&'.join(['{k}={v}'.format(k=k, v=v) for k, v in data.items()]).encode(),
            digestmod=hashlib.sha256
        ).hexdigest()

        data.update({'signature': signature})

        return request('delete', path.join(self.head, body), data=data, headers=self.header).json()

    def current_open_orders(self):
        """

        :return: [
                  {
                    "symbol": "LTCBTC",
                    "orderId": 1,
                    "clientOrderId": "myOrder1",
                    "price": "0.1",
                    "origQty": "1.0",
                    "executedQty": "0.0",
                    "status": "NEW",
                    "timeInForce": "GTC",
                    "type": "LIMIT",
                    "side": "BUY",
                    "stopPrice": "0.0",
                    "icebergQty": "0.0",
                    "time": 1499827319559,
                    "isWorking": trueO
                  }
                ]
        """
        body = 'api/v3/openOrders'
        data = {'symbol': self.symbol, 'timestamp': self.timestamp}
        signature = hmac.new(
            settings.BINANCE_SECRETKEY.encode(),
            '&'.join(['{k}={v}'.format(k=k, v=v) for k, v in data.items()]).encode(),
            digestmod=hashlib.sha256
        ).hexdigest()

        data.update({'signature': signature})

        return request('get', path.join(self.head, body), params=data, headers=self.header).json()

    def account_information(self):
        """

        :return:
                {
                  "makerCommission": 15,
                  "takerCommission": 15,
                  "buyerCommission": 0,
                  "sellerCommission": 0,
                  "canTrade": true,
                  "canWithdraw": true,
                  "canDeposit": true,
                  "updateTime": 123456789,
                  "balances": [
                    {
                      "asset": "BTC",
                      "free": "4723846.89208129",
                      "locked": "0.00000000"
                    },
                    {
                      "asset": "LTC",
                      "free": "4763368.68006011",
                      "locked": "0.00000000"
                    }
                  ]
                }
        """
        body = 'api/v3/account'
        data = {'timestamp': self.timestamp}
        signature = hmac.new(
            settings.BINANCE_SECRETKEY.encode(),
            '&'.join(['{k}={v}'.format(k=k, v=v) for k, v in data.items()]).encode(),
            digestmod=hashlib.sha256
        ).hexdigest()

        data.update({'signature': signature})

        return request('get', path.join(self.head, body), params=data, headers=self.header).json()

    def account_trade_list(self):
        """

        :return:
                [
                  {
                    "id": 28457,
                    "orderId": 100234,
                    "price": "4.00000100",
                    "qty": "12.00000000",
                    "commission": "10.10000000",
                    "commissionAsset": "BNB",
                    "time": 1499865549590,
                    "isBuyer": true,
                    "isMaker": false,
                    "isBestMatch": true
                  }
                ]
        """
        body = 'api/v3/myTrades'
        data = {'symbol': self.symbol, 'timestamp': self.timestamp}
        signature = hmac.new(
            settings.BINANCE_SECRETKEY.encode(),
            '&'.join(['{k}={v}'.format(k=k, v=v) for k, v in data.items()]).encode(),
            digestmod=hashlib.sha256
        ).hexdigest()

        data.update({'signature': signature})

        return request('get', path.join(self.head, body), params=data, headers=self.header).json()
