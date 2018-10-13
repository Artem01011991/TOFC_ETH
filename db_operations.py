from TOFC_ETH import settings
from datetime import datetime
import psycopg2 as connector


class Connection:
    cnt = connector.connect(
        settings.DATABASE_URL, sslmode='require'
    )

    def __init__(self):
        self.cursor = self.cnt.cursor()

    def get_timestamp_data(self, table):
        query = 'SELECT * FROM {table} ORDER BY created ASC;'.format(table=table)

        self.cursor.execute(query)
        return self.cursor  # [[id, created, price]]

    def set_timestamp(self, price, table):
        created = datetime.now()
        query = 'INSERT INTO {table} (created, price) VALUES (%(created)s, %(price)s);'.format(table=table)
        data = {'created': created, 'price': price}

        self.cursor.execute(query, data)
        self.cnt.commit()

    def delete_timestamp_data(self, id_list, table):
        query = 'DELETE FROM {table} WHERE id IN %(id_list)s;'.format(table=table)
        data = {'id_list': id_list}

        self.cursor.execute(query, data)
        self.cnt.commit()

    def get_price_data(self, table):
        query = 'SELECT * FROM {table};'.format(table=table)

        self.cursor.execute(query)
        return self.cursor  # [[price, buy_price, buy_amount]]

    def update_price_data(self, average_price, buy_price, buy_amount):
        query = 'UPDATE index_minimal_sell_price SET' \
                'price=%(average_price)s,' \
                'buy_price=%(buy_price)s,' \
                'buy_amount=%(buy_amount)s' \
                'WHERE id=1;'
        data = {'average_price': average_price, 'buy_price': buy_price, 'buy_amount': buy_amount}

        self.cursor.execute(query, data)
        self.cnt.commit()
