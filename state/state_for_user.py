from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State,StatesGroup


class UserState(StatesGroup):
    current_state = State()
