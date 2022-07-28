from aiogram import Bot, types, Dispatcher
from create import dp,bot
from handlers import create_inline_markup
from shop import category_object
"""file for userhandlers"""

Handlers_list = {
    1 : "start",
    2 : "help"
}





#команда start
async def command_start(message: types.Message):
    await bot.send_message(message.from_user.id, """
    Добро пожаловать в магазин!
    """,reply_markup=create_inline_markup(["Меню"]))

#команда help
async def command_help(message: types.Message):
    await bot.send_message(message.from_user.id, f"""
    Вот список доступных комманд 
    {str(Handlers_list)}    
    """)
# command to start choose the item
async def start_shopping(message: types.Message):
    await bot.message.answer("Выбери нужную категорию", reply_markup=create_inline_markup(category_object.view()))



async def buttons(message: types.CallbackQuery):

    await bot.send_message(message.from_user.id,f"Нажата {message.data}")
    await message.answer()



def register_handler_users(dp : Dispatcher):
    """Функция которая оборачивает функционал ответов на сообщения в хэндлеры телеграмма"""

    dp.register_message_handler(command_start, commands=[Handlers_list[1]])
    dp.register_message_handler(command_help, commands=[Handlers_list[2]])
    dp.register_message_handler(start_shopping, commands=["start_shopping"])
    # dp.register_callback_query_handler(buttons, text_contains=)