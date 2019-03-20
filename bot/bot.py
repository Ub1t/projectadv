from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import apiai
import json
import requests
import pyowm
import datetime

TOKEN = "789571978:AAFC5acFj6-GRIfDOXgo2B5HIgF0L1srqRM"
updater = Updater(token='{}'.format(TOKEN))
dispatcher = updater.dispatcher


def start_command(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text='Привет, давай пообщаемся?')


def weather_command(bot, update, args):
    from googletrans import Translator
    owm = pyowm.OWM('0c9f3c052f1d81b7062750ff0926f345')
    city = "".join(str(x) for x in args)
    translator = Translator()
    city_en = translator.translate(city, dest='en')
    observation = owm.weather_at_place(city_en.text)

    w = observation.get_weather()
    wind = w.get_wind()
    temp = w.get_temperature('celsius')

    convert_temp_min = temp.get('temp_min')
    convert_temp_max = temp.get('temp_max')
    convert_temp = temp.get('temp')
    convert_wind = wind.get('speed')

    text_temp_min = str(convert_temp_min)
    text_temp_max = str(convert_temp_max)
    text_temp = str(convert_temp)
    text_wind = str(convert_wind)

    weekday_num = datetime.datetime.today().weekday()
    weekday = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
    r = '{}:{}'.format(datetime.datetime.today().hour, datetime.datetime.today().minute)

    if text_temp and text_wind:
        bot.send_message(chat_id=update.message.chat_id, text="""{}
{}""".format(weekday[weekday_num], r))
        bot.send_message(chat_id=update.message.chat_id, text='Температура сейчас: {}℃'.format(text_temp))
        bot.send_message(chat_id=update.message.chat_id, text='Максимальная температура: {}℃'.format(text_temp_max))
        bot.send_message(chat_id=update.message.chat_id, text='Минимальная температура: {}℃'.format(text_temp_min))
        bot.send_message(chat_id=update.message.chat_id, text='Скорость ветра: {}м/с'.format(text_wind))

    else:
        bot.send_message(chat_id=update.message.chat_id, text='Я Вас не совсем понял!')


def text_message(bot, update):
    request = apiai.ApiAI('5c3fdcc91e2f42ed952f4f5710d30fc7').text_request()
    request.lang = 'ru'
    request.session_id = 'AdvProjectWeather'
    request.query = update.message.text
    response_json = json.loads(request.getresponse().read().decode('utf-8'))
    response = response_json['result']['fulfillment']['speech']
    if response:
        bot.send_message(chat_id=update.message.chat_id, text=response)
    else:
        bot.send_message(chat_id=update.message.chat_id, text='Я Вас не совсем понял!')


start_command_handler = CommandHandler('start', start_command)
weather_command_handler = CommandHandler('weather', weather_command, pass_args=True)
text_message_handler = MessageHandler(Filters.text, text_message)

dp = updater.dispatcher
dp.add_handler(start_command_handler)
dp.add_handler(weather_command_handler)
dp.add_handler(text_message_handler)

updater.start_polling(clean=True)

updater.idle()