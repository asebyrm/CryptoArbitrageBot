from flask import Flask, jsonify, request
from exchange_controller import ExchangeController  # Önceki adımda oluşturduğunuz sınıf

app = Flask(__name__)
controller = ExchangeController()  # ExchangeController sınıfının bir örneğini oluştur

@app.route('/api/arbitrage', methods=['GET'])
def arbitrage():
    # Kullanıcıdan symbol ve threshold değerlerini al
    symbol = request.args.get('symbol', 'BTC/USD')
    threshold = float(request.args.get('threshold', 0.15))
    data = controller.check_arbitrage_opportunity(symbol, threshold)
    return jsonify(data)  # Elde edilen veriyi JSON formatında döndür

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
