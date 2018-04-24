import mysql.connector as connector
from decouple import config
from datetime import datetime


class MySqlConnection:
    cnt = connector.connect(
        user=config('USER_DB'),
        password=config('PASSWORD_DB'),
        host=config('HOST_DB'),
        port=config('PORT_DB'),
        database=config('NAME_DB'),
    )

    def __init__(self, price, count, isbid):
        self.date = datetime.now()
        self.price = price
        self.count = count
        self.isbid = isbid

    def __delete__(self, instance):
        self.cnt.commit()
        self.cnt.close()
        return super().__delete__(instance)

    def write(self):
        cursor = self.cnt.cursor()
        write = 'INSERT INTO `%{table}s` SET (`date`="%{date}s", `price`="%{price}s", `count`="%{count}s", `isbid`="%{isbid}s");'
        data = {
            'table': config('TABLE_DB'),
            'date': self.date,
            'price': self.price,
            'count': self.count,
            'isbid': self.isbid,
        }

        cursor.execute(write, data)

    def read(self):
        cursor = self.cnt.cursor()
        read = 'SELECT * FROM `%{table}s` WHERE (`price`="%{price}s", `isbid`="%{isbid}s");'
        data = {
            'table': config('TABLE_DB'),
            'price': self.price,
            'isbid': self.isbid,
        }

        cursor.execute(read, data)
        return cursor

    def delete(self):
        pass
