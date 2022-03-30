import requests
import telebot

#чтение токена из файла TOKEN.txt
with open('TOKEN.txt','r') as f:
    TOKEN = f.readline()

#TOKEN = '5222765611:AAFz8nvJeqAPqeYeWyxXkwhfPYzXtMu7EQI'
bot = telebot.TeleBot(TOKEN)

keys = {
    'эфириум':'ETH',
    'биткоин':'BTC',
    'доллар':'USD',
    'евро':'EUR',
    'рубль':'RUB'
}

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

@bot.message_handler(type = ['text'])
def answer(message: telebot.types.Message):
    pass

bot.polling()
