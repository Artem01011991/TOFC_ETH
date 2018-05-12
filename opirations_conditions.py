class TradingOpirations:

    def __init__(self, trading_percentage_result, user_info, price):
        self.user_wmz = user_info['balance']['wmz']  # amount WMZ
        self.user_notes = user_info['portfolio'][0]['notes']  # amount ETH notes
        self.trading_percentage_result = trading_percentage_result
        self.price = price

    def sell(self):

        if self.user_notes:
            return {
                'count': int(self.user_notes / 100 * self.trading_percentage_result['sell_notes']),
                'price': self.trading_percentage_result['sell_price_diff'] + self.price,
            }

    def buy(self):
        buy_price = self.price - self.trading_percentage_result['buy_price_diff']

        if self.user_wmz >= buy_price:
            return {
                'count': int((self.user_wmz / buy_price) / 100 * self.trading_percentage_result['buy_notes']),
                'price': buy_price,
            }
