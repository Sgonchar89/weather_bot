import datetime as dt
import logging
import os

import requests
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from dotenv import load_dotenv

load_dotenv()

OPENWEATHER_TOKEN = os.environ.get('OPENWEATHER_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
file_log = logging.FileHandler('program.log')
console_out = logging.StreamHandler()

logging.basicConfig(handlers=(file_log, console_out),
                    format='%(asctime)s, %(levelname)s,'
                           ' %(message)s, %(name)s', level=logging.DEBUG)


bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.reply("Hi! Text me the name of your town and I'll show you "
                        "the weather!")


@dp.message_handler()
async def get_weather(message: types.Message):

    emoji_code = {
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
            f"http://api.openweathermap.org/data/2.5/weather?q={message.text}"
            f"&appid={OPENWEATHER_TOKEN}&units=metric")
        data = request.json()
        city = data['name']
        cur_weather = data['main']['temp']
        weather_icon = data['weather'][0]['main']
        if weather_icon in emoji_code:
            icon = emoji_code[weather_icon]
        else:
            icon = "Look out the window"
        humidity = data['main']['humidity']
        pressure = data['main']['pressure']
        wind = data['wind']['speed']  # !!
        sunrise_timestamp = (dt.datetime.fromtimestamp(
            data['sys']['sunrise']).strftime('%H:%M:%S'))
        sunset_timestamp = (dt.datetime.fromtimestamp(
            data['sys']['sunset']).strftime('%H:%M:%S'))
        daylength = (dt.datetime.fromtimestamp(data['sys']['sunset'])
                     - dt.datetime.fromtimestamp(data['sys']['sunrise']))

        await message.reply(f"*{dt.datetime.now().strftime('%Y-%m-%d %H:%M')}"
                            f"*\nWeather in {city}: {icon}\n"
                            f"Temperature: {cur_weather}C°\n"
                            f"Wind: {wind} km/h\n"
                            f"Humidity: {humidity} %\n"
                            f"Pressure: {pressure} mm Hg\n"
                            f"Sunrise: {sunrise_timestamp}\n"
                            f"Sunset: {sunset_timestamp}\n"
                            f"Day length: {daylength}\n")
    except:
        await message.reply('\U00002620 Check City name \U00002620')

if __name__ == '__main__':
    executor.start_polling(dp)
