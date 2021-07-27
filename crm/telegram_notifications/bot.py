import requests
from dataclasses import dataclass
import time
import threading as th
import json
import os
import sys

if __name__ != "__main__":
    from accounts.models import User

from datetime import datetime as dt

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
            if value is not None:
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
        update_id: int
        first_name: str
        username: str
        date: int
        text: str

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

    def getUpdates(self, offset:int = None, limit:int = None, timeout:int = None, allowed_updates:list = None):
        parameters = {'offset': offset, 'limit': limit, 'timeout': timeout, 'allowed_updates': allowed_updates}
        url = QSGen.generate(self.__telegram_api.updates_url, parameters)
        response = requests.get(url)
        return response
    # END OF LOW LEVEL METHODS


    # HIGH LEVEL METHODS
    def getUserMessages(self, offset, timeout):
        json_list = self.GetUpdatesResponseWrapper(self.getUpdates(offset=offset, timeout=timeout)).result()
        py_list = list()
        for each in json_list:
            update_id = each['update_id']
            date = each['message']['date']
            tmp_chat = each['message']['chat']
            chat_id = tmp_chat['id']
            username = tmp_chat['username']
            first_name = tmp_chat['first_name']
            text = each['message']['text']

            py_list.append(self.UserMessage(chat_id, update_id, first_name, username, date, text))
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
            last_update_id = 216929435 # TODO: load from file
            locked_chats_to_send = dict() # to avoid several replies sent to a user by the bot

            print('|Telegram notification module is running|')
            while self.running:
                # Getting messages from users
                for msg in self.telegramBot.getUserMessages(offset=last_update_id + 1, timeout=10):
                    chatId = msg.chat_id
                    updateId = msg.update_id
                    
                    # tmp_lcts = locked_chats_to_send.copy()
                    # for cid, stamp in tmp_lcts.items():
                    #     if dt.now().timestamp() - stamp > 10:
                    #         locked_chats_to_send.pop(cid) # or use del

                    # Avoiding answering on all messages. Getting only last ones. Avoiding several replies to one message.
                    if (msg.update_id > last_update_id):
                        last_update_id = updateId
                        # Checking if a user is mapped with chatId
                        if self.__is_user_in_db(chatId):
                            self.telegramBot.sendMessage(chatId, 'Your orders statuses still the same')
                            print(locked_chats_to_send)

                        # Mapping user if the text which was sent is equalt to a username in database
                        else:
                            user = User.objects.filter(username=msg.text)
                            if user.exists():
                                user = user.first()
                                user.telegram_id = chatId
                                user.save()
                                self.telegramBot.sendMessage(chatId, 'You are mapped.')
                            else:
                                self.telegramBot.sendMessage(chatId, 'Please, send your crm data to us.')
                        
                        locked_chats_to_send[chatId] = dt.now().timestamp()

                time.sleep(1) # without it doesn't work

if __name__ == "__main__":
    print(dt.now().timestamp())
    from dotenv import load_dotenv
    from os import environ
    load_dotenv()
    bot_token = environ['BOT_TOKEN']
    bot = TelegramBot(bot_token, True)
    print(bot.getUserMessages())