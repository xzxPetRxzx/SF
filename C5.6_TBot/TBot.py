#Данную работу сделал с помощью сервиса https://www.currate.ru/, т.к. функция конвертация валют в сервисе указанном
#в техзадании  стала платной, 10 долларов платить задавила жаба
import telebot
from extensions import Converter, APIException, keys
from config import TOKEN, keys

bot = telebot.TeleBot(TOKEN)

#Команды старт/хэлп
@bot.message_handler(commands=['start', 'help'])
def start(message: telebot.types.Message):
    text = 'Для начала работы введите  команду в формате: \n<имя валюты, цену которой он хочет узнать>' \
           '<имя валюты, в которой надо узнать цену первой валюты>' \
           '<количество первой валюты>'
    bot.reply_to(message, text)

#Команда вальюс
@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text,key,))
    bot.reply_to(message, text)

#Обработчик текста
@bot.message_handler(content_types = ['text',])
def answer(message: telebot.types.Message):
    values = message.text.lower().split()
#отлов ошибок
    try:
        if len(values) > 3:
            raise APIException('Слишком много параметров')
        base, quote, amount = values
        req = Converter.get_price(base, quote, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя:\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду:\n{e}')
    else:
        text = f'{amount} {base} в {quote} = {req}'
        bot.reply_to(message, text)

bot.polling()
