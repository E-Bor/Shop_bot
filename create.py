from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher, storage
from config import TOKEN
from aiogram.contrib.fsm_storage.memory import MemoryStorage

"""Файл для избежаний ошибок импорта объектов класса Bot, dispatcher"""

storage = MemoryStorage()

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage= storage)