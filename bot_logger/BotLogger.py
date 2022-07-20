import logging
import os
import platform

"""This is a logger for bot"""

path_to_log = os.path.dirname(__file__)+"\\Bot_logs.log" if platform.system() == "Windows" else os.path.dirname(__file__)+"/Bot_logs.log"
logging.basicConfig(
    level=logging.INFO,
    filename = path_to_log,
    filemode='w',
    format = "[%(asctime)s] %(levelname)s -- FILE: %(filename)s -- |FUNC: %(funcName)s LINE: %(lineno)d| \
- MSG: '%(message)s'",
    datefmt='%H:%M:%S',
    )
logger = logging.getLogger("Bot_logger")