import ETH_state
from decouple import config

obj = ETH_state.IndexInfo(config('USER_LOGIN'), config('USER_PASS'), config('USER_WMID'))
print(obj.get_eth_status())
