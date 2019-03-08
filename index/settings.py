import os

from decouple import config

try:
    import local_settings
    DEBUG = local_settings.DEBUG
    LOCAL = local_settings.LOCAL
except ImportError:
    DEBUG = False
    LOCAL = False


# Index config
USER_LOGIN = config('USER_LOGIN') if LOCAL else os.environ['USER_LOGIN']
USER_PASS = config('USER_PASS') if LOCAL else os.environ['USER_PASS']
USER_WMID = config('USER_WMID') if LOCAL else os.environ['USER_WMID']

# DB config
INDEX_SELL_PRICE_TABLE = 'index_minimal_sell_price'
INDEX_PRICE_STAMP_TABLE = 'index_price_stamp'
