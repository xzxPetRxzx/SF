#Данную работу сделал с помощью сервиса https://www.currate.ru/, т.к. функция конвертация валют в сервисе указанном
#в техзадании  стала платной, 10 долларов платить задавила жаба
import telebot
from extensions import Converter, APIException, keys
from config import TOKEN, keys

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def start(message: telebot.types.Message):
    text = 'Для начала работы введите  команду в формате: \n<имя валюты>' \
           '<в какую валюту перевести>' \
           '<количество переводимой валюты>'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text,key,))
    bot.reply_to(message, text)

@bot.message_handler(content_types = ['text',])
def answer(message: telebot.types.Message):
    values = message.text.split()
    if len(values) > 3:
        raise APIException('Слишком много параметров')
    base, quote, amount = values
    req = Converter.get_price(base, quote, amount)
    text = req
    bot.reply_to(message, text)

bot.polling()
