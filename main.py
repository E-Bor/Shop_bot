from aiogram.utils import executor
from create import dp
from handlers import userhandlers


userhandlers.register_handler_users(dp)


if __name__ == '__main__':

    executor.start_polling(dp,skip_updates=False)


