from helpers.logger import configure_logging
configure_logging()
import logging
logging.debug('----------===== Start of new Program Execution =====----------')

from helpers.common import whoami
from helpers import constants as c
from  helpers import config as conf
#from helpers.logger import AppLogger

def handler(args=None) -> None:
    """
    Docstring for handler

    Purpose: Main Function to start the application

    """

    #print(__name__)
    app_logger = logging.getLogger(f'{c.APPLICATION_NAME}').getChild(f'{whoami(logging.currentframe()).split(".")[0]}')
    #logging.debug(f'{app_logger=}')
    #print(f'{app_logger.name=}')
    #print(f'{app_logger.parent=}')
    app_logger.info('Starting PowerIPAM Scan Agent Application...')

if __name__ == "__main__":
    root_logger = logging.getLogger(f'{c.APPLICATION_NAME}')
    root_logger.info('Starting PowerIPAM Server from command line...')
    root_logger.debug(f'{__file__=}')

    #root_logger.debug('Checking for command line arguments')
    #from helpers.command_line import parse_args
    #args = parse_args()

    #handler(args)
    handler()

    root_logger.debug('Stopping PowerIPAM Server...')

