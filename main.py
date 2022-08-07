from aiogram.utils import executor
from create import dp
from handlers import userhandlers
import logging
from bot_logger.BotLogger import logger

userhandlers.register_handler_users(dp)


if __name__ == '__main__':
    logger.info("hi")

    executor.start_polling(dp,skip_updates=True)


