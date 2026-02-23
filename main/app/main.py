"""
Docstring for main.app

Purpose: This is the main service for the PowerIPAM Application

"""

import logging
from pathlib import Path
from helpers.constants import DEFAULT_LOG_FORMAT,DEFAULT_LOG_DIR,DEFAULT_DEBUG_LOG_LOCATION
#from helpers.logger import setup_basic_logging

# START ---  Build basic logging to catch any logs that are not from a constructed logger.
if not Path.is_dir(DEFAULT_LOG_DIR):
    Path(DEFAULT_LOG_DIR).mkdir(644,parents=True)

#logging.basicConfig(level=logging.DEBUG,
#                    format=DEFAULT_LOG_FORMAT,
#                    filename=DEFAULT_DEBUG_LOG_LOCATION)
# END ---  Basic Logging

from helpers.logger import configure_logging
configure_logging()
logging.debug('----------===== Start of new Program Execution =====----------')

from helpers.common import whoami
from helpers import constants as c
from  helpers import config as conf
#from helpers.logger import AppLogger

def handler(args) -> None:
    """
    Docstring for handler

    Purpose: Main Function to start the application

    """

    #print(__name__)
    app_logger = logging.getLogger(f'{c.APPLICATION_NAME}').getChild(f'{whoami(logging.currentframe()).split(".")[0]}')
    #logging.debug(f'{app_logger=}')
    #print(f'{app_logger.name=}')
    #print(f'{app_logger.parent=}')
    app_logger.info('Starting PowerIPAM Server Application...')

    from helpers.database import create_db_connection
    session = create_db_connection(conf.DB_URI)
    app_logger.debug(f'{session.info=}')

    if args.test_implementations:
        app_logger.info('Testing Implementations...')
        import sys
        from pathlib import Path
        sys.path.insert(0,str(Path('./tests').absolute()))
        from test_implementations import PowerIPAMtesting
        test_case = PowerIPAMtesting(session)
        test_case.do_testing()
        app_logger.info('Implementation Testing Complete...')

    app_logger.info('Closing DB Connection...')
    session.close()

    return

if __name__ == "__main__":
    root_logger = logging.getLogger('PowerIPAM')
    root_logger.info('Starting PowerIPAM Server from command line...')
    root_logger.debug(f'{__file__=}')

    root_logger.debug('Checking for command line arguments')
    from helpers.command_line import parse_args
    args = parse_args()

    handler(args)

    root_logger.debug('Stopping PowerIPAM Server...')
    
