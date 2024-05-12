from flask import Flask, render_template, jsonify
from exchange_controller import ExchangeController
import threading
import time

app = Flask(__name__)
controller = ExchangeController()

data = []  # Global veri deposu

def update_data():
    global data
    symbols = ['BTC/USD', 'ETH/USD', 'SOL/USD', 'XRP/USD', 'ADA/USD', 'LTC/USD', 'BCH/USD']
    threshold = 0.15
    counts = {symbol: 0 for symbol in symbols}
    while True:
        new_data = []
        for symbol in symbols:
            result = controller.check_arbitrage_opportunity(symbol, threshold)
            if result:  # Eğer arbitraj fırsatı varsa
                new_data.append(result)
        data = new_data
        time.sleep(10)  # Verileri her 1 dakikada bir güncelle

# Arka planda veri güncellemesi için thread başlat
thread = threading.Thread(target=update_data)
thread.start()

@app.route('/')
def index():
    return render_template('table.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)
