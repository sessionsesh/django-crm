from django.core.signals import request_finished
from django.db.models.signals import post_save
from django.dispatch import receiver

from accounts.models import User

from telegram_notifications.apps import botThread


chat_id = '231731765'

@receiver(request_finished)
def my_handler(sender, **kwargs):
    text = 'Request finished'
    botThread.telegramBot.sendMessage(chat_id, text)
    print('SIGNAL_REQUEST_SENT')

@receiver(post_save)
def my_db_handler(sender, instance, **kwargs):
    text='DB CHANGED'
    botThread.telegramBot.sendMessage(chat_id, text)
    print('SIGNAL_DB_SENT')