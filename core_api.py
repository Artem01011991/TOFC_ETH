import requests
import base64
import hashlib
import time


class IndexInfo:
    """
    All data sends to methods as string values!!!
    """
    urls = {
        'tool': 'https://api.indx.ru/api/v2/trade/Tools',
        'balance': 'https://api.indx.ru/api/v2/trade/Balance',
        'my offer': 'https://api.indx.ru/api/v2/trade/OfferMy',
        'list offer': 'https://api.indx.ru/api/v2/trade/OfferList',
        'history trading': 'https://api.indx.ru/api/v2/trade/HistoryTrading',
        'history transaction': 'https://api.indx.ru/api/v2/trade/HistoryTransaction',
        'add offer': 'https://api.indx.ru/api/v2/trade/OfferAdd',
        'delete offer': 'https://api.indx.ru/api/v2/trade/OfferDelete',
    }

    def __init__(self, login, password, wmid, culture='en-EN'):
        self.login = login
        self.password = password
        self.wmid = wmid
        self.culture = culture
        while True:
            status = self.get_eth_status()
            if isinstance(status, str):
                time.sleep(1)
            else:
                break
        self.ID = str(status['id'])

    def get_eth_status(self):
        '''
        {'id': 64, 'name': 'ETH', 'price': 0.5473, 'kind': 2, 'type': 'ECU', 'by': 2}
        '''
        result = self._get_request(self.urls['tool'])
        return result.get('value')[1] if isinstance(result, dict) else result

    def get_balance(self):
        '''
        {'wmid': '1', 'nickname': 'Till', 'balance':
        {'price': 73.66, 'wmz': 0.43}, 'portfolio':
        [{'id': 64, 'name': 'ETH', 'notes': 134, 'price': 0.5133, 'type': 'ECU', 'kind': 2, 'by': 2}], 'profit':
        [{'symbolid': 64, 'buy': 517.1196, 'sell': 517.5498}]}
        '''
        result = self._get_request(self.urls['balance'], wmid=self.wmid)
        return result.get('value') if isinstance(result, dict) else result

    def _get_request(
            self,
            url,
            wmid=None,
            ID=None,
            date_from=None,
            date_to=None,
            count='0',
            is_anonymous=True,
            is_bid=True,
            price='0',
            offer_id=None
    ):
        return requests.post(url, json=self._form_request(wmid, ID, date_from, date_to, count, is_anonymous, is_bid, price, offer_id)).json()

    def _form_request(self, wmid, ID, date_from, date_to, count, is_anonymous, is_bid , price, offer_id):
        return {"ApiContext": {
                "Login": self.login,
                "Password": self.password,
                "Culture": self.culture,
                "Wmid": self.wmid,
                "Signature": self._get_signature(wmid, ID, date_from, date_to, offer_id),
            },
            "Trading":{
                "ID": ID,
                "DateStart": date_from,  # YYYYMMDD
                "DateEnd": date_to,  # YYYYMMDD
            },
            "Offer": {
                "ID": ID,
                "Count": count,
                "IsAnonymous": is_anonymous,
                "IsBid": is_bid,  # true - заявка будет создана для покупки, false - для продажи
                "Price": price,
            },
            "OfferId": offer_id,
        }

    def get_history_traiding(self, date_from, date_to):
        '''
        isbid - тип операции задается целым десятичным числом, 1 -покупка, 0 - продажа
        [{'id': 1358784, 'stamp': 1522603074, 'name': 'ETH.ECU', 'isbid': 1, 'notes': 30, 'price': 0.3794},
         {'id': 1358783, 'stamp': 1522603074, 'name': 'ETH.ECU', 'isbid': 1, 'notes': 20, 'price': 0.3793}]
        '''
        result = self._get_request(self.urls['history trading'], wmid=self.wmid, ID=self.ID, date_from=date_from, date_to=date_to)
        return result.get('value') if isinstance(result, dict) else result

    def get_history_transaction(self, date_from, date_to):
        result = self._get_request(self.urls['history transaction'], wmid=self.wmid, ID=self.ID, date_from=date_from, date_to=date_to)
        return result.get('value') if isinstance(result, dict) else result

    def get_offer_my(self):
        '''
        kind - тип операции задается целым десятичным числом, 1 -покупка, 0 - продажа
        [{"toolid":0,"offerid":0,"name":"","kind":0,"price":0,"notes":0,"stamp":}]
        '''
        result = self._get_request(self.urls['my offer'], wmid=self.wmid)
        return result.get('value') if isinstance(result, dict) else result

    def get_offer_list(self):
        '''
        kind - тип операции задается целым десятичным числом, 1 -покупка, 0 - продажа
        [{'offerid': 0, 'kind': 1, 'price': 0.5412, 'notes': 1}, {'offerid': 0, 'kind': 1, 'price': 0.5411, 'notes': 1}]
        '''
        result = self._get_request(self.urls['list offer'], wmid=self.wmid, ID=self.ID)
        return result.get('value') if isinstance(result, dict) else result

    def _get_signature(self, wmid, ID, date_from, date_to, offer_id):
        signature_values = [
            self.login,
            self.password,
            self.culture,
        ]

        if wmid:
            signature_values.append(wmid)
        if ID:
            signature_values.append(ID)
        if date_from or date_to:
            signature_values.extend([date_from, date_to])
        if offer_id:
            signature_values.append(offer_id)

        return base64.b64encode(hashlib.sha256(str.encode(';'.join(signature_values))).digest()).decode("utf-8")

    def set_offer(self, count, price, is_bid=True, is_anonymous=True):
        '''
        IsBid - тип подачи заявки true - заявка будет создана для покупки, false - для продажи
        '''
        return self._get_request(
            self.urls['add offer'],
            wmid=self.wmid,
            ID=self.ID,
            count=count,
            price=price,
            is_anonymous=is_anonymous,
            is_bid=is_bid
        )

    def delete_offer(self, offer_id):
        return self._get_request(self.urls['delete offer'], wmid=self.wmid, offer_id=str(offer_id))
