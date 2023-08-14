import json

from django.http.response import JsonResponse

from eventopolis.utils import JsonRedirectResponse
from .bot_commands import TelegramBotCommands
from .utils import get_last_bot_command


def enable_telegram_bot(request):
    user = request.user
    if not user.telegram_username:
        data = {'push': {'message': 'Не указано имя пользователя Telegram.'}}
        return JsonResponse(data=json.dumps(data), status=400, safe=False)

    telegram_username = user.telegram_username

    last_bot_command = get_last_bot_command(telegram_username)
    if last_bot_command is TelegramBotCommands.start:
        user.telegram_notifications = True
        user.save()
        return JsonRedirectResponse(url='user-settings-notifications')
    else:
        data = {
            'push': {
                'message': 'Не удалось включить уведомления! '
                           'Возможно вы неверно указали имя пользователя '
                           'Telegram или не активировали бота.'
            }
        }
        return JsonResponse(data=json.dumps(data), status=400, safe=False)


def disable_telegram_bot(request):
    user = request.user
    if not user.telegram_username:
        data = {'push': {'message': 'Не указано имя пользователя Telegram.'}}
        return JsonResponse(data=json.dumps(data), status=400, safe=False)

    user.telegram_notifications = False
    user.save()
    return JsonRedirectResponse(url='user-settings-notifications')
