from TOFC_ETH.main.operations import OperationsBaseClass


class BinanceOperationsClass(OperationsBaseClass):
    def __init__(self, timestamp_list, purchase_data=None, client_data=None):
        super(BinanceOperationsClass, self).__init__(timestamp_list)
        if purchase_data and client_data:
            self.minimal_price = self._minimal_price(purchase_data, client_data)

    def _minimal_price(self, purchase_data: tuple(), client_data: tuple()):
        '''

        :param purchase_data: data that is got by sale ('quntity', 'price',)
        :param client_data: data that is stored in DB ('quntity', 'price',)
        :return: minimal price which is necessary for get back entire amount of money
        '''
        purchase_entire_price = purchase_data[0] * purchase_data[1]
        client_data_entire_price = client_data[0] * client_data[1]
        amount_of_symbol = purchase_data[0] + client_data[0]
        return (purchase_entire_price + client_data_entire_price) / amount_of_symbol
