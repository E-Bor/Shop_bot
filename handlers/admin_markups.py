from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton,ReplyKeyboardMarkup,KeyboardButton,ReplyKeyboardRemove
from bot_logger.BotLogger import logger


# creating inline keyboard for admin
def create_admin_inline_markup(titles: list, back=None):
    if not isinstance(titles, list):
        titles = [titles]
    buttons = [InlineKeyboardButton(text=f"{i}", callback_data=f"{i}") for i in titles]
    main_markup = InlineKeyboardMarkup(row_width=2)
    main_markup.add(*buttons)
    logger.info("Markup was created")
    return main_markup


# creating keyboard for admin
def create_admin_markup():
    mk = ReplyKeyboardMarkup(resize_keyboard=True)
    mk.add(KeyboardButton("Добавить товар"), KeyboardButton("Добавить категорию"), KeyboardButton(
        "Удалить"), KeyboardButton("Статистика")).row(
        KeyboardButton("Закончить"), KeyboardButton("Начать"), KeyboardButton("Назад"),)
    return mk

