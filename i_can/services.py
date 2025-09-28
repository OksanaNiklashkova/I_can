import requests
from config.settings import TELEGRAM_URL, BOT_TOKEN

def send_telegram_message(tg_id, message):
    """Сервисная функция отправки сообщения в телеграмм"""
    params = {
        'text': message,
        'chat_id': tg_id,
    }
    requests.get(f'{TELEGRAM_URL}{BOT_TOKEN}/sendMessage', params=params)