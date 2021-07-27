from django.core.signals import request_finished
from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.models import User
from dotenv import load_dotenv
from os import environ


# from telegram_notifications.apps import botThread
from telegram_notifications.bot import TelegramBot
load_dotenv()
bot_token = environ['BOT_TOKEN']
telegramBot = TelegramBot(bot_token)

chat_id = '231731765'

# @receiver(request_finished)
# def my_handler(sender, **kwargs):
#     text = 'Request finished'
#     telegramBot.sendMessage(chat_id, text)
#     print('SIGNAL_REQUEST_SENT')

@receiver(post_save)
def my_db_handler(sender, instance, **kwargs):
    text='DB CHANGED'
    telegramBot.sendMessage(chat_id, text)
    print('SIGNAL_DB_SENT')