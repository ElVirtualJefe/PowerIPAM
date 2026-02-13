"""
Docstring for main.app

Purpose: This is the main service for the PowerIPAM Application

"""

import logging
from helpers.logger import setup_basic_logging

#print('--- 001 ---')
setup_basic_logging()
logging.debug('----------===== Start of new Program Execution =====----------')

from inspect import currentframe
from helpers.common import whoami
import helpers.constants as c
import helpers.config as conf

def handler() -> None:
    """
    Docstring for handler

    Purpose: Main Function to start the application

    """

    # print(whoami(currentframe()))
    app_logger = logging.getLogger(f'{c.APPLICATION_NAME}.{whoami(currentframe()).split(".")[0]}')
    app_logger.setLevel(logging.DEBUG)
    app_logger.propagate = False

    from sys import stdout
    conLogHandler = logging.StreamHandler(stdout)
    conLogHandler.setLevel(logging.DEBUG)
    conLogHandler.setFormatter(c.DEFAULT_LOG_FORMATTER)

    app_logger.addHandler(conLogHandler)

    app_logger.debug('Starting PowerIPAM Server Application...')
    #print(f'{app_logger.handlers=}')
    #print(f'{app_logger.parent=}')
    #print(f'{app_logger.root.handlers=}')

    from helpers.database import create_db_connection

    return

if __name__ == "__main__":
    #print('--- 002 ---')
    root_logger = logging.getLogger('root')
    root_logger.info('Starting PowerIPAM Server from command line...')
    root_logger.debug(f'{__file__=}')

    root_logger.debug('Checking for command line arguments')
    from helpers.command_line import parse_args
    parse_args()

#    logging.debug('Checking for configuration file...')
#    import helpers.config as config
#    config.check_for_config_file()

    handler()
    root_logger.debug('Stopping PowerIPAM Server...')
    
