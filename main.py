import rq
import telebot
from telebot import types

from datetime import date
import datetime

from api_token import *

import random
import requests

USD = float(rq.check_currency_usd().replace(',', '.'))
EURO = float(rq.check_currency_eur().replace(',', '.'))

bot = telebot.TeleBot(bot_api)


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    conventor = types.KeyboardButton('Конвертирование валюты')
    weather = types.KeyboardButton('Погода в городе')
    choise = types.KeyboardButton('Подбросить монетку')

    markup.add(conventor, weather, choise)

    bot.send_message(message.chat.id, 'Главное меню ', reply_markup=markup)


@bot.message_handler(content_types='text')
def bot_message(message):
    if message.text == 'Конвертирование валюты':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        usd_conv = types.KeyboardButton('UAH > USD')
        eur_conv = types.KeyboardButton('UAH > EURO')
        back = types.KeyboardButton('Выйти')
        markup.add(usd_conv, eur_conv, back)
        msg = bot.send_message(message.chat.id, 'На что меняем?', reply_markup=markup)
        bot.register_next_step_handler(msg, currency)

    elif message.text == 'Подбросить монетку':
        bot.send_message(message.chat.id, coin_flip())

    elif message.text == 'Погода в городе':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        back = types.KeyboardButton('Меню')
        markup.add(back)
        msg = bot.send_message(message.chat.id, 'Введите ваш город', reply_markup=markup)
        bot.register_next_step_handler(msg, get_weather)
    elif message.text == 'Выйти':
        start(message)
    else:
        bot.send_message(message.chat.id, 'Выберите пунк с меню')


@bot.message_handler(content_types=['text'])
def get_weather(message):
    code_to_smile = {
        'Clear': 'Ясно \U00002600',
        'Clouds': 'Облачно \U00002601',
        'Rain': 'Дождь \U00002614',
        'Drizzle': 'Дождь \U00002614',
        'Thunderstorm': 'Гроза \U000026A1',
        'Mist': 'Туман \U0001F328',
        'Snow': 'Снег \U0001F32B'
    }
    if message.text:
        try:
            wea = requests.get(
                f'https://api.openweathermap.org/data/2.5/weather?q={message.text}&units=metric&appid=dc1becbc9e406dc21a63e086658afa7e')
            data = wea.json()
            city = data.get('name')
            temp = data['main']['temp']
            wind = data['wind']['speed']
            weather_description = data['weather'][0]['main']
            if weather_description in code_to_smile:
                wd = code_to_smile[weather_description]
            else:
                wd = 'Непонятная погода'
            sunrise_timeup = datetime.datetime.fromtimestamp(data['sys']['sunrise']).strftime("%H:%M:%S")
            sunset_timeup = datetime.datetime.fromtimestamp(data['sys']['sunset']).strftime("%H:%M:%S")
            bot.send_message(message.chat.id, f'Сегодня {date.today().strftime("%B %d, %Y")}\n'
                  f'Температура воздуха в городе {city} - {temp}℃ - {wd}\n'
                  f'Скорость ветра  - {wind}M/c\n'
                  f'Восход солнца в - {sunrise_timeup}\n'
                  f'Закат в {sunset_timeup}\n')
            start(message)
        except Exception:
            bot.send_message(message.chat.id, 'Город не распознан повторите ввод')
            start(message)
    elif message.text == 'Меню':
        start(message)


@bot.message_handler(content_types=['text'])
def currency(message):
    if message.text == 'UAH > EURO':
        msg = bot.send_message(message.chat.id, 'Сколько грн хотите обменять на € (НБУ)')
        bot.register_next_step_handler(msg, euro)
    elif message.text == 'UAH > USD':
        msg = bot.send_message(message.chat.id, 'Сколько грн хотите обменять на $ (НБУ)')
        bot.register_next_step_handler(msg, dollar)
    else:
        start(message)
    # else:
        # msg = bot.send_message(message.chat.id, 'Введите число')
        # bot.register_next_step_handler(msg, )


@bot.message_handler()
def dollar(message):
    try:
        sumq = str(format(float(message.text) / USD, '.2f'))
        msg = bot.send_message(message.chat.id, message.text + ' Uah is ' + sumq + ' USD')
        bot.register_next_step_handler(msg, currency)
    except ValueError:
        bot.send_message(message.chat.id, 'Число не корректно')
        start(message)


@bot.message_handler()
def euro(message):
    try:
        sumq = str(format(float(message.text) / EURO, '.2f'))
        msg = bot.send_message(message.chat.id, message.text + ' Uah is ' + sumq + ' EURO')
        bot.register_next_step_handler(msg, currency)

    except ValueError:
        bot.send_message(message.chat.id, 'Введите корректную сумму')
        start(message)


def coin_flip():
    if random.randint(0, 1):
        coin = 'Бросок успешный, Орёл'
    else:
        coin = 'Хороший бросок, Решка'
    return coin


bot.polling(none_stop=True)

