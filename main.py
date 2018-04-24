import core_api
from decouple import config


index_conection = core_api.IndexInfo(config('USER_LOGIN'), config('USER_PASS'), config('USER_WMID'))
user_info = index_conection.get_balance()
instrument_info = index_conection.get_eth_status()
