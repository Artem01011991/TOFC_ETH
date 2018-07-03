import core_api
import time
import settings
from db_operations import Connection
from core_binance_api import BinanceCoreApi
from operations import OperationsBaseClass, BinanceOpirationsClass


def delay_func(func, *args, **kwargs):
    delay = 1
    delay_inc = 3

    while True:
        if not kwargs:
            result = func() if not args else func(*args)
        else:
            result = func(*args, **kwargs)
        if isinstance(result, str):
            time.sleep(delay)
        else:
            break
        delay += delay_inc

    return result


def main_index():
    index_connection = core_api.IndexInfo(settings.USER_LOGIN, settings.USER_PASS, settings.USER_WMID)
    instrument_info = delay_func(index_connection.get_eth_status)
    db_connection = Connection()
    user_info = delay_func(index_connection.get_balance)
    my_offer_list = delay_func(index_connection.get_offer_my)
    operations = OperationsBaseClass()

    db_connection.set_timestamp(instrument_info['price'], settings.INDEX_PRICE_STAMP_TABLE)

    timestamp_data = db_connection.get_timestamp_data(settings.INDEX_PRICE_STAMP_TABLE).fetchall()
    largest_prices = operations.largest_prices(timestamp_data)

    if largest_prices['ids']:
        db_connection.delete_timestamp_data(largest_prices['ids'], settings.INDEX_PRICE_STAMP_TABLE)

    price_data = next(db_connection.get_price_data(settings.INDEX_SELL_PRICE_TABLE))
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
                db_connection.update_price_data(average_price, price, buy_amount)
        else:
            price = instrument_info['price'] + 0.001
            buy_amount = int(user_info['balance']['wmz'] / price)
            res = delay_func(index_connection.set_offer, buy_amount, price)
            if not res['code']:
                db_connection.update_price_data(average_price, price, buy_amount)
    else:
        (db_connection.update_price_data(average_price, i['price'], i['notes']) for i in list_off if i['kind'] == 1)


def main_binance():
    # binance_api_connection = BinanceCoreApi(settings.BINANCE_APIKEY, settings.BINANCE_SECRETKEY, 'ETHUSDT')
    # symbol_info = binance_api_connection.symbol_price_ticker()
    # db_connection = Connection()
    # date_time_now = datetime.now()
    # operations = Operations()
    #
    # db_connection.set_timestamp(date_time_now, symbol_info['price'], 'binance_price_stamp')
    #
    # list_timestampe = db_connection.get_timestamp_data('binance_price_stamp').fetchall()
    # largest_prices = operations.largest_prices(list_timestampe)
    #
    # if largest_prices['ids']:
    #     db_connection.delete_timestamp_data(largest_prices['ids'], 'binance_price_stamp')
    binance_api_connection = BinanceCoreApi(settings.BINANCE_APIKEY, settings.BINANCE_SECRETKEY, 'ETHUSDT')
    symbol_info = binance_api_connection.symbol_price_ticker()

    db_connection = Connection()
    db_connection.set_timestamp(symbol_info['price'], settings.BINANCE_PRICE_STAMP_TABLE)
    list_timestampe = db_connection.get_timestamp_data(settings.BINANCE_PRICE_STAMP_TABLE).fetchall()

    client_orders = binance_api_connection.current_open_orders()
    buy_order = next((i for i in client_orders if i['side'] == 'BUY'), None)
    sell_order = next((i for i in client_orders if i['side'] == 'SELL'), None)

    client_data = binance_api_connection.account_information()
    db_minimal_price = db_connection.get_price_data(settings.BINANCE_SELL_PRICE_TABLE).fetchall()
    if db_minimal_price:
        if buy_order and db_minimal_price[2] != buy_order['executedQty']:

            operations = BinanceOpirationsClass(
                list_timestampe,
                (buy_order['executedQty'], buy_order['price'],),
                (, db_minimal_price[0],)
            )
    else:
        operations = BinanceOpirationsClass(list_timestampe)

    if operations.timestamp_ids:
        db_connection.delete_timestamp_data(operations.timestamp_ids, settings.BINANCE_PRICE_STAMP_TABLE)

