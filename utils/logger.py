import logging
import os
from logging.handlers import TimedRotatingFileHandler

logger = None

os.makedirs("logs", exist_ok=True)


def setup_logger(test=False) -> logging.Logger:
    global logger

    class TerminalFormatter(logging.Formatter):
        grey = "\x1b[38;20m"
        yellow = "\x1b[33;20m"
        red = "\x1b[31;20m"
        bold_red = "\x1b[31;1m"
        reset = "\x1b[0m"

        custom_format = (
            "%(asctime)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"
        )

        FORMATS = {
            logging.DEBUG: grey + custom_format + reset,
            logging.INFO: grey + custom_format + reset,
            logging.WARNING: yellow + custom_format + reset,
            logging.ERROR: red + custom_format + reset,
            logging.CRITICAL: bold_red + custom_format + reset,
        }

        def format(self, record):
            log_fmt = self.FORMATS.get(record.levelno)
            formatter = logging.Formatter(log_fmt)
            return formatter.format(record)

    class FileFormatter(logging.Formatter):
        custom_format = (
            "%(asctime)s - %(levelname)-8s - %(message)s (%(filename)s:%(lineno)d)"
        )

        def format(self, record):
            formatter = logging.Formatter(
                self.custom_format, datefmt="%d-%m-%Y %H:%M:%S"
            )
            return formatter.format(record)

    logger = logging.Logger("yuibotlogger")
    logger.setLevel(logging.DEBUG)

    # stream handler for handling terminal logging only if we are in test mode
    if test is True:
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(TerminalFormatter())
        logger.addHandler(stream_handler)

    # file handler for logging to file
    if test is not True:
        file_handler = TimedRotatingFileHandler(
            "logs/yuibot.log", when="midnight", interval=1, backupCount=7
        )
        file_handler.setFormatter(FileFormatter())
        logger.addHandler(file_handler)

    return logger
