import core_api
import time
from opirations_conditions import TradingOpirations
from index_trading import IndexTrading
from db_operations import Connection
from core_binance_api import BinanceCoreApi
from apscheduler.schedulers.blocking import BlockingScheduler
from decouple import config
from datetime import datetime, timedelta


sched = BlockingScheduler()


@sched.scheduled_job('interval', minutes=1)
def clock_sched():
    index_connection = core_api.IndexInfo(config('USER_LOGIN'), config('USER_PASS'), config('USER_WMID'))

    while True:
        instrument_info = index_connection.get_eth_status()
        if isinstance(instrument_info, str):
            time.sleep(1)
        else:
            break

    db_connection = Connection()

    while True:
        user_info = index_connection.get_balance()
        if isinstance(user_info, str):
            time.sleep(1)
        else:
            break

    while True:
        my_offer_list = index_connection.get_offer_my()
        if isinstance(my_offer_list, str):
            time.sleep(1)
        else:
            break

    date_time_now = datetime.now()
    db_connection.set_timestamp(date_time_now, instrument_info['price'], 'index_price_stamp')

    timestamp_data = db_connection.get_timestamp_data('index_price_stamp').fetchall()

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

    if max_count[0] < prior_max_count[0]:
        max_count[0], prior_max_count[0] = prior_max_count[0], max_count[0]

    if ids_for_delete:
        db_connection.delete_timestamp_data(ids_for_delete, 'index_price_stamp')

    price_data = next(db_connection.get_price_data())
    new_average_price = None
    buy_offer = next((i for i in my_offer_list if i['kind'] == 1), None)
    if not buy_offer or buy_offer['notes'] < price_data[2]:
        buy_offer_notes = buy_offer['notes'] if buy_offer else 0
        bouth_notes_amount = price_data[2] - buy_offer_notes
        prior_price_notes = user_info['portfolio'][0]['notes'] - bouth_notes_amount
        sum_prior_price = prior_price_notes * price_data[0]
        sum_price_new = bouth_notes_amount * price_data[1]
        new_average_price = (sum_price_new + sum_prior_price) / user_info['portfolio'][0]['notes']

    temp = None

    while True:
        list_off = index_connection.get_offer_list()
        if isinstance(list_off, str):
            time.sleep(1)
        else:
            break

    for i in list_off:
        if i['kind'] == 0:
            temp = i['price'] if not temp or temp > i['price'] else temp

    average_price = new_average_price if new_average_price else price_data[0]
    offerid = next((i for i in my_offer_list if i['kind'] == 0), None)
    if offerid:
        while True:
            res = index_connection.delete_offer(offerid['offerid'])
            if isinstance(res, str):
                time.sleep(1)
            else:
                break
    if average_price < temp:
        while True:
            res = index_connection.set_offer(user_info['portfolio'][0]['notes'], temp - 0.001, is_bid=False)
            if isinstance(res, str):
                time.sleep(1)
            else:
                break
    else:
        while True:
            res = index_connection.set_offer(user_info['portfolio'][0]['notes'], average_price, is_bid=False)
            if isinstance(res, str):
                time.sleep(1)
            else:
                break

    if max_count[0] >= instrument_info['price'] <= prior_max_count[0]:
        temp = None
        for i in list_off:
            if i['kind'] == 1:
                temp = i['price'] if not temp or temp < i['price'] else temp
        offerid = next((i for i in my_offer_list if i['kind'] == 1), None)
        if offerid:
            while True:
                res = index_connection.delete_offer(offerid['offerid'])
                if isinstance(res, str):
                    time.sleep(1)
                else:
                    break
        if temp < instrument_info['price']:
            price = temp + 0.001
            buy_amount = int(user_info['balance']['wmz'] / price)
            while True:
                res = index_connection.set_offer(buy_amount, price)
                if isinstance(res, str):
                    time.sleep(1)
                else:
                    break
            if not res['code']:
                db_connection.set_price_data(average_price, price, buy_amount)
        else:
            price = instrument_info['price'] + 0.001
            buy_amount = int(user_info['balance']['wmz'] / price)
            while True:
                res = index_connection.set_offer(buy_amount, price)
                if isinstance(res, str):
                    time.sleep(1)
                else:
                    break
            if not res['code']:
                db_connection.set_price_data(average_price, price, buy_amount)
    else:
        (db_connection.set_price_data(average_price, i['price'], i['notes'])for i in list_off if i['kind'] == 1)


    ####################################### Binance logic ##################################################################

    binance_connection = BinanceCoreApi(config('BINANCE_APIKEY'), config('BINANCE_SECRETKEY'), 'ETHUSDT')
    symbol_info = binance_connection.symbol_price_ticker()

    db_connection.set_timestamp(date_time_now, symbol_info['price'], 'binance_price_stamp')

    list_timestampe = db_connection.get_timestamp_data('binance_price_stamp')
    ids_for_delete = ()
    for i in list_timestampe:
        if i[1] + timedelta(hours=24) <= date_time_now:
            ids_for_delete = ids_for_delete + (i[0],)
            list_timestampe.remove(i)

    if ids_for_delete:
        db_connection.delete_timestamp_data(ids_for_delete, 'binance_price_stamp')


sched.start()


# user_info = index_connection.get_balance()
#
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


