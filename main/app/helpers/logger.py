"""
Docstring for main.app.helpers.logger
"""

from sys import stdout
import logging
from helpers.config import LOG_LEVEL,LOG_FILE_LEVEL,LOG_LOCATION
from helpers.constants import DEFAULT_LOG_FORMATTER,DEFAULT_DEBUG_LOG_LOCATION

class AppLogger():    
    logger = None
    name = None

    def __init__(self,name,propagate=True):
        self.name = name
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        self.logger.propagate = propagate

        console_log_handler = logging.StreamHandler(stdout)
        console_log_handler.setLevel(LOG_LEVEL)
        console_log_handler.setFormatter(DEFAULT_LOG_FORMATTER)
        self.logger.addHandler(console_log_handler)

        file_log_handler = logging.FileHandler(LOG_LOCATION)
        file_log_handler.setLevel(LOG_FILE_LEVEL)
        file_log_handler.setFormatter(DEFAULT_LOG_FORMATTER)
        self.logger.addHandler(file_log_handler)

        debug_file_log_handler = logging.FileHandler(DEFAULT_DEBUG_LOG_LOCATION)
        debug_file_log_handler.setLevel(logging.DEBUG)
        debug_file_log_handler.setFormatter(DEFAULT_LOG_FORMATTER)
        self.logger.addHandler(debug_file_log_handler)

    def __repr__(self) -> str:
        
        return f"""<--
AppLogger - {self.name}
Handlers - {self.logger.handlers}
-->"""
      
    def log(self,msg,level='info'):
        """
        Docstring for log
        
        :param self: Description
        :param msg: Description
        :param level: Description
        """
        match level:
            case 'debug':
                self.logger.debug(msg)
            case 'critical':
                self.logger.critical(msg)
            case 'error':
                self.logger.error(msg)
            case 'warning':
                self.logger.warning(msg)
            case 'info':
                self.logger.info(msg)
            case _:
                self.logger.info(msg)
    
    def debug(self,msg):
        """
        Docstring for debug
        
        :param self: Description
        :param msg: Description
        """
        self.log(msg,'debug')

    def critical(self,msg):
        """
        Docstring for critical
        
        :param self: Description
        :param msg: Description
        """
        self.log(msg,'critical')

    def error(self,msg):
        """
        Docstring for error
        
        :param self: Description
        :param msg: Description
        """
        self.log(msg,'error')

    def warning(self,msg):
        """
        Docstring for warning
        
        :param self: Description
        :param msg: Description
        """
        self.log(msg,'warning')

    def info(self,msg):
        """
        Docstring for info
        
        :param self: Description
        :param msg: Description
        """
        self.log(msg,'info')

