import random

from btcpy.setup import setup
from btcpy.structs.crypto import PublicKey
from btcpy.structs.transaction import Transaction

from flask import Flask, jsonify, request
import model

ADDRESS = "mvmSpLUxCXkMGj3CTAsudaB148YypZodDm"

app = Flask(__name__)
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

    model.add_transaction_to_order(order_id, tx.transaction)

    return '', 204


@app.route('/orders/<order_id>')
def get_order(order_id):
    order = model.find_query_by_id(order_id)
    return jsonify(
        id=order.id,
        amount=order.amount,
        state=order.state,
        destination=ADDRESS
    )


def check_transaction(tx, amont):
    for out in tx.outs:
        if out.value == amont and str(out.script_pubkey.address()) == ADDRESS:
            return True
    return False


if __name__ == '__main__':
    app.run(debug=True)
