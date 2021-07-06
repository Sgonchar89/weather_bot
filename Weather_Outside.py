import logging
import os
import time
import datetime as dt

import requests
from requests.exceptions import RequestException
import telegram
from dotenv import load_dotenv
from json import JSONDecodeError

load_dotenv()

# PRAKTIKUM_URL = 'https://praktikum.yandex.ru/api/user_api/homework_statuses/'
# PRAKTIKUM_TOKEN = os.getenv('PRAKTIKUM_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')
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


# def parse_homework_status(homework):
#     """Функция возвращает текущий статус ревью проекта."""
#     try:
#         homework_name = homework['homework_name']
#         homework_status = homework['status']
#         if homework_status in HOMEWORK_VERDICTS:
#             return (f'У вас проверили работу "{homework_name}"!\n'
#                     f'\n{HOMEWORK_VERDICTS[homework_status]}')
#         else:
#             return f'Получен неизвестный статус работы "{homework_status }"'
#     except KeyError as e:
#         logging.error(f'Бот столкнулся с ошибкой: {e}')
#         raise


# def get_homework_statuses(current_timestamp):
#     """Функция возвращает json() со списком домашних работ от текущей даты."""
#     current_timestamp = current_timestamp or int(time.time())
#     headers = {'Authorization': f'OAuth {PRAKTIKUM_TOKEN}'}
#     params = {'from_date': 0}
#     try:
#         homework_statuses = requests.get(
#             url=PRAKTIKUM_URL,
#             headers=headers,
#             params=params,
#         )
#         return homework_statuses.json()
#     except (RequestException, JSONDecodeError):
#         raise
#

def send_message(message, bot_client):
    """Функция возвращает данные для отправки сообщения."""
    return bot_client.send_message(chat_id=CHAT_ID, text=message)


def main():
    """Основная вычислительная функция."""
    current_timestamp = dt.datetime.now().time()
    bot_client = telegram.Bot(token=TELEGRAM_TOKEN)
    logging.debug('Бот запущен')

    message = requests.get(URL)  # выполните HTTP-запрос
    if dt.time(21,48) <= current_timestamp <= dt.time(21,55):
        logging.info('Отправляем сообщение в телегу')
        send_message(message.text, bot_client)
        logging.info('Сообщение отправлено')
    # while True:
    #     try:
    #         new_homework = get_homework_statuses(current_timestamp)
    #         if new_homework.get('homeworks'):
    #             homework_data = new_homework.get('homeworks')[0]
    #             message = parse_homework_status(homework_data)
    #             logging.info('Отправляем сообщение в телегу')
    #             send_message(message, bot_client)
    #             logging.info('Сообщение отправлено')
    #         current_timestamp = new_homework.get('current_date',
    #                                              int(time.time()))
    # while True:
    #     try:
    #         new_homework = get_homework_statuses(current_timestamp)
    #         if new_homework.get('homeworks'):
    #             homework_data = new_homework.get('homeworks')[0]
    #             message = parse_homework_status(homework_data)
    #             logging.info('Отправляем сообщение в телегу')
    #             send_message(message, bot_client)
    #             logging.info('Сообщение отправлено')
    #         current_timestamp = new_homework.get('current_date',
    #                                              int(time.time()))
    #     except Exception as e:
    #         logging.error(f'Бот столкнулся с ошибкой: {e}')
    #
    #     finally:
    #         time.sleep(1200)


if __name__ == '__main__':
    main()
