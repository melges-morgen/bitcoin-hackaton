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


def find_query_by_id(order_id):
    session = sessionmaker(bind=engine)()
    return session.query(Order) \
        .filter(Order.id == order_id) \
        .one()


def add_transaction_to_order(order_id, tx):
    session = sessionmaker(bind=engine)()
    session.query(Order) \
        .filter(Order.id == order_id) \
        .update({Order.transaction: tx, Order.state: "PENDING"})
    session.commit()


class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    amount = Column(Integer)
    transaction = Column(String)
    state = Column(String)


engine = create_engine('sqlite:///database.sqlite', echo=True)
Base.metadata.create_all(engine)

