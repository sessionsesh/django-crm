from django.apps import AppConfig
import threading as th
import time
import sys

class BotLongPollThread(th.Thread):
    """
    Thread that handles Telegram Bot income messages
    """
    def __init__(self, running=True, daemon=True):
        super(BotLongPollThread, self).__init__()
        self.running = running
        self.daemon = daemon # allows to use 'ctrl+c' to close process

    def run(self):
        print('|Telegram notification module is running|')
        while(self.running):
            # Bot code
            time.sleep(0)# without it doesn't work

    def setRunning(self, value):
        self.running = value

class TelegramNotificationsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'telegram_notifications'

    def ready(self):
        import telegram_notifications.signals   # importing signals
        if 'runserver' in sys.argv:
            botThread = BotLongPollThread()
            #botThread.start()

        return super(TelegramNotificationsConfig, self).ready()
