import telebot
import extensions
from config import TELEGRAM_BOT_TOKEN
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

#bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)
bot = telebot.TeleBot(os.getenv("TELEGRAM_BOT_TOKEN"))

@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    instructions = (
        "Привет! Я бот для получения курса валют.\n"
        "Для получения цены на валюту используйте формат: <валюта1> <валюта2> <количество>\n"
        "Пример: USD EUR 100\n"
        "Для просмотра доступных валют используйте /values"
    )
    bot.send_message(message.chat.id, instructions)

@bot.message_handler(commands=['values'])
def handle_values(message):
    available_currencies = "Доступные валюты:\nUSD - Доллар США\nEUR - Евро\nRUB - Российский рубль"
    bot.send_message(message.chat.id, available_currencies)

@bot.message_handler(func=lambda message: True)
def handle_currency_conversion(message):
    try:
        input_data = message.text.split()
        if len(input_data) != 3:
            raise extensions.APIException("Неверный формат ввода. Используйте: <валюта1> <валюта2> <количество>")
        if len(input_data) > 3:
            raise extensions.APIException(
                "Вы ввели больше трех валют. Используйте формат: <валюта1> <валюта2> <количество>")

        base_currency, quote_currency, amount = input_data
        price = extensions.CurrencyConverter.get_price(base_currency, quote_currency, float(amount))

        response_message = f"Цена {amount} {base_currency} в {quote_currency}: {price} {quote_currency}"
        bot.send_message(message.chat.id, response_message)

    except extensions.APIException as e:
        bot.send_message(message.chat.id, f"Ошибка: {str(e)}")

if __name__ == "__main__":
    bot.polling(none_stop=True, interval=0)
