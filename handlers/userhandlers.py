from aiogram import Bot, types, Dispatcher
from bot_logger.BotLogger import logger
from create import dp,bot
from handlers import create_inline_markup,create_markup
from shop import category_object
from state import UserState
"""file for userhandlers"""


Handlers_list = {
    1 : "start",
    2 : "Помощь"
}

#команда start
async def command_start(message: types.Message):
    await bot.send_message(message.from_user.id, """
    Добро пожаловать в магазин!
    """,reply_markup=create_markup())


#команда help
async def command_help(message: types.Message):
    await bot.send_message(message.from_user.id, f"""
    Вот список доступных комманд 
    {str(Handlers_list)}    
    """)
# command to start choose the item
async def start_shopping(message: types.Message):
    logger.ingo("user was start shop")
    await message.delete()
    await message.answer("Выбери нужную категорию", reply_markup=create_inline_markup(category_object.view()))
    await UserState.current_state.set()
    state = Dispatcher.get_current().current_state()
    await state.update_data(current_state=["start"])

# function for stop shopping. todo: create a function, That deleting messages
async def stop_shopping(message: types.Message, state):
    logger.ingo("shopping was stopped")
    await message.delete()
    data = await state.get_data()
    await state.finish()
    await message.answer("Чтобы открыть категории заного, нажмите кнопку начать")

# function to go back in categories
async def back_to_category(message: types.Message, state):
    logger.ingo("user go back in categories")
    await message.delete()
    update_fsm = await state.get_data()
    a = update_fsm["current_state"].copy()
    a.pop(-1)
    await state.reset_data()
    await state.update_data(current_state=a)
    cat = category_object.view(a[-1])
    markup = create_inline_markup(cat)
    await message.answer("Выбери категорию", reply_markup=markup)


# function for handling categories
async def control_categories(callback: types.CallbackQuery, state):
    logger.info("Function to update categories is run")
    await callback.message.delete()
    cat = category_object.view(callback.data)
    markup = create_inline_markup(cat)
    await callback.message.answer("Выбери категорию",reply_markup=markup)
    update_fsm = await state.get_data()
    print(update_fsm)
    a = update_fsm["current_state"].copy()
    a.append(callback.data)
    await state.update_data(current_state=a)
    await callback.answer()




def register_handler_users(dp : Dispatcher):
    """Функция которая оборачивает функционал ответов на сообщения в хэндлеры телеграмма"""

    dp.register_message_handler(command_start, commands=["start"])
    dp.register_message_handler(command_help, lambda message: "Помощь" in message.text)
    dp.register_message_handler(start_shopping,lambda message: "Начать" in message.text)
    dp.register_message_handler(back_to_category, lambda message: "Назад" in message.text, state=UserState.current_state)
    dp.register_message_handler(stop_shopping, lambda message: "Закончить" in message.text, state=UserState.current_state)
    dp.register_callback_query_handler(control_categories, state=UserState.current_state)
