from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher, storage
from config import TOKEN
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio

"""Файл для избежаний ошибок импорта объектов класса Bot, dispatcher"""
# loop = asyncio.get_event_loop()
storage = MemoryStorage()

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage= storage)