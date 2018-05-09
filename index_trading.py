import settings


class IndexTrading:

    def __init__(self, percent, prior_price, prior_change_percent, actual_price):
        self.percent = percent
        self.prior_price = prior_price
        self.prior_change_percent = prior_change_percent
        self.actual_price = actual_price
        self.actual_change_percent = (self.actual_price - self.prior_price) / (self.actual_price / 100.0)

    def get_trade_state_percent(self):

        if self.actual_change_percent < settings.RESET_TRADE_STATE_PERCENT and \
                self.prior_change_percent < settings.RESET_TRADE_STATE_PERCENT:
            return 0.0

        change_percent = self.actual_change_percent - self.prior_change_percent if \
            (self.prior_change_percent > 0 < self.actual_change_percent < self.prior_change_percent) or \
            (self.prior_change_percent < 0 > self.actual_change_percent > self.prior_change_percent) else \
            self.actual_change_percent

        trade_state_percent = self.percent + change_percent

        if trade_state_percent > 100:
            return 100.0
        elif trade_state_percent < -100:
            return -100.0
        else:
            return trade_state_percent

    def sell_buy_conditions(self):
        trade_state_percent = self.get_trade_state_percent()

        if trade_state_percent > 0:
            sell_notes = int(settings.NOTES_AMOUNT / 100 * settings.MIN_PERCENT_FOR_SELL_BUY)