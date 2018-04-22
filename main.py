import core_api
from decouple import config

obj = core_api.IndexInfo(config('USER_LOGIN'), config('USER_PASS'), config('USER_WMID'))
print(obj.get_eth_status())
