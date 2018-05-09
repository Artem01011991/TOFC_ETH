from decouple import config
import psycopg2 as connector


class Connection:
    cnt = connector.connect(
        config('DATABASE_URL'), sslmode='require'
    )

    def __init__(self):
        self.cursor = self.cnt.cursor()

    def index_state_update(self, frash_price, percent, frash_change_percent):
        update = 'UPDATE index_state_track SET ' \
                 'percent=%(percent)s, ' \
                 'prior_price=%(frash_price)s,' \
                 'prior_change_percent=%(frash_change_percent)s' \
                 ' WHERE id=1;'
        data = {'frash_price': frash_price, 'percent': percent, 'frash_change_percent': frash_change_percent}

        self.cursor.execute(update, data)
        self.cnt.commit()

    def get_index_state(self):
        state = 'SELECT * FROM index_state_track WHERE id=1;'

        self.cursor.execute(state)
        return self.cursor
