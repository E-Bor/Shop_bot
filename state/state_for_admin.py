from aiogram.dispatcher.filters.state import State, StatesGroup


class CategoryState(StatesGroup):
    """class for category state"""
    name = State()
    path = State()


class ItemState(StatesGroup):
    """class for item info state"""
    new_files_data = State()
    directory = State()
    file = State()
    file_name = State
    pre_view = State()
    pre_view_name = State()


class Items(StatesGroup):
    """class for item buy"""
    file = State()


class CheckStat(StatesGroup):
    """class for get stats"""
    category = State()
