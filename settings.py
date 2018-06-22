import os
from decouple import config


try:
    import local_settings
    DEBUG = local_settings.DEBUG
    LOCAL = local_settings.LOCAL
except:
    DEBUG = False
    LOCAL = False

HEROKU_APP_NAME = 'immense-eyrie-59509'

USER_LOGIN = config('USER_LOGIN') if LOCAL else os.environ['USER_LOGIN']
USER_PASS = config('USER_PASS') if LOCAL else os.environ['USER_PASS']
USER_WMID = config('USER_WMID') if LOCAL else os.environ['USER_WMID']
DATABASE_URL = config('DATABASE_URL') if LOCAL else os.environ['DATABASE_URL']
BINANCE_APIKEY = config('BINANCE_APIKEY') if LOCAL else os.environ['BINANCE_APIKEY']
BINANCE_SECRETKEY = config('BINANCE_SECRETKEY') if LOCAL else os.environ['BINANCE_SECRETKEY']
