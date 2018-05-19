import core_api
from opirations_conditions import TradingOpirations
from index_trading import IndexTrading
from db_operations import Connection
from decouple import config
from apscheduler.schedulers.blocking import BlockingScheduler


sched = BlockingScheduler()


# @sched.scheduled_job('interval', minutes=1)
# def clock_sched():
index_connection = core_api.IndexInfo(config('USER_LOGIN'), config('USER_PASS'), config('USER_WMID'))
user_info = index_connection.get_balance()
instrument_info = index_connection.get_eth_status()
my_offer_list = index_connection.get_offer_my()

for i in my_offer_list:
    if i:
        index_connection.delete_offer(i['offerid'])

db_connection = Connection()
db_data = next(db_connection.get_index_state())
trading_percentage = IndexTrading(
    db_data[1],
    db_data[2],
    db_data[3],
    instrument_info['price']
)
trading = TradingOpirations(trading_percentage.sell_buy_conditions(), user_info, instrument_info['price'], index_connection.get_offer_list())

db_connection.index_state_update(
    instrument_info['price'],
    trading_percentage.get_trade_state_percent(),
    trading_percentage.actual_change_percent
)

sell = trading.sell()
buy = trading.buy()

if sell:
    index_connection.set_offer(sell['count'], sell['price'], is_bid=False)
if buy:
    print('buy')
    print(index_connection.set_offer(buy['count'], buy['price']))

# sched.start()
