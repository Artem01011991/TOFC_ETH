from TOFC_ETH.binance import settings
from TOFC_ETH.binance.api import BinanceCoreApi
from TOFC_ETH.binance.opirations import BinanceOperationsClass
from TOFC_ETH.main.db_operations import Connection


def main_binance():
    binance_api_connection = BinanceCoreApi(
        settings.BINANCE_APIKEY,
        settings.BINANCE_SECRETKEY,
        settings.BINANCE_API_SYMBOL,
        settings.DEBUG
    )
    symbol_info = binance_api_connection.symbol_price_ticker()
    db_connection = Connection()

    # set new timestamp
    db_connection.set_timestamp(symbol_info['price'], settings.BINANCE_TABLES['binance_price_stamp'])

    # get timestamp data
    list_timestampe = db_connection.get_timestamp_data(settings.BINANCE_TABLES['binance_price_stamp']).fetchall()

    # get current buy and sell orders info
    client_orders = binance_api_connection.current_open_orders()
    buy_order = next((i for i in client_orders if i['side'] == 'BUY'), None)
    next((i for i in client_orders if i['side'] == 'SELL'), None)  # sell_order

    # logic for minimal sell price
    client_data = binance_api_connection.account_information()
    client_symbol_balance = next(
        (i for i in client_data['balances'] if i['asset'] == settings.BINANCE_CLIENT_BALANCE_SYMBOL['ETH']),
        None
    )
    db_minimal_price = db_connection.get_price_data(settings.BINANCE_TABLES['binance_minimal_sell_price']).fetchall()

    if db_minimal_price:
        if client_symbol_balance and buy_order and db_minimal_price[2] != buy_order['executedQty']:
            operations = BinanceOperationsClass(
                list_timestampe,  # for frequency range determination
                (buy_order['executedQty'], buy_order['price'],),
                (client_symbol_balance['locked'], db_minimal_price[0],)
            )
    else:
        operations = BinanceOperationsClass(list_timestampe)  # If no minimal price in database.

    # delete deprecated timestamps
    if operations.timestamp_ids:
        db_connection.delete_timestamp_data(operations.timestamp_ids, settings.BINANCE_TABLES['binance_price_stamp'])

    # buy logic
    # checking for allowable price to buy
    if operations.max_price >= symbol_info['price'] >= operations.prior_max_price:
        client_utc = next(
            (i for i in client_data['balances'] if i['asset'] == settings.BINANCE_CLIENT_BALANCE_SYMBOL['UTC']),
            None
        )
        if client_utc:
            binance_api_connection.new_order(
                settings.BINANCE_CLIENT_SIDE['BUY'],
                settings.BINANCE_CLIENT_ORDER_TYPE,
                settings.BINANCE_CLIENT_ORDER_OPTIONS,
                client_utc['free'] / symbol_info['price'],
                symbol_info['price'],
                newOrderRespType=settings.BINANCE_CLIENT_NEW_ORDER_RESPONSE_TYPE['RESULT']
            )

    # sell logic
    if db_minimal_price[0] < symbol_info['price']:
        client_symbol_amount = next(
            (i for i in client_data['balances'] if i['asset'] == settings.BINANCE_CLIENT_BALANCE_SYMBOL['ETH']),
            None
        )
        if client_symbol_amount:
            binance_api_connection.new_order(
                settings.BINANCE_CLIENT_SIDE['SELL'],
                settings.BINANCE_CLIENT_ORDER_TYPE,
                settings.BINANCE_CLIENT_ORDER_OPTIONS,
                client_symbol_amount['free'],
                symbol_info['price'],
                newOrderRespType=settings.BINANCE_CLIENT_NEW_ORDER_RESPONSE_TYPE['RESULT']
            )
