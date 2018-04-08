import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Float, BLOB
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


def create_order(amount):
    session = sessionmaker(bind=engine)()
    order = Order(amount=amount, state="CREATED")
    session.add(order)
    session.commit()
    return order


class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    amount = Column(Float)
    transaction = Column(BLOB)
    state = Column(String)


engine = create_engine('sqlite:///database.sqlite', echo=True)
Base.metadata.create_all(engine)

