import random

from btcpy.setup import setup
from btcpy.structs.crypto import PublicKey
from btcpy.structs.transaction import Transaction

from flask import Flask, jsonify, request, abort
from app import app
import model

ADDRESS = "mvmSpLUxCXkMGj3CTAsudaB148YypZodDm"

setup('testnet')


@app.route('/health-check')
def health_check():
    return "OK"


@app.route('/current-order')
def current_order():
    order = model.create_order(int(random.uniform(0.01, 1.1) * 10 ** 4))
    return jsonify(
        id=order.id,
        amount=order.amount,
        state=order.state,
        destination=ADDRESS
    )


@app.route('/orders/<order_id>/pay', methods=['POST'])
def pay_order(order_id):
    pay_info = request.get_json()
    tx = Transaction.unhexlify(pay_info['transaction'])
    order = model.find_query_by_id(order_id)
    if not check_transaction(tx, order.amount):
        return jsonify(error='Destination or amount are wrong'), 400

    if not model.check_transaction(tx.txid):
        return jsonify(error='This transaction already used for another order'), 400

    post_transaction_to_bitcoin_network(tx)
    model.add_transaction_to_order(order_id, tx.txid)

    return '', 204


@app.route('/orders/<order_id>')
def get_order(order_id):
    order = model.find_query_by_id(order_id)
    return jsonify(
        id=order.id,
        amount=order.amount,
        state=order.state,
        transaction=order.transaction
    )


def check_transaction(tx, amont):
    for out in tx.outs:
        if out.value == amont and str(out.script_pubkey.address()) == ADDRESS:
            return True
    return False

def post_transaction_to_bitcoin_network(tx):
    pass

@app.route('/invoice/', methods=['POST'])
def new_invoice():
    # if not request.json:
    #     abort(400)
    pay_info = request.get_json()
    invoice = model.Invoice.new(**pay_info)
    return jsonify({
        "amount_satoshi": invoice.amount_satoshi,
        "lock_time": invoice.lock_time,
        "to_addr": invoice.to_addr,
        "confirmation_type": invoice.confirmation_type,
        "user_data": invoice.user_data
    })
    # return '', 204


if __name__ == '__main__':
    app.run(debug=True)
