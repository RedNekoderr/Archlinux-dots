from aiogram import Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher
from os import getenv
from dotenv import load_dotenv
from dotenv import find_dotenv

load_dotenv(find_dotenv())
TOKEN = getenv('TOKEN')

if isinstance(TOKEN, str):
    storage = MemoryStorage()
    bot: Bot = Bot(token=TOKEN)
    dp: Dispatcher = Dispatcher(bot, storage=storage)
else:
    print('!!!Cannot access token!!!')
