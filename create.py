from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from config import TOKEN

"""Файл для избежаний ошибок импорта объектов класса Bot, dispatcher"""

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)