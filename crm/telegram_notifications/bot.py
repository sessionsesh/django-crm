import requests
from dataclasses import dataclass
import time
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
    def __init__(self, bot_token, listening = False):
        self.listening = listening
        self.__token = bot_token
        self.__telegram_api = TelegramAPI(bot_token)

    def sendMessage(self, chatId, text):
        parameters = {'chat_id':chatId,'text':text}
        url = QSGen.generate(self.__telegram_api.message_url, parameters)
        print(url)
        response = requests.get(url)
        print(response.text)
        return requests.get(url)

    def getUpdates(self):
        url = self.__telegram_api.updates_url
        response = requests.get(url)
        return response
    
    def setListening(self, listening: bool):
        self.listening = listening
    

    # def longPoll(self):
    #     while(self.listening):
    #         print(self.getUpdates())
    #         time.sleep(5)
            



# from dotenv import load_dotenv
# from os import environ
# load_dotenv()
# bot_token = environ['BOT_TOKEN']
# bot = TelegramBot(bot_token, True)
# bot.longPoll()