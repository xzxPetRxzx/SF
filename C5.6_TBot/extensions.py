import requests
import json
from config import API_KEY, keys

#Исключения
class APIException(Exception):
    pass
#Класс конвертации
class Converter:
    @staticmethod
    def get_price(base: str, quote: str, amount: str):
        #выброс возможных ошибок
        if base == quote:
            raise APIException('валюты конвертации одинаковы')
        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Ошибка валюты:{base}')
        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'Ошибка валюты:{quote}')
        try:
            fl_amount = float(amount)
        except ValueError:
            raise APIException(f'неправильно введено число:{amount}')
        #подключение к сервису и вычисление курса
        r = requests.get(f'https://currate.ru/api/?get=rates&pairs={base_ticker}{quote_ticker}&key={API_KEY}')
        course = float(json.loads(r.content)['data'][f'{base_ticker}{quote_ticker}']) * fl_amount
        return str(course)
