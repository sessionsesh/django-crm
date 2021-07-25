import telegram as tg
import os
import sys

from dotenv import load_dotenv






load_dotenv()

# Adding django project folder to the sys.path
dirname = os.path.dirname
exec_dir = dirname(dirname(dirname(__file__)))
sys.path.append(exec_dir)
#for path in sys.path:print(path)

# Importing django mandatory stuff
import django
from django.conf import settings
from django.apps import apps
from crm.crm import settings as django_settings

# Loading django environment to access its ORM
settings.configure(default_settings=django_settings, DEBUG=True)
django.setup()

class Bot(tg.Bot):
    """
    Class for incapsualting bot api
    """
    def __init__(self):
        bot = tg.Bot(token=os.environ['BOT_TOKEN'])
    pass

class Message:
    """
    Class for structure the messages to be sent by bot to the user 
    """
    pass