import requests
import json
from config import keys

class ExchangeException(Exception):
    pass


class Exchange:
    @staticmethod
    def convert(quote: str, base: str, amount: str):

        if quote == base:
            raise ExchangeException(f"Невозможно перевести одинаковые валюты {base}.")

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ExchangeException(f"Невозможно обработать валюту {quote}.\nПросмотреть доступные валюты - /values.")

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ExchangeException(f"Невозможно обработать валюту {base}.\nПросмотреть доступные валюты - /values.")

        try:
            amount = float(amount)
        except ValueError:
            raise ExchangeException(f"\nНе удалось обработать количество '{amount}'.")

        r = requests.get(f"https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}")
        total_base = json.loads(r.content)[keys[base]]

        return total_base * amount