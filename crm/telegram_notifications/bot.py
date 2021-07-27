import requests
from dataclasses import dataclass
import time
import threading as th
import json
import os
import sys
from django.conf import settings
from accounts.models import User
"""
Module for Telegram API handling
"""


@dataclass
class TelegramAPI:
    """Class for keeping Telegram API urls without query string for bot functional"""
    message_url: str = 'https://api.telegram.org/bot/sendMessage'
    updates_url: str = 'https://api.telegram.org/bot/getUpdates'

    def __init__(self, token):
        self.message_url = self.__insert_str_after_bot_part(self.message_url, token)
        self.updates_url = self.__insert_str_after_bot_part(self.updates_url, token)
    
    def __insert_str_after_bot_part(self, str1, str2):
        index = str1.find('bot')
        str1 = str1[:index + 3] + str2 + str1[index + 3:]   # TODO: redesign
        return str1

class QSGen:
    """Class for generating query strings"""

    @staticmethod
    def generate(url: str, parameters: dict):
        """ Appends generate query string to the url"""

        url += '?'
        for key, value in parameters.items():
            parameter = f'{key}={value}&'
            url += parameter
        return url

class TelegramBot:
    class GetUpdatesResponseWrapper:
        """Wrapper around getUpdates method to make interactions with API more user-friendly"""

        def __init__(self, response):
            self.__response_json = response.json()

        def ok(self):
            """Returns True if request was successfull, else return False."""
            return self.__response_json['ok']
        
        def result(self):
            """Returns array of dicts with each user message sent to bot.""" 
            return self.__response_json['result']

    @dataclass
    class UserMessage:
        """Stores main fields of message sent by a user to the bot"""
        chat_id: int
        first_name: str
        username: str
        date: int

    def __init__(self, bot_token, listening = False):
        self.listening = listening
        self.__token = bot_token
        self.__telegram_api = TelegramAPI(bot_token)

    # LOW LEVEL METHODS
    def sendMessage(self, chatId, text):
        parameters = {'chat_id':chatId,'text':text}
        url = QSGen.generate(self.__telegram_api.message_url, parameters)
        response = requests.get(url)
        return requests.get(url)

    def getUpdates(self):
        url = self.__telegram_api.updates_url
        response = requests.get(url)
        return response
    # END OF LOW LEVEL METHODS


    # HIGH LEVEL METHODS
    def getUserMessages(self):
        json_list = self.GetUpdatesResponseWrapper(self.getUpdates()).result()
        py_list = list()
        for each in json_list:
            date = each['message']['date']
            tmp_chat = each['message']['chat']
            chat_id = tmp_chat['id']
            username = tmp_chat['username']
            first_name = tmp_chat['first_name'] 

            py_list.append(self.UserMessage(chat_id, first_name, username, date))
        return py_list
    # END OF HIGH LEVEL METHODS

class BotLongPollThread(th.Thread):
        """
        Thread that handles Telegram Bot income messages
        """

        def __init__(self, bot_token, running=True, daemon=True):
            super(BotLongPollThread, self).__init__()
            self.telegramBot = TelegramBot(bot_token)
            self.running = running
            self.daemon = daemon # allows to use 'ctrl+c' to close process

        def __is_user_in_db(self, chatId):
            is_user_in_db = User.objects.filter(telegram_id=chatId).exists()
            return is_user_in_db
    

        def run(self):
            print('|Telegram notification module is running|')
            while self.running:
                # Getting messages from users
                for msg in self.telegramBot.getUserMessages():
                    chatId = msg.chat_id
                    if self.__is_user_in_db(chatId):
                        self.telegramBot.sendMessage(chatId, 'You already have sent your crm data to us.')
                    else:
                        self.telegramBot.sendMessage(chatId, 'Please, send your crm data to us.')    

                print(self.telegramBot.getUserMessages()) 
                time.sleep(5) # without it doesn't work
if __name__ == "__main__":
    from dotenv import load_dotenv
    from os import environ
    load_dotenv()
    bot_token = environ['BOT_TOKEN']
    bot = TelegramBot(bot_token, True)
    print(bot.getUserMessages())