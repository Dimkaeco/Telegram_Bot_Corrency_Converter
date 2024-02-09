import requests
import json

class APIException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class CurrencyConverter:
    @staticmethod
    def get_price(base, quote, amount):
        api_key = "1fbae4aeafafd089aecda465"
        url = f"https://v6.exchangerate-api.com/v6/{api_key}/pair/{base}/{quote}/{amount}"

        response = requests.get(url)
        data = json.loads(response.text)

        if response.status_code != 200 or 'error' in data:
            raise APIException(f"Не удалось получить обменный курс. Ошибка: {data.get('error', 'Неизвестная ошибка')}")

        price = data.get('conversion_result')
        if price is None:
            raise APIException("Не удалось получить обменный курс. Результат конвертации не найден.")

        return price
