from aiogram import Bot, types, Dispatcher
from bot_logger.BotLogger import logger
from create import dp, bot
from handlers import create_inline_markup, create_markup
from shop import category_object
from shop.payments import get_data_for_payment, config_payments
from state import UserState
from aiogram.types.message import ContentTypes


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
    logger.info("user was start shop")
    await message.delete()
    await message.answer("Выбери нужную категорию", reply_markup=create_inline_markup(category_object.view()))
    await UserState.current_state.set()
    state = Dispatcher.get_current().current_state()
    await state.update_data(current_state=[])

# function for stop shopping. todo: create a function, That deleting messages
async def stop_shopping(message: types.Message, state):
    logger.info("shopping was stopped")
    await message.delete()
    data = await state.get_data()
    await state.finish()
    await message.answer("Чтобы открыть категории заного, нажмите кнопку начать")

# function to go back in categories
async def back_to_category(message: types.Message, state):
    logger.info("user go back in categories")
    await message.delete()
    update_fsm = await state.get_data()
    print(update_fsm)
    a = update_fsm["current_state"].copy()
    a.pop(-1)
    await state.reset_data()
    await state.update_data(current_state=a)

    cat = category_object.view(a)
    markup = create_inline_markup(cat)
    await message.answer("Выбери категорию", reply_markup=markup)


# function for handling categories
async def control_categories(callback: types.CallbackQuery, state):
    logger.info("Function to update categories is run")
    await callback.message.delete()
    update_fsm = await state.get_data()
    # print(update_fsm)
    a = update_fsm["current_state"].copy()
    a.append(callback.data)
    await state.update_data(current_state=a)
    update_fsm = await state.get_data()
    # print(update_fsm)
    cat = category_object.view(update_fsm["current_state"])

    # print(cat)
    # Not end categories
    if isinstance(cat, list):
        print(cat)
        markup = create_inline_markup(cat)
        await callback.message.answer("Выбери категорию",reply_markup=markup)
    # end categories
    if isinstance(cat, dict):
        # await BuyState.item_for_buying.set()
        # markup = create_inline_markup(cat.keys())
        # await callback.message.answer("Выбери товар",reply_markup=markup)

        logger.info("User in last lvl in categories")
        await bye_item(callback, state)
        # await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)


    await callback.answer()


# function for replying markup and payments
async def bye_item(callback: types.CallbackQuery, state):
    await callback.answer("bye")
    # end_fsm = await state.get_data()
    # a = end_fsm["current_state"].copy()
    # a.append(callback.data)
    # await state.update_data(current_state=a)
    # print(callback)
    category = await state.get_data()
    logger.info("called function to pay")
    # print(category["current_state"])
    dataoffile = get_data_for_payment(category["current_state"])        # getting data about callable file
    with open(dataoffile["preview_path"], "rb") as f:                  # open callable file and send preview
        await callback.message.answer_document(f)

    prices = [
        types.LabeledPrice(label=dataoffile["name"],\
                           amount=dataoffile["cost"]),
    ]
    await bot.send_invoice(callback.message.chat.id, title=config_payments.TITLE,           # send payments
                           description=config_payments.DESCRIPTION,
                           provider_token=config_payments.PAYMENTS_PROVIDER_TOKEN,
                           currency='rub',
                           photo_url='',
                           photo_height=512,  # !=0/None or picture won't be shown
                           photo_width=512,
                           photo_size=512,
                           is_flexible=False,   # True If you need to set up Shipping Fee
                           prices=prices,
                           start_parameter='time-machine-example',
                           payload='HAPPY FRIDAYS COUPON')

    await callback.answer()


# handler for update pay status
async def checkout(pre_checkout_query: types.PreCheckoutQuery):
    print("pre_checkout_query")
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True,
                                        error_message=config_payments.ERROR_MESSAGE)


# handler for success pay status and reply file
async def got_payment(message: types.Message, state):
    print("got_payment")
    await bot.send_message(message.chat.id,
                           config_payments.PAYED_SUCCESS,
                           parse_mode='Markdown')
    category = await state.get_data()
    dataoffile = get_data_for_payment(category["current_state"])
    with open(dataoffile["file_path"], "rb") as f:                  # open callable file and send file
        await message.answer_document(f)

    await state.finish()



def register_handler_users(dp : Dispatcher):
    """Функция которая оборачивает функционал ответов на сообщения в хэндлеры телеграмма"""

    dp.register_message_handler(command_start, commands=["start"])
    dp.register_message_handler(command_help, lambda message: "Помощь" in message.text)
    dp.register_message_handler(start_shopping,lambda message: "Начать" in message.text)
    dp.register_message_handler(back_to_category, lambda message: "Назад" in message.text,
                                state=UserState.current_state,)
    dp.register_message_handler(stop_shopping, lambda message: "Закончить" in message.text,
                                state=UserState.current_state)
    # dp.register_callback_query_handler(bye_item,lambda message: message.data == "Pay" ,
    #                                    state=UserState.current_state)
    # написать хэндлер который ловит категории
    dp.register_pre_checkout_query_handler(checkout,lambda query: True,state=UserState.current_state)
    dp.register_message_handler(got_payment, content_types=ContentTypes.SUCCESSFUL_PAYMENT, state=UserState.current_state)
    dp.register_callback_query_handler(control_categories, state=UserState.current_state)

