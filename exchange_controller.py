import ccxt
import csv
from datetime import datetime


class ExchangeController:
    def __init__(self):
        # API anahtarlarınızı buraya ekleyeceksiniz, şimdilik yoruma alındı
        self.exchange_config = {
            'binance': {
                # 'apiKey': 'YOUR_BINANCE_API_KEY',
                # 'secret': 'YOUR_BINANCE_SECRET'
            },
            'coinbase': {
                # 'apiKey': 'YOUR_COINBASE_API_KEY',
                # 'secret': 'YOUR_COINBASE_SECRET'
            },
            'kraken': {
                # 'apiKey': 'YOUR_KRAKEN_API_KEY',
                # 'secret': 'YOUR_KRAKEN_SECRET'
            },
            'bitget': {
                # 'apiKey': 'YOUR_BITFINEX_API_KEY',
                # 'secret': 'YOUR_BITFINEX_SECRET'
            },
            'okx': {
                # 'apiKey': 'YOUR_BITFINEX_API_KEY',
                # 'secret': 'YOUR_BITFINEX_SECRET'
            },
            'kucoin': {
                # 'apiKey': 'YOUR_BITFINEX_API_KEY',
                # 'secret': 'YOUR_BITFINEX_SECRET'
            },
            'cryptocom': {
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
            data = {
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'symbol': symbol,
                'price_difference': price_difference,
                'prices': prices,
                'arbitrage_opportunity': price_difference > threshold
            }
            self.save_data_to_csv(data)
            return data
        return None

    def save_data_to_csv(self, data, filename='arbitrage_data.csv'):
        # Tüm borsa isimlerini almak için data['prices'] anahtarlarını kullan
        exchanges = list(data['prices'].keys())
        # Her bir borsa için bir sütun başlığı oluştur
        fieldnames = ['timestamp', 'symbol'] + exchanges + ['price_difference', 'arbitrage_opportunity']
        try:
            with open(filename, 'a', newline='') as csvfile:
                # Eğer dosya yeni oluşturulduysa, sütun başlıklarını yaz
                if csvfile.tell() == 0:
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                # Verileri uygun şekilde düzenle
                row = {
                    'timestamp': data['timestamp'],
                    'symbol': data['symbol'],
                    'price_difference': f"{data['price_difference']:.2f}",
                    'arbitrage_opportunity': data['arbitrage_opportunity']
                }
                # Her borsanın fiyatını ilgili sütuna yerleştir
                row.update(data['prices'])

                # Satırı yaz
                writer.writerow(row)
        except IOError as e:
            print(f"Error writing to CSV: {str(e)}")

