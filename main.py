import telebot
from config import *
from extensions import Converter, ApiException

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands = ['start', 'help'])
def start(message: telebot.types.Message):
    text = f"Добрый день!\n Чтобы узнать доступные валюты для конвертации введите /values\nЧтобы узнать стоимость валюты введите: \nназвание валюты, которая вам нужна \nназвание валюты, из которой совершается перевод \nсумма перевода.\nДля получении информации о работе бота введите /start или /help"
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands = ['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for i in exchanges.keys():
        text = '\n'.join((text, i))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text'])
def converter(message: telebot.types.Message):
    try:
        base, quote, amount = message.text.split()
    except ValueError as e:
        bot.reply_to(message, "Неверное количество параметров!")
    try:
        new_price = Converter.get_price(base, quote, amount)
        bot.reply_to(message, f"Цена {amount} {base} в {quote}: {new_price}")
    except ApiException as e:
        bot.reply_to(message, f"Ошибка в команде:\n{e}")

bot.polling()