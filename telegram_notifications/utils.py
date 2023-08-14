import requests
from django.conf import settings

from .bot_commands import TelegramBotCommands


def get_last_bot_command(telegram_username: str) -> TelegramBotCommands:
    response = requests.get(
        settings.TELEGRAM_BOT_API_URL +
        'getUpdates?allowed_updates=["message"]'
    )
    updates = response.json()['result']

    messages = []
    for update in updates:
        from_user = update['message']['from']['username']
        if from_user != telegram_username:
            continue
        text = update['message']['text']
        messages.append(text)

    last_command = None
    for message in messages[::-1]:
        if message in TelegramBotCommands.values():
            last_command = TelegramBotCommands(message)
            break

    return last_command
