import mysql.connector as connector
from decouple import config
from datetime import datetime


class MySqlConnection:
    cnt = connector.connect(
        user='kgbhmmyxevpltt',
        password='28cbd7f4e0bcf341902c08f48372d41f8d9e80cde7329d3c9105b6d868121fc4',
        host='ec2-174-129-41-64.compute-1.amazonaws.com',
        port='5432',
        database='d7ujqj2gd6r5kn',
    )

    def __init__(self, price=None, kind=None, notes=None, offerID=None):
        self.stamp = datetime.now().date()
        self.price = price
        self.notes = notes
        self.kind = kind
        self.offerID = offerID

    def list(self):
        cursor = self.cnt.cursor(buffered=True)
        list = 'SELECT offerID FROM index_tasks;'

        cursor.execute(list)
        return cursor

    def write(self):
        cursor = self.cnt.cursor()
        write = 'INSERT INTO index_tasks SET stamp=%(stamp)s, price=%(price)s, notes=%(notes)s, kind=%(kind)s, offerID=%(offerID)s;'
        data = {
            'stamp': self.stamp,
            'price': self.price,
            'notes': self.notes,
            'kind': self.kind,
            'offerID': self.offerID,
        }

        cursor.execute(write, data)
        self.cnt.commit()

    def exist(self):
        cursor = self.cnt.cursor()
        read = 'SELECT * FROM index_tasks WHERE (price=%(price)s and kind=%(kind)s);'
        data = {
            'price': self.price,
            'kind': self.kind,
        }

        cursor.execute(read, data)
        return next(cursor, None)

    def delete(self):
        cursor = self.cnt.cursor()
        delete = 'DELETE FROM index_tasks WHERE (offerID=%(offerID)s);'
        data = {
            'offerID': self.offerID,
        }

        cursor.execute(delete, data)
        self.cnt.commit()
