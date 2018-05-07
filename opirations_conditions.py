import settings
import functools


class TradingOpirations:

    def __init__(self, instrument_info, user_info, my_offer_list):
        self.buy_price = instrument_info['price'] - settings.PERCENT_BUY  # price for buy
        self.sell_price = instrument_info['price'] + settings.PERCENT_SELL  # price for sale
        self.user_wmz = user_info['balance']['wmz']  # amount WMZ
        self.user_notes = user_info['portfolio'][0]['notes']  # amount ETH notes
        self.selling_notes = functools.reduce(lambda x, y: x+y, (i['notes'] for i in my_offer_list if i['kind'] == 0), 0)

    def sell(self):
        rest_notes = self.user_notes - self.selling_notes

        if rest_notes > settings.NOTES_AMOUNT:
            return {
                'count': settings.NOTES_AMOUNT,
                'price': self.sell_price,
            }
        return {
            'count': rest_notes,
            'price': self.sell_price,
        }

    def buy(self):

        if self.user_wmz >= settings.NOTES_AMOUNT * self.buy_price:
            return {
                'count': settings.NOTES_AMOUNT,
                'price': self.buy_price,
            }
        return {
            'count': int(self.user_wmz / self.buy_price),
            'price': self.buy_price,
        }