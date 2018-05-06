import settings
import functools


def sell(user_info, instrument_info):
    user_notes = user_info['portfolio'][0]['notes']  # amount ETH notes
    price = instrument_info['price'] + settings.PERCENT_SELL  # price for sale

    if user_notes > settings.NOTES_AMOUNT:
        return {
            'count': settings.NOTES_AMOUNT,
            'price': price,
        }
    elif user_notes:
        return {
            'count': user_notes,
            'price': price,
        }


def buy(user_info, instrument_info):
    user_wmz = user_info['balance']['wmz']  # amount WMZ
    price = instrument_info['price'] - settings.PERCENT_BUY  # price for buy

    if user_wmz >= settings.NOTES_AMOUNT * price:
        return {
            'count': settings.NOTES_AMOUNT,
            'price': price,
        }
    elif user_wmz >= price:
        return {
            'count': int(user_wmz/price),
            'price': price,
        }

class TradingOpirations:

    def __init__(self, instrument_info, user_info, my_offer_list):
        self.buy_price = instrument_info['price'] - settings.PERCENT_BUY  # price for buy
        self.sell_price = instrument_info['price'] + settings.PERCENT_SELL  # price for sale
        self.user_wmz = user_info['balance']['wmz']  # amount WMZ
        self.user_notes = user_info['portfolio'][0]['notes']  # amount ETH notes
        self.selling_notes = functools.reduce(lambda x, y: x+y, (i['notes'] for i in my_offer_list if i['kind'] == 0))

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