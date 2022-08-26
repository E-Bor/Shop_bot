import urllib
from config import TOKEN, file_path, pre_view_path
from aiogram import Bot, types, Dispatcher
from aiogram.dispatcher import FSMContext
from shop.Datacontroller import database
from bot_logger.BotLogger import logger
from create import dp, bot
from handlers import create_admin_inline_markup, create_admin_markup, create_inline_markup
from shop import category_object
from shop.payments import get_data_for_payment, config_payments
from state import UserState, CategoryState, ItemState, Items
from aiogram.types.message import ContentTypes
from .userhandlers import back_to_category

ID = None

# Functions to check admins
async def start_administrate(message: types.Message):
    global ID
    ID = message.from_user.id
    await bot.send_message(ID, text="Привет, мой администратор!, нажмите на /start")

async def stop_administrate(message: types.Message):
    global ID
    await bot.send_message(ID, text="До встречи, мой администратор")
    ID = None


# command start for admin
async def command_start(message: types.Message):
    await message.delete()
    await bot.send_message(message.from_user.id, """
    Добро пожаловать админ!
    """,reply_markup=create_admin_markup())


# Function that delete partition from the categories
async def command_delete(message: types.Message, state):
    # await message.delete()
    update_fsm = await state.get_data()
    print(update_fsm)
    a = update_fsm["current_state"].copy()
    print(category_object.dict)
    category_object.del_partition(a)
    b = "|".join(a)
    database.delete_position(b)
    await back_to_category(message, state)
    category_object.apply_changes("q")


# add category to dict with categories
async def command_add_category(message: types.Message, state: FSMContext):
    old_state = await state.get_data()
    a = old_state["current_state"].copy()
    await state.finish()
    await CategoryState.name.set()
    new_state = Dispatcher.get_current().current_state()
    await new_state.update_data(path=a)
    await message.answer("Введите название категории")


# catch name of category
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
    if isinstance(cat, list):
        markup = create_inline_markup(cat)
        await message.answer("Выбери категорию", reply_markup=markup)
    category_object.apply_changes("q")


# Start finit state mashine to add file
async def start_adding_file(message: types.Message, state: FSMContext):
    old_state = await state.get_data()
    a = old_state["current_state"].copy()
    await state.finish()
    await ItemState.new_files_data.set()
    new_state = Dispatcher.get_current().current_state()
    await new_state.update_data(directory=a)
    print(old_state := await state.get_state())
    await message.answer("""Введите данные о файле.
    
Имя файла:
Цена:
                         """)

# adding filedata
async def add_file(message: types.Message, state: FSMContext):
    print("add_file")
    a = message.text.split("\n")
    await state.update_data(new_files_data=a)
    await message.answer("скиньте файл")
    await ItemState.file.set()


# catch the file
async def load_file(file: types.Message, state: FSMContext):
    print("load_file")
    file_info = await bot.get_file(file.document.file_id)
    await state.update_data(files=dict(file_info))
    await state.update_data(files_name=file.document.file_name)
    urllib.request.urlretrieve(f'https://api.telegram.org/file/bot{TOKEN}/{file_info.file_path}',
                               f'{file_path}{file.document.file_name}')
    await file.answer("скиньте превью")
    await ItemState.pre_view.set()


# Create position in database
def create_new_file_in_database(dictionary: dict):
    file_name = dictionary["new_files_data"][0]
    cost = dictionary["new_files_data"][1]+"00"
    dictionary["directory"].append(file_name)
    category = "|".join(dictionary["directory"])
    # file = f"{file_path}{dictionary['files_name']}"
    file = f"{dictionary['files_name']}"
    telegram_id_file = dictionary["files"]["file_id"]
    pre_view = f"{dictionary['pre_view_name']}"
    # pre_view = f"{pre_view_path}{dictionary['pre_view_name']}"
    database.add_position(file_name, category, cost, file, telegram_id_file, pre_view)


# catch the file pre view
async  def load_preview(file: types.Message, state: FSMContext):
    pre_view_info = await bot.get_file(file.document.file_id)
    # print("info about files", pre_view_info)
    await state.update_data(pre_view=dict(pre_view_info))
    await state.update_data(pre_view_name=file.document.file_name)
    urllib.request.urlretrieve(f'https://api.telegram.org/file/bot{TOKEN}/{pre_view_info.file_path}',
                               f'{pre_view_path}{file.document.file_name}')
    new_item_data = await state.get_data()
    await state.finish()
    category_object.add_item(new_item_data["new_files_data"][0], new_item_data["directory"])
    await UserState.current_state.set()
    state = Dispatcher.get_current().current_state()
    await state.update_data(current_state=new_item_data["directory"])
    create_new_file_in_database(new_item_data)
    await file.answer("Новый файл успешно добавлен, нажмите кнопку назад")
    category_object.apply_changes("q")


async def add_file_to_file(message: types.Message, state: FSMContext):
    # print("123")
    old_state = await state.get_data()
    a = old_state["current_state"].copy()
    await state.finish()
    await Items.file.set()
    new_state = Dispatcher.get_current().current_state()
    await new_state.update_data(file=a)
    await message.answer("Скиньте файл который нужно прикрепить к данному товару")
    # print(new_state:= await state.get_state())


# add new file for file to sell
async def add_file_to_file_cach (file: types.Message, state: FSMContext):
    pre_view_info = await bot.get_file(file.document.file_id)
    data = await state.get_data()
    # print("hi")
    # print(data["file"])
    urllib.request.urlretrieve(f'https://api.telegram.org/file/bot{TOKEN}/{pre_view_info.file_path}',
                               f'{file_path}{file.document.file_name}')
    path = "|".join(data["file"])
    name = file.document.file_name
    # print(name)
    database.add_position("0", path, "0", str(name), pre_view_info["file_id"], "0")
    await state.finish()
    new_state = data["file"]
    await UserState.current_state.set()
    state = Dispatcher.get_current().current_state()
    await state.update_data(current_state=new_state)
    await file.answer("файл успешно добавлен")


# applied changes
# async def apply(message: types.Message, state: FSMContext):
    # category_object.apply_changes("q")
#     await message.answer("Изменения успешно применены!")


# registers messages
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
    dp.register_message_handler(start_adding_file,
                                lambda message: message.text == "Добавить товар" and message.from_user.id == ID,
                                state=UserState.current_state)
    dp.register_message_handler(add_file, state=ItemState.new_files_data)
    dp.register_message_handler(load_file, state=ItemState.file, content_types=["document"])
    dp.register_message_handler(load_preview, state=ItemState.pre_view, content_types=["document"])
    # dp.register_message_handler(apply,
    #                             lambda message: message.text == "Применить" and message.from_user.id == ID,
    #                             state=UserState.current_state)
    dp.register_message_handler(add_file_to_file ,lambda message: message.text == "/add_files" and message.from_user.id == ID,
                                state=UserState.current_state)
    dp.register_message_handler(add_file_to_file_cach, state=Items.file, content_types=["document"])