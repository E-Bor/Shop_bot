from aiogram.utils import executor
from create import dp
from handlers import userhandlers
from handlers import admin_hendlers
import logging
from bot_logger.BotLogger import logger

admin_hendlers.register_handler_admins(dp)
userhandlers.register_handler_users(dp)


if __name__ == '__main__':
    logger.info("hi")

    executor.start_polling(dp ,skip_updates=True)


