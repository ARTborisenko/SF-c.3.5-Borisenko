from config import KEY, keys, TOKEN
import requests
import json


class CovertionException(Exception):
    pass


class GetPrice():
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        if quote == base:
            raise CovertionException(f'Не удалось перевести одинаковые валюты {base}.')

        try:
            quote_tiker = keys[quote]
        except KeyError:
            raise CovertionException(f'Не удалось обработать валюту {quote}')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise CovertionException(f'Не удалось обработать валюту {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise CovertionException(f'Не удалось обработать количество {amount}')

        API = f'http://api.exchangeratesapi.io/v1/latest?access_key={KEY}'
        html = requests.get(API).content
        texts = json.loads(html)
        currencies = texts['rates']

        return currencies[base_ticker] / currencies[quote_tiker] * amount
