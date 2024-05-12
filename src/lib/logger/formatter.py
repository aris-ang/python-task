"""
Module that defines a custom log formatter
"""
import logging


class CustomFormatter(logging.Formatter):
    """
    Custom formatter class used for formatting all logger logs.
    """
    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    form = "%(asctime)s %(levelname)-8s [%(filename)s:%(funcName)s:" \
           "%(lineno)d] [%(message)s]"

    FORMATS = {
        logging.DEBUG: grey + form + reset,
        logging.INFO: grey + form + reset,
        logging.WARNING: yellow + form + reset,
        logging.ERROR: red + form + reset,
        logging.CRITICAL: bold_red + form + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)
