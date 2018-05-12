import settings


class IndexTrading:

    def __init__(self, percent, prior_price, prior_change_percent, actual_price):
        self.percent = percent
        self.prior_price = prior_price
        self.prior_change_percent = prior_change_percent
        self.actual_price = actual_price
        self.actual_change_percent = (self.actual_price - self.prior_price) / (settings.SELL_BUY_PRICE_DIFF / 100.0)

    def get_trade_state_percent(self):

        if self.actual_change_percent < settings.RESET_TRADE_STATE_PERCENT and \
                self.prior_change_percent < settings.RESET_TRADE_STATE_PERCENT:
            if self.percent > 0:
                return self.percent - settings.DECREASE_TRADE_PERCENT
            elif self.percent < 0:
                return self.percent + settings.DECREASE_TRADE_PERCENT
            else:
                return self.percent

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
        trade_state_percent = settings.MIN_PERCENT_FOR_SELL_BUY / 100.0 * self.get_trade_state_percent()

        if trade_state_percent > 0:
            buy_notes = 50.0 + trade_state_percent
            buy_price_diff = settings.SELL_BUY_PRICE_DIFF / 100.0 * (50.0 + trade_state_percent)
            sell_notes = 100.0 - buy_notes
            sell_price_diff = settings.SELL_BUY_PRICE_DIFF - buy_price_diff
        elif trade_state_percent < 0:
            sell_notes = 50.0 + (-trade_state_percent)
            sell_price_diff = settings.SELL_BUY_PRICE_DIFF / 100.0 * (50.0 + (-trade_state_percent))
            buy_notes = 100.0 - sell_notes
            buy_price_diff = settings.SELL_BUY_PRICE_DIFF - sell_price_diff
        else:
            buy_notes = 50.0
            buy_price_diff = settings.SELL_BUY_PRICE_DIFF / 2.0
            sell_notes = 50.0
            sell_price_diff = settings.SELL_BUY_PRICE_DIFF - buy_price_diff

        return {
            'buy_notes': buy_notes,
            'buy_price_diff': buy_price_diff,
            'sell_notes': sell_notes,
            'sell_price_diff': sell_price_diff
        }
