from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from tofc_eth.conf import settings


class PostgreConnection:
    def __enter__(self):
        self.engine = create_engine(settings.DATABASE_URL, echo=True)
        self.session = sessionmaker(bind=self.engine)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close_all()
