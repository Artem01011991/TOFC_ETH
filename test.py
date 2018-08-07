import settings
import unittest
from core_binance_api import BinanceCoreApi
from db_operations import Connection


class BinanceTest(unittest.TestCase):

    def setUp(self):

        # main
        self.binance_api_connection = BinanceCoreApi(
            settings.BINANCE_APIKEY,
            settings.BINANCE_SECRETKEY,
            settings.BINANCE_API_SYMBOL
        )
        self.db_connection = Connection()

        self.symbol_info = self.binance_api_connection.symbol_price_ticker()
        self.list_timestampe = self.db_connection.get_timestamp_data(settings.BINANCE_PRICE_STAMP_TABLE).fetchall()

        self.client_orders = self.binance_api_connection.current_open_orders()
        self.buy_order = next((i for i in self.client_orders if i['side'] == 'BUY'), None)
        self.sell_order = next((i for i in self.client_orders if i['side'] == 'SELL'), None)


if __name__ == '__main__':
    unittest.main()
