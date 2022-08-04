from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton,ReplyKeyboardMarkup,KeyboardButton,ReplyKeyboardRemove
from bot_logger.BotLogger import logger


def create_inline_markup(titles: list,back=None):
    if not isinstance(titles,list):
        titles = [titles]
    buttons = [InlineKeyboardButton(text=f"{i}", callback_data=f"{i}") for i in titles]
    main_markup = InlineKeyboardMarkup(row_width=2)
    main_markup.add(*buttons)
    logger.info("Markup was created")
    return main_markup

def create_markup():
    mk = ReplyKeyboardMarkup(resize_keyboard=True)
    mk.add(KeyboardButton("Помощь"), KeyboardButton("Начать")).row(KeyboardButton("Закончить"),KeyboardButton("Назад"))
    return mk

