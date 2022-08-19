from aiogram import Bot, types, Dispatcher
from aiogram.dispatcher import FSMContext

from bot_logger.BotLogger import logger
from create import dp, bot
from handlers import create_admin_inline_markup, create_admin_markup, create_inline_markup
from shop import category_object
from shop.payments import get_data_for_payment, config_payments
from state import UserState, CategoryState
from aiogram.types.message import ContentTypes
from .userhandlers import back_to_category

ID = None

async def start_administrate(message: types.Message):
    global ID
    ID = message.from_user.id
    await bot.send_message(ID, text="Привет, мой администратор!, нажмите на /start")

async def stop_administrate(message: types.Message):
    global ID
    await bot.send_message(ID, text="До встречи, мой администратор")
    ID = None



async def command_start(message: types.Message):
    await message.delete()
    await bot.send_message(message.from_user.id, """
    Добро пожаловать админ!
    """,reply_markup=create_admin_markup())

async def command_delete(message: types.Message, state):
    # await message.delete()
    update_fsm = await state.get_data()
    # print(update_fsm)
    a = update_fsm["current_state"].copy()
    # print(category_object.dict)
    category_object.del_partition(a)
    await back_to_category(message, state)


async def command_add_category(message: types.Message, state: FSMContext):
    old_state = await state.get_data()
    a = old_state["current_state"].copy()
    await state.finish()
    await CategoryState.name.set()
    new_state = Dispatcher.get_current().current_state()
    await new_state.update_data(path=a)
    await message.answer("Введите название категории")


async def add_category(message: types.Message, state: FSMContext):
    old_state = await state.get_data()
    path = old_state["path"].copy()
    name_new_category = message.text
    await state.finish()
    await UserState.current_state.set()
    state = Dispatcher.get_current().current_state()
    await state.update_data(current_state=path)
    category_object.add_category(name_new_category, path)
    await message.answer("Категория успешно добавлена")
    cat = category_object.view(path)
    # Not end categories
    if isinstance(cat, list):
        # print(cat)
        markup = create_inline_markup(cat)
        await message.answer("Выбери категорию", reply_markup=markup)







def register_handler_admins(dp : Dispatcher):
    dp.register_message_handler(start_administrate, commands="start_administrate", is_chat_admin=True)
    dp.register_message_handler(stop_administrate, commands="stop_administrate", is_chat_admin=True)
    dp.register_message_handler(command_start, lambda message: message.text == "/start" and message.from_user.id == ID)
    dp.register_message_handler(command_delete, lambda message: message.text == "Удалить" and message.from_user.id == ID,
                                state=UserState.current_state)
    dp.register_message_handler(command_add_category,
                                lambda message: message.text == "Добавить категорию" and message.from_user.id == ID,
                                state=UserState.current_state)
    dp.register_message_handler(add_category, state=CategoryState.name)