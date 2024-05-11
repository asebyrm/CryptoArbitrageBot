import ccxt
import csv
from datetime import datetime

class ExchangeController:
    def __init__(self):
        # API anahtarlarınızı buraya ekleyeceksiniz, şimdilik yoruma alındı
        self.exchange_config = {
            'kraken': {
                # 'apiKey': 'YOUR_KRAKEN_API_KEY',
                # 'secret': 'YOUR_KRAKEN_SECRET'
            },
            'coinbase': {
                # 'apiKey': 'YOUR_COINBASE_API_KEY',
                # 'secret': 'YOUR_COINBASE_SECRET'
            },
            'binance': {
                # 'apiKey': 'YOUR_BINANCE_API_KEY',
                # 'secret': 'YOUR_BINANCE_SECRET'
            },
            'bitfinex': {
                # 'apiKey': 'YOUR_BITFINEX_API_KEY',
                # 'secret': 'YOUR_BITFINEX_SECRET'
            }
        }
        self.exchanges = self.setup_exchanges()

    def setup_exchanges(self):
        exchanges = []
        for name, config in self.exchange_config.items():
            exchange_class = getattr(ccxt, name)
            exchange = exchange_class({
                'enableRateLimit': True
                # 'apiKey': config.get('apiKey', ''),
                # 'secret': config.get('secret', '')
            })
            exchanges.append(exchange)
        return exchanges

    def fetch_prices(self, symbol):
        prices = {}
        for exchange in self.exchanges:
            try:
                ticker = exchange.fetch_ticker(symbol)
                prices[exchange.id] = ticker['last']
            except Exception as e:
                print(f"{datetime.now()}: Error fetching price from {exchange.id} for {symbol}: {str(e)}")
        return prices

    def check_arbitrage_opportunity(self, symbol, threshold):
        prices = self.fetch_prices(symbol)
        if prices and len(prices.values()) > 0:
            min_price = min(prices.values())
            max_price = max(prices.values())
            price_difference = (max_price - min_price) / min_price * 100
            return {
                'symbol': symbol,
                'min_price': min_price,
                'max_price': max_price,
                'price_difference': price_difference
            }
        else:
            return {'error': 'No prices available'}

    def save_data_to_csv(self, data, filename='arbitrage_data.csv'):
        fieldnames = ['timestamp', 'symbol', 'price_difference', 'prices', 'count']
        try:
            with open(filename, 'a', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writerow(data)
        except IOError as e:
            print(f"Error writing to CSV: {str(e)}")
