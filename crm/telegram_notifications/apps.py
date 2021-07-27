from django.apps import AppConfig
import time
import sys
from dotenv import load_dotenv
from os import environ


botThread = None 

class TelegramNotificationsConfig(AppConfig):
    global botThread
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'telegram_notifications' 

    def setRunning(self, value):
        self.running = value
    def ready(self):
        from telegram_notifications.bot import TelegramBot, BotLongPollThread
        import telegram_notifications.signals   # importing signals
        load_dotenv
        botThread = BotLongPollThread(environ['BOT_TOKEN']) # sharing between modules
        if 'runserver' in sys.argv:
            botThread.start()

        return super(TelegramNotificationsConfig, self).ready()
