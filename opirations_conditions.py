from settings import CRITICAL_PERCENT


class TradingOpirations:

    def __init__(self, trading_percentage_result, user_info, price, offer_list):
        self.user_wmz = user_info['balance']['wmz']  # amount WMZ
        self.user_notes = user_info['portfolio'][0]['notes']  # amount ETH notes
        self.trading_percentage_result = trading_percentage_result
        self.price = price
        self.offer_list = offer_list

    def sell(self):

        if self.user_notes:
            if self.trading_percentage_result['sell_notes'] >= CRITICAL_PERCENT:
                return self.large_percent()
            return {
                'count': int(self.user_notes / 100 * self.trading_percentage_result['sell_notes']),
                'price': self.trading_percentage_result['sell_price_diff'] + self.price,
            }

    def buy(self):

        if self.trading_percentage_result['buy_notes'] >= CRITICAL_PERCENT:
            return self.large_percent(sell=False)

        buy_price = self.price - self.trading_percentage_result['buy_price_diff']

        if self.user_wmz >= buy_price:
            return {
                'count': int((self.user_wmz / buy_price) / 100 * self.trading_percentage_result['buy_notes']),
                'price': buy_price,
            }

    def large_percent(self, sell=True):
        temp = None

        if sell:
            for i in self.offer_list:
                if i['kind'] == 0:
                    temp = i['price'] if not temp or temp > i['price'] else temp
            return {'count': self.user_notes, 'price': temp - 0.001}

        for i in self.offer_list:
            if i['kind'] == 1:
                temp = i['price'] if not temp or temp < i['price'] else temp

        if int(self.user_wmz / temp + 0.001):
            return {'count': int(self.user_wmz / temp + 0.001), 'price': temp + 0.001}
