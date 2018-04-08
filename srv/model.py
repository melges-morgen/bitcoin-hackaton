import enum
import calendar
import time
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app import app, db


def create_order(amount):
    order = Order(amount=amount, state="CREATED")
    db.session.add(order)
    db.session.commit()
    return order


def find_query_by_id(order_id):
    return db.session.query(Order) \
        .filter(Order.id == order_id) \
        .one()


def check_transaction(tx):
    return not db.session.query(SQLAlchemy.exists() \
            .where(Order.transaction == tx)).scalar()


def add_transaction_to_order(order_id, tx):
    db.session.query(Order) \
        .filter(Order.id == order_id) \
        .update({Order.transaction: tx, Order.state: "PENDING"})
    db.session.commit()


def complete_order(order_id):
    db.session.query(Order) \
        .filter(Order.id == order_id) \
        .update({Order.state: "COMPLETED"})
    db.session.commit()


def complete_order_by_transaction(tx):
    db.session.query(Order) \
        .filter(Order.transaction == tx) \
        .update({Order.state: "COMPLETED"})
    db.session.commit()


class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer)
    transaction = db.Column(db.String)
    state = db.Column(db.String)


class CType(enum.IntEnum):
    amount = 1
    time = 2


class Invoice(db.Model):
    __tablename__ = 'invoice'

    user_data = db.Column(db.String, nullable=True)
    confirmation_type = db.Column(db.Enum(CType))
    amount_satoshi = db.Column(db.Integer, primary_key=True)
    lock_time = db.Column(db.Integer, nullable=True, primary_key=True)
    to_addr = db.Column(db.String, nullable=False, primary_key=True)

    def __repr__(self):
        return "to={} amount={} ud={}".format(self.to_addr, self.amount_satoshi,
                                              self.user_data)

    @staticmethod
    def _new_amomunt_diff(satoshi, user_data=None):
        invoices = db.session.query(Invoice) \
                .filter(Invoice.amount_satoshi >= satoshi) \
                .order_by("amount_satoshi")
        for invoice in invoices:
            if satoshi != invoice.amount_satoshi:
                break
            else:
                satoshi += 1
        to_addr = "mzG7e9S5z4dBzUNV2brKMHu7ZQTyEeu3fV"
        ts = calendar.timegm(time.gmtime())
        invoice = Invoice(amount_satoshi=satoshi, confirmation_type=CType.amount,
                          to_addr=to_addr, user_data=user_data, lock_time=ts)
        db.session.add(invoice)
        db.session.commit()
        return invoice

    @staticmethod
    def _new_time_diff(satoshi, user_data=None):
        ts = calendar.timegm(time.gmtime())
        to_addr = "mzG7e9S5z4dBzUNV2brKMHu7ZQTyEeu3fV"
        invoice = Invoice(amount_satoshi=satoshi, confirmation_type=CType.time,
                          to_addr=to_addr, user_data=user_data,
                          lock_time=ts)
        db.session.add(invoice)
        db.session.commit()
        return invoice

    @staticmethod
    def new(confirmation_type, **kwargs):
        if confirmation_type == "amount":
            invoice = Invoice._new_amomunt_diff(**kwargs)
        elif confirmation_type == "time":
            invoice = Invoice._new_time_diff(**kwargs)
        else:
            raise Exception("Wrong confirmation type " + confirmation_type)
        invoices = db.session.query(Invoice) \
                .order_by("amount_satoshi")
        for xinvoice in invoices:
            print("Inv", xinvoice)
        return invoice


db.create_all()
