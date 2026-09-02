#from pathlib import Path
#print(f"Path = {Path(__file__).resolve().parent.parent}")

from . import log_manager, APPLICATION_NAME
from logging import getLogger, currentframe

log_manager.configure_logging()
#print(f"__init__ {log_manager.application_name=}")
#print(f"__init__ {log_manager.log_level=}")
#print(f"__init__ {log_manager.log_file_level=}")

app_logger = getLogger(log_manager.application_name)
app_logger.debug("---+++  Initialized Logger for %s  +++---",APPLICATION_NAME)
#app_logger.info('test log...')

app_logger.debug('Starting Scan Agent Process...')

from .helpers import common
from .helpers import constants as c
from .helpers import config as conf
#from helpers.logger import AppLogger

def handler(args=None) -> None:
    """
    Docstring for handler

    Purpose: Main Function to start the application

    """

    func_logger = getLogger(f'{c.APPLICATION_NAME}').getChild(f'{common.whoami(currentframe()).split(".")[0]}')
    func_logger.info('Starting PowerIPAM Scan Agent Application...')

    import nmap
    scanner = nmap.PortScanner()
    results = scanner.scan(hosts='10.160.0.0/24',arguments=c.NMAP_ARGUMENTS["pingScan"])
    print(f'{results=}')

    return


if __name__ == "__main__":
    root_logger = getLogger(f'{c.APPLICATION_NAME}')
    root_logger.info('Starting PowerIPAM Server from command line...')
    root_logger.debug(f'{__file__=}')

    #root_logger.debug('Checking for command line arguments')
    #from helpers.command_line import parse_args
    #args = parse_args()

    #handler(args)
    handler()

    root_logger.debug('Stopping PowerIPAM Server...')

