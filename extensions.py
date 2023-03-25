import requests
from config import exchanges

class ApiException(Exception):
    pass

class Converter:
    @staticmethod
    def get_price(base, quote, amount):
        try:
            base_key = exchanges[base.lower()]
        except KeyError:
            return ApiException(f"Валюта {base} не найдена!")
        try:
            quote_key = exchanges[quote.lower()]
        except KeyError:
            return ApiException(f"Валюта {base} не найдена!")
        if base_key == quote_key:
            raise ApiException(f"Невозможно перевести одинаковые валюты {base}!")
        try:
            amount = float(amount.replace(",", "."))
        except ValueError:
            raise ApiException(f"Не удалось обработать количество {amount}!")

        url = f'https://v6.exchangerate-api.com/v6/0ec66db3a233bd52c1e71a21/pair/{base_key}/{quote_key}'
        response = requests.get(url)
        resp = response.json()
        new_price = resp['conversion_rate'] * float(amount)
        return round(new_price, 2)