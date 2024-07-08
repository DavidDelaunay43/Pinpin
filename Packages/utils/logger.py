import datetime
import logging
import os
import sys
from Packages.utils.constants.preferences import LOGS_PATH
date = str(datetime.date.today()).replace("-", "_")


class Logger:


    def __init__(self, 
                 logger_name = "Logger name", 
                 format_default = "[%(asctime)s][%(name)s][%(levelname)s] %(message)s",
                 file_format_default = "[%(asctime)s][%(name)s][%(levelname)s] %(message)s",
                 level_default = logging.DEBUG,
                 level_write_default = logging.WARNING,
                 propagate_default = False
    ):
        
        self.LOGGER_NAME = logger_name if '\\' not in logger_name else os.path.basename(logger_name)
        self.FORMAT_DEFAULT = format_default
        self.FILE_FORMAT_DEFAULT = file_format_default
        self.LEVEL_DEFAULT = level_default
        self.LEVEL_WRITE_DEFAULT = level_write_default
        self.PROPAGATE_DEFAULT = propagate_default

        self._logger = None
        self.init_logger()


    def init_logger(self):
        if self.logger_exists():
            self._logger = logging.getLogger(self.LOGGER_NAME)
        else:
            self._logger = logging.getLogger(self.LOGGER_NAME)
            self._logger.setLevel(self.LEVEL_DEFAULT)
            self._logger.propagate = self.PROPAGATE_DEFAULT

            formatter = logging.Formatter(self.FORMAT_DEFAULT)
            handler = logging.StreamHandler(sys.stderr)
            handler.setFormatter(formatter)
            self._logger.addHandler(handler)


    def logger_exists(self):
        return self.LOGGER_NAME in logging.Logger.manager.loggerDict.keys()


    def set_level(self, level):
        self._logger.setLevel(level)


    def set_propagate(self, propagate):
        self._logger.propagate = propagate


    def debug(self, msg, *args, **kwargs):
        self._logger.debug(msg, *args, **kwargs)


    def info(self, msg, *args, **kwargs):
        self._logger.info(f'{msg}', *args, **kwargs)


    def warning(self, msg, *args, **kwargs):
        self._logger.warning(f'{msg}', *args, **kwargs)


    def error(self, msg, *args, **kwargs):
        self._logger.error(f'{msg}', *args, **kwargs)


    def critical(self, msg, *args, **kwargs):
        self._logger.critical(msg, *args, **kwargs)


    def log(self, level, msg, *args, **kwargs):
        self._logger.log(level, msg, *args, **kwargs)


    def exception(self, msg, *args, **kwargs):
        self._logger.exception(msg, *args, **kwargs)


    def write_to_file(self, path, level=None):
        if level is None:
            level = self.LEVEL_WRITE_DEFAULT
        file_handler = logging.FileHandler(path)
        file_handler.setLevel(level)

        formatter = logging.Formatter(self.FILE_FORMAT_DEFAULT)
        file_handler.setFormatter(formatter)

        self._logger.addHandler(file_handler)


def init_logger(file_name: str):
    '''
    '''

    logger = Logger(file_name)
    log_file_path = f'{os.path.join(LOGS_PATH, date)}.log'
    if os.path.exists(log_file_path):
        logger.write_to_file(log_file_path)

    return logger
