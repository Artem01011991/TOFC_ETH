from sqlalchemy import Column, DateTime, ForeignKey, Integer, Sequence, String
from sqlalchemy.ext.declarative import declarative_base

ExchangeBase = declarative_base()


class Exchange(ExchangeBase):
    __tablename__ = "exchange"

    id = Column(Integer, Sequence("exchange_id_seq"), primary_key=True)
    name = Column(String(20), unique=True)


TimeStampBase2 = declarative_base()


class TimeStamp(TimeStampBase2):
    __tablename__ = "timestamp"

    id = Column(Integer, Sequence("timestamp_id_seq"), primary_key=True)
    date = Column(DateTime)
    exchange = Column(ForeignKey(Exchange.id, ondelete="RESTRICT"))
    price = Column(Integer)

    def __str__(self):
        return "{exchange_name} - {price} - {date}".format(
            exchange_name=self.exchange.name, price=self.price, date=self.date,
        )
