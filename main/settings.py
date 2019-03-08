import os

from decouple import config

try:
    import local_settings
    DEBUG = local_settings.DEBUG
    LOCAL = local_settings.LOCAL
except ImportError:
    DEBUG = False
    LOCAL = False


# Module config
SCHEDULER_IDS = {'index': 'index', 'binance': 'binance'}
CONFIG_MODULES_OPTION_NAME = ['Index activation mode', 'Binance activation mode']
CONFIG_FILE_NAME = 'config.ini'
CONF_PATH = os.path.join(os.path.dirname(__file__), CONFIG_FILE_NAME)


# Heroku config
HEROKU_APP_NAME = 'immense-eyrie-59509'
DATABASE_URL = config('DATABASE_URL') if LOCAL else os.environ['DATABASE_URL']
