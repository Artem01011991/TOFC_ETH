import core_api
from decouple import config
from opirations_conditions import sell, buy
from db_operations import MySqlConnection


index_connection = core_api.IndexInfo(config('USER_LOGIN'), config('USER_PASS'), config('USER_WMID'))
user_info = index_connection.get_balance()
instrument_info = index_connection.get_eth_status()
sell_condition = sell(user_info, instrument_info)
buy_condition = buy(user_info, instrument_info)

if sell_condition and not MySqlConnection(sell_condition['price'], False).exist():
    status = index_connection.set_offer(sell_condition['count'], sell_condition['price'], is_bid=False)

    if not status['value']['Code']:
        MySqlConnection(sell_condition['price'], False, notes=sell_condition['count'], offerID=status['value']['OfferID']).write()

if buy_condition and not MySqlConnection(buy_condition['price'], True).exist():
    status = index_connection.set_offer(buy_condition['count'], buy_condition['price'])

    if not status['value']['Code']:
        MySqlConnection(buy_condition['price'], True, notes=buy_condition['count'], offerID=status['value']['OfferID']).write()
