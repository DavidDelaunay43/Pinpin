import logging
import sys

try:
    from colorama import init, Fore, Style 

    class ColoramaFormatter(logging.Formatter):
        
        COLOR_CODES = {
            logging.DEBUG: Fore.CYAN,
            logging.INFO: Fore.GREEN,
            logging.WARNING: Fore.YELLOW,
            logging.ERROR: Fore.RED,
            logging.CRITICAL: Fore.MAGENTA,
        }

        def format(self, record: logging.LogRecord):
            init(autoreset=True)
            color = self.COLOR_CODES.get(record.levelno, "")
            record.levelname = f"{color}[{record.levelname}]{Style.RESET_ALL}"
            return super(ColoramaFormatter, self).format(record)
        
except ModuleNotFoundError as error:
    class ColoramaFormatter(logging.Formatter):
        ...    


class Logger:
    
    
    LOGGER_NAME = 'Pinpin Logger'
    FORMAT_DEFAULT = "%(levelname)s\n%(message)s\n"
    FILE_FORMAT_DEFAULT = "[%(asctime)s][%(levelname)s]\n%(message)s\n"
    SECONDS_FMT_DEF = r"%Y-%m-%d %H:%M:%S"
    LEVEL_DEFAULT = logging.DEBUG
    LEVEL_WRITE_DEFAULT = logging.INFO
    PROPAGATE_DEFAULT = False
    
    _logger = None
    
    
    @classmethod
    def logger(cls):
        
        if not cls._logger:
            
            if cls.logger_exists():
                cls._logger = logging.getLogger(cls.LOGGER_NAME)
                
            else:
                cls._logger = logging.getLogger(cls.LOGGER_NAME)
                cls._logger.setLevel(cls.LEVEL_DEFAULT)
                cls._logger.propagate = cls.PROPAGATE_DEFAULT
            
                #formatter = logging.Formatter(cls.FORMAT_DEFAULT, cls.SECONDS_FMT_DEF)
                formatter: ColoramaFormatter = ColoramaFormatter(cls.FORMAT_DEFAULT, cls.SECONDS_FMT_DEF)

                handler = logging.StreamHandler(sys.stderr)
                handler.setFormatter(formatter)
                
                cls._logger.addHandler(handler)
        
        return cls._logger
    
    
    @classmethod
    def logger_exists(cls):
        return cls.LOGGER_NAME in logging.Logger.manager.loggerDict.keys()
    
    
    @classmethod
    def set_level(cls, level):
        cls.logger().setLevel(level)
    
        
    @classmethod
    def set_propagate(cls, propagate):
        cls.logger().propagate = propagate
    
       
    @classmethod
    def debug(cls, msg, *args, **kwargs):
        cls.logger().debug(msg, *args, **kwargs)
    
        
    @classmethod
    def info(cls, msg, *args, **kwargs):
        cls.logger().info(msg, *args, **kwargs)
    
        
    @classmethod
    def warning(cls, msg, *args, **kwargs):
        cls.logger().warning(msg, *args, **kwargs)
    
        
    @classmethod
    def error(cls, msg, *args, **kwargs):
        cls.logger().error(msg, *args, **kwargs)
    
        
    @classmethod
    def critical(cls, msg, *args, **kwargs):
        cls.logger().critical(msg, *args, **kwargs)
    
        
    @classmethod
    def log(cls, level, msg, *args, **kwargs):
        cls.logger().log(level, msg, *args, **kwargs)
    
        
    @classmethod
    def exception(cls, msg, *args, **kwargs):
        cls.logger().exception(msg, *args, **kwargs)
    
        
    @classmethod
    def write_to_file(cls, path, level = LEVEL_WRITE_DEFAULT):
        file_handler = logging.FileHandler(path)
        file_handler.setLevel(level)
        
        formatter = logging.Formatter(cls.FILE_FORMAT_DEFAULT, cls.SECONDS_FMT_DEF)
        file_handler.setFormatter(formatter)
        
        logger = cls.logger()
        logger.addHandler(file_handler)



def main() -> None:
    log_path: str = 'test.log'
    Logger.LOGGER_NAME = f'{__file__}'
    Logger.write_to_file(path=log_path, level=logging.DEBUG)
    Logger.info('info')
    Logger.critical("critical")
    Logger.warning('warning')
    Logger.debug("debug")
    

if __name__ == '__main__':
    main()
