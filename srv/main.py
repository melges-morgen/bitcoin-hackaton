from btcpy.setup import setup

from flask import Flask

app = Flask(__name__)


@app.route('/health-check')
def health_check():
    return "OK"

def current_order():
    


if __name__ == '__main__':
    app.run(debug=True)
