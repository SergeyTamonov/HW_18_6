import telebot
from config import keys, TOKEN
from utils import ExchangeException, Exchange


bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def start_help(message: telebot.types.Message):
    text = 'Чтобы начать работу, введите команду боту в следующем формате:\n<имя валюты, цену которой вы хотите узнать> \
<имя валюты, в которой надо узнать цену первой валюты> \
<количество первой валюты>\nУвидеть список всех доступных валют: /values'

    bot.reply_to(message, text)

@bot.message_handler(commands = ["values"])
def values(message: telebot.types.Message):
    text = "Информация о доступных валютах:"
    for key in keys.keys():
        text = "\n".join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types = ["text", ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(" ")
        if len(values) != 3:
            raise ExchangeException("Неверно введены параметры.")

        quote, base, amount = values
        total_base = Exchange.convert(quote, base, amount)
    except ExchangeException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exchange as e:
        bot.reply_to(message, f'Что-то пошло не так с {e}')
    else:
        text = f"Стоимость {amount} {quote} в {base} = {total_base}"
        bot.send_message(message.chat.id, text)


bot.polling()