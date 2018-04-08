import random

from btcpy.setup import setup

from flask import Flask, jsonify, request
import model

app = Flask(__name__)


@app.route('/health-check')
def health_check():
    return "OK"


@app.route('/current-order')
def current_order():
    order = model.create_order(random.uniform(0.01, 1.1))
    return jsonify(
        id=order.id,
        amount=order.amount,
        state=order.state
    )


@app.route('/orders/<order_id>/pay', methods = ['POST'])
def pay_order(order_id):
    pay_info = request.get_json()
    print(order_id)
    print(pay_info)

    return '', 204

if __name__ == '__main__':
    app.run(debug=True)
