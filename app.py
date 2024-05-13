from flask import Flask, render_template, jsonify
import threading
import time
from exchange_controller import ExchangeController


app = Flask(__name__)
controller = ExchangeController()

data = []  # Global data store

def update_data():
    global data
    symbols = ['BTC/USDT', 'ETH/USDT', 'SOL/USDT', 'XRP/USDT', 'ADA/USDT', 'DOGE/USDT', 'DOT/USDT']
    threshold = 0.20
    while True:
        new_data = []
        for symbol in symbols:
            result = controller.check_arbitrage_opportunity(symbol, threshold)
            if result:
                new_data.append(result)
        data = new_data
        time.sleep(20)  # Update data every 20 second

# Background thread to update data
thread = threading.Thread(target=update_data)
thread.daemon = True
thread.start()

@app.route('/')
def index():
    return render_template('table.html')

@app.route('/data')
def get_data():
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
