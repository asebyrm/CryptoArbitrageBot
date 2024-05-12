from flask import Flask, render_template
from exchange_controller import ExchangeController
import threading
import time

app = Flask(__name__)
controller = ExchangeController()

data = []  # Global veri deposu
data_lock = threading.Lock()  # Veri listesi için bir kilit oluşturaa

def update_data():
    global data
    symbols = ['BTC/USDT', 'ETH/USDT', 'SOL/USDT', 'XRP/USDT', 'ADA/USDT', 'DOGE/USDT', 'DOT/USDT']
    threshold = 0.15
    while True:
        new_data = []
        for symbol in symbols:
            result = controller.check_arbitrage_opportunity(symbol, threshold)
            if result:  # Eğer arbitraj fırsatı varsa
                new_data.append(result)
        with data_lock:  # Data listesini kilit altına alarak güncelle
            data.clear()
            data.extend(new_data)
        time.sleep(60)  # Verileri her 60 saniyede bir güncelle

# Arka planda veri güncellemesi için thread başlat
thread = threading.Thread(target=update_data)
thread.daemon = True
thread.start()

@app.route('/')
def index():
    with data_lock:  # Data listesine erişirken kilit kullan
        return render_template('table.html', data=data.copy())

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
