import os
from decouple import config


try:
    import local_settings
    DEBUG = local_settings.DEBUG
    LOCAL = local_settings.LOCAL
except:
    DEBUG = False
    LOCAL = False

# Heroku settings
HEROKU_APP_NAME = 'immense-eyrie-59509'
DATABASE_URL = config('DATABASE_URL') if LOCAL else os.environ['DATABASE_URL']

# Index settings
USER_LOGIN = config('USER_LOGIN') if LOCAL else os.environ['USER_LOGIN']
USER_PASS = config('USER_PASS') if LOCAL else os.environ['USER_PASS']
USER_WMID = config('USER_WMID') if LOCAL else os.environ['USER_WMID']

# Binance settings
BINANCE_APIKEY = config('BINANCE_APIKEY') if LOCAL else os.environ['BINANCE_APIKEY']
BINANCE_SECRETKEY = config('BINANCE_SECRETKEY') if LOCAL else os.environ['BINANCE_SECRETKEY']
BINANCE_API_SYMBOL = 'ETHUSDT'

# DB settings
BINANCE_TABLES = {'binance_minimal_sell_price': 'binance_minimal_sell_price', 'binance_price_stamp': 'binance_price_stamp'}
INDEX_SELL_PRICE_TABLE = 'index_minimal_sell_price'
INDEX_PRICE_STAMP_TABLE = 'index_price_stamp'

# Client settings
BINANCE_CLIENT_BALANCE_SYMBOL = {'ETC': 'ETC', 'UTC': 'UTC'}
BINANCE_CLIENT_SIDE = {'BUY': 'BUY', 'SELL': 'SELL'}
BINANCE_CLIENT_ORDER_TYPE = 'LIMIT'
BINANCE_CLIENT_ORDER_OPTIONS = 'GTC'
BINANCE_CLIENT_NEW_ORDER_RESPONSE_TYPE = {'ACK': 'ACK', 'RESULT': 'RESULT', 'FULL': 'FULL'}
