import requests
import json
from config import keys


class APIException(Exception):
    pass


class Converter:
    @staticmethod
    def get_price(base: str, quote: str, amount: str):

        if base == quote:
            raise APIException(f'Нельзя конвертировать одинаковые валюты: {base}.')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {base}')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {quote}')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество: {amount}')

        request_text = f'https://api.exchangeratesapi.io/latest?base={base_ticker}&symbols={quote_ticker}'
        response = requests.get(request_text)
        response_dict = json.loads(response.content)
        total_rate = amount * response_dict['rates'][quote_ticker]

        return total_rate
