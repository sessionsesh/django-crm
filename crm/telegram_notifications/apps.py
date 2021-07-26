from django.apps import AppConfig
import threading as th
import time
import sys
from dotenv import load_dotenv
from os import environ
from telegram_notifications.bot import TelegramBot


class BotLongPollThread(th.Thread):
    """
    Thread that handles Telegram Bot income messages
    """

    def __init__(self, bot_token, running=True, daemon=True):
        super(BotLongPollThread, self).__init__()
        self.telegramBot = TelegramBot(bot_token)
        self.running = running
        self.daemon = daemon # allows to use 'ctrl+c' to close process

    def run(self):
        print('|Telegram notification module is running|')
        while self.running:
            print(self.telegramBot.getUpdates()) # without it doesn't work
            time.sleep(5)

    def setRunning(self, value):
        self.running = value

load_dotenv()
botThread = BotLongPollThread(environ['BOT_TOKEN']) # sharing between modules

class TelegramNotificationsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'telegram_notifications'

    def ready(self):
        import telegram_notifications.signals   # importing signals

        if 'runserver' in sys.argv:
            botThread.start()

        return super(TelegramNotificationsConfig, self).ready()
