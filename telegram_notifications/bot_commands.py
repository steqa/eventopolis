from enum import Enum, unique


@unique
class TelegramBotCommands(Enum):
    start = '/start'
    stop = '/stop'

    @classmethod
    def values(cls):
        return list(map(lambda c: c.value, cls))
