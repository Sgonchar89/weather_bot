import logging
import os
import time
import datetime as dt

import requests
from requests.exceptions import RequestException
import telegram
from dotenv import load_dotenv
from json import JSONDecodeError
from pprint import pprint
from config import openweather_token
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

load_dotenv()

# PRAKTIKUM_URL = 'https://praktikum.yandex.ru/api/user_api/homework_statuses/'
# PRAKTIKUM_TOKEN = os.getenv('PRAKTIKUM_TOKEN')
#TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
#CHAT_ID = os.getenv('CHAT_ID')
URL = 'http://wttr.in/vancouver?0T'
file_log = logging.FileHandler('program.log')
console_out = logging.StreamHandler()

logging.basicConfig(handlers=(file_log, console_out),
                    format='%(asctime)s, %(levelname)s, %(message)s, %(name)s',
                    level=logging.DEBUG)

HOMEWORK_VERDICTS = {
    'rejected': 'К сожалению в работе нашлись ошибки.',
    'reviewing': 'Работа взята в ревью.',
    'approved': 'Ревьюеру всё понравилось, '
                 'можно приступать к следующему уроку.',
}

bot = Bot(token=os.environ.get('TELEGRAM_TOKEN'))
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.reply("Hi! Text me the name of your town and I'll show you "
                        "the weather!")


def get_weather (city, openweather_token):

    Emoji_code = {
        "Clear": "Clear \U00002600",
        "Clouds": "Clouds \U00002601",
        "Rain": "Rain \U00002614",
        "Drizzle": "Drizzle \U00002614",
        "Thunderstorm": "Thunderstorm \U000026A1",
        "Snow": "Snow \U0001F328",
        "Mist": "Fog \U0001F32B",
    }

    try:
        request = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid="
            f"{openweather_token}&units=metric")
        data = request.json()
        pprint(data)

        city = data['name']
        cur_weather = data['main']['temp']
        weather_icon = data['weather'][0]['main']
        if weather_icon in Emoji_code:
            icon = Emoji_code[weather_icon]
        else:
            icon = "Look out the window"
        humidity = data['main']['humidity']
        pressure = data['main']['pressure']
        wind = data['wind']['speed'] #!!
        sunrise_timestamp = (dt.datetime.fromtimestamp(
            data['sys']['sunrise']).strftime('%H:%M:%S'))
        sunset_timestamp = (dt.datetime.fromtimestamp(
            data['sys']['sunset']).strftime('%H:%M:%S'))
        daylength = (dt.datetime.fromtimestamp(data['sys']['sunset']) -
                     dt.datetime.fromtimestamp(data['sys']['sunrise']))

        print(f"***{dt.datetime.now().strftime('%Y-%m-%d %H:%M')}***\n"
              f"Weather in {city}: {icon}\nTemperature: {cur_weather}C°\n"
              f"Wind: {wind} km/h\n"
              f"Humidity: {humidity} %\nPressure: {pressure} mm Hg\n"
              f"Sunrise: {sunrise_timestamp}\nSunset: {sunset_timestamp}\n"
              f"Day length: {daylength}\n")

    except Exception:
        print(Exception)
        print('Check City name')

def main():
    city = input('Enter city:')
    get_weather(city, openweather_token)


# def send_message(message, bot_client):
#     """Функция возвращает данные для отправки сообщения."""
#     return bot_client.send_message(chat_id=CHAT_ID, text=message)
#
#
# def main():
#     """Основная вычислительная функция."""
#     current_timestamp = dt.datetime.now().time()
#     bot_client = telegram.Bot(token=TELEGRAM_TOKEN)
#     logging.debug('Бот запущен')
#
#     message = requests.get(URL)  # выполните HTTP-запрос
#     if dt.time(19,35) <= current_timestamp <= dt.time(19,50):
#         logging.info('Отправляем сообщение в телегу')
#         send_message(message.text, bot_client)
#         logging.info('Сообщение отправлено')
#     # while True:
#     #     try:
#     #         new_homework = get_homework_statuses(current_timestamp)
#     #         if new_homework.get('homeworks'):
#     #             homework_data = new_homework.get('homeworks')[0]
#     #             message = parse_homework_status(homework_data)
#     #             logging.info('Отправляем сообщение в телегу')
#     #             send_message(message, bot_client)
#     #             logging.info('Сообщение отправлено')
#     #         current_timestamp = new_homework.get('current_date',
#     #                                              int(time.time()))
#     # while True:
#     #     try:
#     #         new_homework = get_homework_statuses(current_timestamp)
#     #         if new_homework.get('homeworks'):
#     #             homework_data = new_homework.get('homeworks')[0]
#     #             message = parse_homework_status(homework_data)
#     #             logging.info('Отправляем сообщение в телегу')
#     #             send_message(message, bot_client)
#     #             logging.info('Сообщение отправлено')
#     #         current_timestamp = new_homework.get('current_date',
#     #                                              int(time.time()))
#     #     except Exception as e:
#     #         logging.error(f'Бот столкнулся с ошибкой: {e}')
#     #
#     #     finally:
#     #         time.sleep(1200)
#
#
if __name__ == '__main__':
    main()
