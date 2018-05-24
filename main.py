import core_api
from opirations_conditions import TradingOpirations
from index_trading import IndexTrading
from db_operations import Connection
from decouple import config
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime, timedelta


sched = BlockingScheduler()


@sched.scheduled_job('interval', minutes=1)
def clock_sched():
    index_connection = core_api.IndexInfo(config('USER_LOGIN'), config('USER_PASS'), config('USER_WMID'))
    instrument_info = index_connection.get_eth_status()
    db_connection = Connection()

    date_time_now = datetime.now()
    db_connection.set_timestamp(date_time_now, instrument_info['price'])

    timestamp_data = db_connection.get_timestamp_data().fetchall()

    ids_for_delete = ()
    occur_count = {}  # list of amount of occur
    max_count = [-1, -1]  # largest most occur price
    prior_max_count = [-1, -1]  # lowest most occur price


    for i in timestamp_data:
        if i[1] + timedelta(hours=24) <= date_time_now:
            ids_for_delete = ids_for_delete + (i[0],)
            timestamp_data.remove(i)
        else:
            if occur_count.get(i[2], None):
                occur_count[i[2]] += 1
            else:
                occur_count[i[2]] = 1
            if occur_count[i[2]] > max_count[1] or (occur_count[i[2]] == max_count[1] and max_count[0] < i[2]):
                prior_max_count = max_count if max_count[0] != prior_max_count[0] else prior_max_count
                max_count = [i[2], occur_count[i[2]]]

    occur_count.pop(max_count[0])

    for i in occur_count:
        if occur_count[i] > prior_max_count[1] or (occur_count[i] == prior_max_count[1] and prior_max_count[0] < i):
            prior_max_count = [i, occur_count[i]]

    if ids_for_delete:
        db_connection.delete_timestamp_data(ids_for_delete)

sched.start()

# user_info = index_connection.get_balance()
# my_offer_list = index_connection.get_offer_my()
#
# for i in my_offer_list:
#     if i:
#         index_connection.delete_offer(i['offerid'])
#
# db_data = next(db_connection.get_index_state())
# trading_percentage = IndexTrading(
#     db_data[1],
#     db_data[2],
#     db_data[3],
#     instrument_info['price']
# )
# trading = TradingOpirations(trading_percentage.sell_buy_conditions(), user_info, instrument_info['price'], index_connection.get_offer_list())
#
# db_connection.index_state_update(
#     instrument_info['price'],
#     trading_percentage.get_trade_state_percent(),
#     trading_percentage.actual_change_percent
# )
#
# sell = trading.sell()
# buy = trading.buy()
#
# if sell:
#     index_connection.set_offer(sell['count'], sell['price'], is_bid=False)
# if buy:
#     print('buy')
#     print(index_connection.set_offer(buy['count'], buy['price']))


