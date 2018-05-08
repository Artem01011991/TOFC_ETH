# import core_api
# import opirations_conditions
# import settings
# from decouple import config
# from apscheduler.schedulers.blocking import BlockingScheduler
#
#
# sched = BlockingScheduler()
#
#
# @sched.scheduled_job('interval', minutes=1)
# def clock_sched():
#     index_connection = core_api.IndexInfo(config('USER_LOGIN'), config('USER_PASS'), config('USER_WMID'))
#     user_info = index_connection.get_balance()
#     instrument_info = index_connection.get_eth_status()
#     my_offer_list = index_connection.get_offer_my()
#
#     trading = opirations_conditions.TradingOpirations(instrument_info, user_info, my_offer_list)
#
#     sell_condition = trading.sell()
#     buy_condition = trading.buy()
#
#     offer_for_delete = (
#         i['offerid'] for i in my_offer_list
#         if (i['kind'] == 0 and (
#                    sell_condition['price'] + settings.DELETE_OFFER_SELL_CONDITION < i['price']
#                    or sell_condition['price'] > i['price']))
#            or (i['kind'] == 1 and (
#             buy_condition['price'] > i['price'] + settings.DELETE_OFFER_BUY_CONDITION
#             or buy_condition['price'] < i['price'])))
#
#     if offer_for_delete:
#         for i in offer_for_delete:
#             index_connection.delete_offer(i)
#
#     if sell_condition['count'] and not next((i for i in my_offer_list if i['price'] == sell_condition['price'] and i['kind'] == 0), None):  # sell operation
#         index_connection.set_offer(sell_condition['count'], sell_condition['price'], is_bid=False)
#
#     if buy_condition['count'] and not next((i for i in my_offer_list if i['price'] == buy_condition['price'] and i['kind'] == 1), None):  # buy operation
#         index_connection.set_offer(buy_condition['count'], buy_condition['price'])
#
#
# sched.start()
