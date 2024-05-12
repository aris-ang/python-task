"""
Logger used for logging to the console
"""
import logging
import os
import queue
from logging.handlers import QueueHandler, QueueListener

from src.lib.logger.formatter import CustomFormatter

LOG_FORMAT = "%(asctime)s %(levelname)-8s " \
         "[%(filename)s:%(funcName)s:%(lineno)d] [%(message)s]"
LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG")
formatter = logging.Formatter(LOG_FORMAT)
handler = logging.StreamHandler()
handler.setLevel(LOG_LEVEL)
handler.setFormatter(CustomFormatter())

que = queue.Queue(-1)  # no limit on size
queue_handler = QueueHandler(que)

listener = QueueListener(que, handler)

logger = logging.getLogger()
logger.setLevel(LOG_LEVEL)
logger.addHandler(queue_handler)
