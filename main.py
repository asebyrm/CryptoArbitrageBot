from exchange_controller import ExchangeController
import time


def main():
    controller = ExchangeController()
    symbols = ['BTC/USDT', 'ETH/USDT', 'SOL/USDT', 'XRP/USDT', 'ADA/USDT', 'DOGE/USDT', 'DOT/USDT']
    threshold = 0.20

    while True:
        for symbol in symbols:
            controller.check_arbitrage_opportunity(symbol, threshold)
            time.sleep(1)

if __name__ == '__main__':
    main()
