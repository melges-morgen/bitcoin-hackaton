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
    order = model.create_order(random.uniform(0.01, 1.1) * 10 ** 8)
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
    if not check_transaction(tx, 2000):
        return jsonify(error='Destination or amount are wrong'), 400
    print(pay_info)

    return '', 204


def check_transaction(tx, amont):
    for out in tx.outs:
        if out.value == amont and out.script_pubkey.to_address() == ADDRESS:
            return True
    return False


if __name__ == '__main__':
    app.run(debug=True)
