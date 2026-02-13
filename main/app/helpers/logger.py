"""
Docstring for main.app.helpers.logger
"""

import logging
from pathlib import Path
from helpers.constants import DEFAULT_LOG_FORMATTER,DEFAULT_LOG_FORMAT,DEFAULT_LOG_DIR
from helpers.config import LOG_LEVEL,LOG_FILE_LEVEL,LOG_LOCATION
from sys import stdout

class AppLogger():

    logger = None
    name = None

    def __init__(self,name,propagate=True):
        self.name = name
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        self.logger.propagate = propagate

        conLogHandler = logging.StreamHandler(stdout)
        conLogHandler.setLevel(LOG_LEVEL)
        conLogHandler.setFormatter(DEFAULT_LOG_FORMATTER)
        self.logger.addHandler(conLogHandler)

        file_log_handler = logging.FileHandler(LOG_LOCATION)
        file_log_handler.setLevel(LOG_FILE_LEVEL)
        file_log_handler.setFormatter(DEFAULT_LOG_FORMATTER)
        self.logger.addHandler(file_log_handler)

    def __repr__(self) -> str:
        
        return f"""<--
AppLogger - {self.name}
-->"""
      
    def log(self,msg,level='info'):
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
        self.log(msg,'debug')

    def critical(self,msg):
        self.log(msg,'critical')

    def error(self,msg):
        self.log(msg,'error')

    def warning(self,msg):
        self.log(msg,'warning')

    def info(self,msg):
        self.log(msg,'info')

def setup_basic_logging(level=logging.DEBUG,fmt=DEFAULT_LOG_FORMAT,dir=DEFAULT_LOG_DIR) -> None:
    """
    Docstring for setup_basic_logging
    
    :param level: Description
    :param format: Description
    """

    if not Path.is_dir(dir):
        Path(dir).mkdir(644,parents=True)

    logging.basicConfig(level=level,
                        format=fmt,
                        filename=f'{dir}/PowerIPAM-debug.log')

