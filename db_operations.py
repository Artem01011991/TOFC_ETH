from decouple import config
import psycopg2 as connector


class Connection:
    cnt = connector.connect(
        config('DATABASE_URL'), sslmode='require'
    )

    def __init__(self):
        self.cursor = self.cnt.cursor()

    # def index_state_update(self, frash_price, percent, frash_change_percent):
    #     update = 'UPDATE index_state_track SET ' \
    #              'percent=%(percent)s, ' \
    #              'prior_price=%(frash_price)s,' \
    #              'prior_change_percent=%(frash_change_percent)s' \
    #              ' WHERE id=1;'
    #     data = {'frash_price': frash_price, 'percent': percent, 'frash_change_percent': frash_change_percent}
    #
    #     self.cursor.execute(update, data)
    #     self.cnt.commit()
    #
    # def get_index_state(self):
    #     state = 'SELECT * FROM index_state_track WHERE id=1;'
    #
    #     self.cursor.execute(state)
    #     return self.cursor

    def get_timestamp_data(self):
        query = 'SELECT * FROM index_price_stamp ORDER BY created ASC;'

        self.cursor.execute(query)
        return self.cursor  # [[id, created, price]]

    def set_timestamp(self, created, price):
        query = 'INSERT INTO index_price_stamp (created, price) VALUES (%(created)s, %(price)s);'
        data = {'created': created, 'price': price}

        self.cursor.execute(query, data)
        self.cnt.commit()

    def delete_timestamp_data(self, id_list):
        query = 'DELETE FROM index_price_stamp WHERE id IN %(id_list)s;'
        data = {'id_list': id_list}

        self.cursor.execute(query, data)
        self.cnt.commit()

    def get_price_data(self):
        query = 'SELECT * FROM index_minimal_sell_price;'

        self.cursor.execute(query)
        return self.cursor  # [[price, buy_price, buy_amount]]

    def set_price_data(self, average_price, buy_price, buy_amount):
        query = 'UPDATE index_minimal_sell_price SET' \
                'price=%(average_price)s,' \
                'buy_price=%(buy_price)s,' \
                'buy_amount=%(buy_amount)s' \
                'WHERE id=1;'
        data = {'average_price': average_price, 'buy_price': buy_price, 'buy_amount': buy_amount}

        self.cursor.execute(query, data)
        self.cnt.commit()
