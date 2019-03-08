import os

from decouple import config

try:
    import local_settings
    DEBUG = local_settings.DEBUG
    LOCAL = local_settings.LOCAL
except ImportError:
    DEBUG = False
    LOCAL = False


# Client config
BINANCE_CLIENT_BALANCE_SYMBOL = {'ETC': 'ETC', 'UTC': 'UTC'}
BINANCE_CLIENT_SIDE = {'BUY': 'BUY', 'SELL': 'SELL'}
BINANCE_CLIENT_ORDER_TYPE = 'LIMIT'
BINANCE_CLIENT_ORDER_OPTIONS = 'GTC'
BINANCE_CLIENT_NEW_ORDER_RESPONSE_TYPE = {'ACK': 'ACK', 'RESULT': 'RESULT', 'FULL': 'FULL'}

# DB config
BINANCE_TABLES = {
    'binance_minimal_sell_price': 'binance_minimal_sell_price',
    'binance_price_stamp': 'binance_price_stamp'
}

# Binance config
BINANCE_APIKEY = config('BINANCE_APIKEY') if LOCAL else os.environ['BINANCE_APIKEY']
BINANCE_SECRETKEY = config('BINANCE_SECRETKEY') if LOCAL else os.environ['BINANCE_SECRETKEY']
BINANCE_API_SYMBOL = 'ETHUSDT'
