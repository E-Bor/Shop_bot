from aiogram.dispatcher.filters.state import State, StatesGroup


class UserState(StatesGroup):
    """state for change user category"""
    current_state = State()


