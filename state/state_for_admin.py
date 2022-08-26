from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State,StatesGroup
from unicodedata import category


class CategoryState(StatesGroup):
    name = State()
    path = State()


class ItemState(StatesGroup):
    new_files_data = State()
    directory = State()
    file = State()
    file_name = State
    pre_view = State()
    pre_view_name = State()


class Items(StatesGroup):
    file = State()


class CheckStat(StatesGroup):
    category = State()
