from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def create_inline_markup(titles: list):
    buttons = [InlineKeyboardButton(text=f"{i}", callback_data=f"{i}") for i in titles]
    main_markup = InlineKeyboardMarkup(row_width=2)
    main_markup.add(*buttons)
    return main_markup
