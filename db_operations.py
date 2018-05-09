# import mysql.connector as connector
from decouple import config
# from datetime import datetime
import psycopg2 as connector


class MySqlConnection:
    cnt = connector.connect(
        config('DATABASE_URL'), sslmode='require'
    )

    def __init__(self):
        self.cursor = self.cnt.cursor()

    def index_state_update(self, frash_price, percent, frash_change_percent):
        update = 'UPDATE index_state_track SET {' \
                 'percent=%(percent)s, ' \
                 'prior_price=%(frash_price)s,' \
                 'prior_change_percent=%(frash_change_percent)s' \
                 '} WHERE id=1;'
        data = {'frash_price': frash_price, 'percent': percent, 'frash_change_percent': frash_change_percent}

        self.cursor.execute(update, data)
        self.cnt.commit()

    def get_index_state(self):
        state = 'SELECT * FROM index_state_track WHERE id=1;'

        self.cursor.execute(state)
        return self.cursor

    # def __init__(self, price=None, kind=None, notes=None, offerID=None):
    #     self.stamp = datetime.now().date()
    #     self.price = price
    #     self.notes = notes
    #     self.kind = kind
    #     self.offerID = offerID
    #
    # def list(self):
    #     cursor = self.cnt.cursor()
    #     list = 'SELECT offerID FROM index_tasks;'
    #
    #     cursor.execute(list)
    #     return cursor
    #
    # def write(self):
    #     cursor = self.cnt.cursor()
    #     write = 'INSERT INTO index_tasks(stamp, price, notes, kind, offerID) VALUES (%(stamp)s, %(price)s, %(notes)s, %(kind)s, %(offerID)s);'
    #     data = {
    #         'stamp': self.stamp,
    #         'price': self.price,
    #         'notes': self.notes,
    #         'kind': self.kind,
    #         'offerID': self.offerID,
    #     }
    #
    #     cursor.execute(write, data)
    #     self.cnt.commit()
    #
    # def exist(self):
    #     cursor = self.cnt.cursor()
    #     read = 'SELECT * FROM index_tasks WHERE (price=%(price)s and kind=%(kind)s);'
    #     data = {
    #         'price': self.price,
    #         'kind': self.kind,
    #     }
    #
    #     cursor.execute(read, data)
    #     return next(cursor, None)
    #
    # def delete(self):
    #     cursor = self.cnt.cursor()
    #     delete = 'DELETE FROM index_tasks WHERE (offerID=%(offerID)s);'
    #     data = {
    #         'offerID': self.offerID,
    #     }
    #
    #     cursor.execute(delete, data)
    #     self.cnt.commit()
