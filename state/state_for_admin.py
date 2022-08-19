from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State,StatesGroup


class CategoryState(StatesGroup):
    name = State()
    path = State()

