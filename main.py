import core_api
import time
import logging
import sys
from db_operations import Connection
from core_binance_api import BinanceCoreApi
from operations import Operations
from decouple import config
from datetime import datetime


log = logging.getLogger()
log.setLevel(logging.DEBUG)
chanel = logging.StreamHandler(sys.stdout)
chanel.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
chanel.setFormatter(formatter)
log.addHandler(chanel)


def delay_func(func, *args, **kwargs):
    delay = 1

    while True:
        if not kwargs:
            result = func() if not args else func(*args)
        else:
            result = func(*args, **kwargs)
        if isinstance(result, str):
            time.sleep(delay)
        else:
            break
        delay += 1

    return result


while True:
    try:
        index_connection = core_api.IndexInfo(config('USER_LOGIN'), config('USER_PASS'), config('USER_WMID'))
        instrument_info = delay_func(index_connection.get_eth_status)
        db_connection = Connection()
        user_info = delay_func(index_connection.get_balance)
        my_offer_list = delay_func(index_connection.get_offer_my)
        operations = Operations()

        date_time_now = datetime.now()
        db_connection.set_timestamp(date_time_now, instrument_info['price'], 'index_price_stamp')

        timestamp_data = db_connection.get_timestamp_data('index_price_stamp').fetchall()
        largest_prices = operations.largest_prices(timestamp_data)

        if largest_prices['ids']:
            db_connection.delete_timestamp_data(largest_prices['ids'], 'index_price_stamp')

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
        list_off = delay_func(index_connection.get_offer_list)

        for i in list_off:
            if i['kind'] == 0:
                temp = i['price'] if not temp or temp > i['price'] else temp

        average_price = new_average_price if new_average_price else price_data[0]
        offerid = next((i for i in my_offer_list if i['kind'] == 0), None)
        if offerid:
            res = delay_func(index_connection.delete_offer, offerid['offerid'])
        if average_price < temp:
            res = delay_func(index_connection.set_offer, user_info['portfolio'][0]['notes'], temp - 0.001, is_bid=False)
        else:
            res = delay_func(index_connection.set_offer, user_info['portfolio'][0]['notes'], average_price, is_bid=False)

        if largest_prices['max'][0] >= instrument_info['price'] <= largest_prices['prior_max'][0]:
            temp = None
            for i in list_off:
                if i['kind'] == 1:
                    temp = i['price'] if not temp or temp < i['price'] else temp
            offerid = next((i for i in my_offer_list if i['kind'] == 1), None)
            if offerid:
                res = delay_func(index_connection.delete_offer, offerid['offerid'])
            if temp < instrument_info['price']:
                price = temp + 0.001
                buy_amount = int(user_info['balance']['wmz'] / price)
                res = delay_func(index_connection.set_offer, buy_amount, price)
                if not res['code']:
                    db_connection.set_price_data(average_price, price, buy_amount)
            else:
                price = instrument_info['price'] + 0.001
                buy_amount = int(user_info['balance']['wmz'] / price)
                res = delay_func(index_connection.set_offer, buy_amount, price)
                if not res['code']:
                    db_connection.set_price_data(average_price, price, buy_amount)
        else:
            (db_connection.set_price_data(average_price, i['price'], i['notes'])for i in list_off if i['kind'] == 1)


        ####################################### Binance logic ##################################################################

        binance_connection = BinanceCoreApi(config('BINANCE_APIKEY'), config('BINANCE_SECRETKEY'), 'ETHUSDT')
        symbol_info = binance_connection.symbol_price_ticker()
        db_connection = Connection()
        date_time_now = datetime.now()
        operations = Operations()

        db_connection.set_timestamp(date_time_now, symbol_info['price'], 'binance_price_stamp')

        list_timestampe = db_connection.get_timestamp_data('binance_price_stamp').fetchall()
        largest_prices = operations.largest_prices(list_timestampe)

        if largest_prices['ids']:
            db_connection.delete_timestamp_data(largest_prices['ids'], 'binance_price_stamp')

        time.sleep(60)
    except:
        time.sleep(60)
