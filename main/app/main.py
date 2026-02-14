"""
Docstring for main.app

Purpose: This is the main service for the PowerIPAM Application

"""

import logging
from pathlib import Path
from helpers.constants import DEFAULT_LOG_FORMAT,DEFAULT_LOG_DIR
#from helpers.logger import setup_basic_logging

def setup_basic_logging(log_level=logging.DEBUG,log_fmt=DEFAULT_LOG_FORMAT,log_dir=DEFAULT_LOG_DIR) -> None:
    """
    Docstring for setup_basic_logging
    
    :param level: Description
    :param format: Description
    """

    if not Path.is_dir(log_dir):
        Path(dir).mkdir(644,parents=True)
    
    logging.basicConfig(level=log_level,
                        format=log_fmt,
                        filename=f'{log_dir}/PowerIPAM-debug.log')

setup_basic_logging()
logging.debug('----------===== Start of new Program Execution =====----------')

from inspect import currentframe
from helpers.common import whoami
import helpers.constants as c
import helpers.config as conf
from helpers.logger import AppLogger

def handler() -> None:
    """
    Docstring for handler

    Purpose: Main Function to start the application

    """

    app_logger = AppLogger(f'{c.APPLICATION_NAME}.{whoami(currentframe()).split(".")[0]}',propagate=False)
    logging.debug(f'{app_logger=}')
    app_logger.info('Starting PowerIPAM Server Application...')

    from helpers.database import create_db_connection

    return

if __name__ == "__main__":
    root_logger = logging.getLogger('root')
    root_logger.info('Starting PowerIPAM Server from command line...')
    root_logger.debug(f'{__file__=}')

    root_logger.debug('Checking for command line arguments')
    from helpers.command_line import parse_args
    parse_args()

    handler()
    root_logger.debug('Stopping PowerIPAM Server...')
    
