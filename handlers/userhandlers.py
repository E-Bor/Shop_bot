from aiogram import Bot, types, Dispatcher
from create import dp,bot
# from handlers import markups as mk
"""file for userhandlers"""

Handlers_list = {
    1 : "start",
    2 : "help"
}

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

mainMenu = InlineKeyboardMarkup(row_width=2)
btn1 = InlineKeyboardButton(text ="button1", callback_data="btn1")
btn2 = InlineKeyboardButton(text ="button2", callback_data="btn2")
btn3 = InlineKeyboardButton(text ="button3", callback_data="btn3")
btn4 = InlineKeyboardButton(text ="button4", callback_data="btn4")
btn5 = InlineKeyboardButton(text ="button5", callback_data="btn5")
btns = [btn1,btn2,btn3,btn4,btn5]

mainMenu.add(*btns)



#команда start
async def command_start(message: types.Message):
    await bot.send_message(message.from_user.id, """
    Добро пожаловать в магазин!
    """,reply_markup=mainMenu)

#команда help
async def command_help(message: types.Message):
    await bot.send_message(message.from_user.id, f"""
    Вот список доступных комманд 
    {str(Handlers_list)}    
    """)

async def button1(message: types.CallbackQuery):

    await bot.send_message(message.from_user.id,f"Нажата {message.data}")
    await message.answer()



def register_handler_users(dp : Dispatcher):
    """Функция которая оборачивает функционал ответов на сообщения в хэндлеры телеграмма"""

    dp.register_message_handler(command_start, commands=[Handlers_list[1]])
    dp.register_message_handler(command_help, commands=[Handlers_list[2]])
    dp.register_callback_query_handler(button1, text_contains="btn")