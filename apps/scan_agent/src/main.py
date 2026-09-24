"""
#from pathlib import Path
#print(f"Path = {Path(__file__).resolve().parent.parent}")

from . import log_manager, APPLICATION_NAME
from logging import getLogger, currentframe

log_manager.configure_logging()
#print(f"__init__ {log_manager.application_name=}")
#print(f"__init__ {log_manager.log_level=}")
#print(f"__init__ {log_manager.log_file_level=}")
"""

from logging import currentframe
#from logging_lib import set_context, get_logger
from logging_lib import configure_logging, set_context, remove_context, get_logger, whoami
from helpers import constants as c

configure_logging(
    service_name=f'[{c.APPLICATION_NAME} {c.APPLICATION_VERSION}]',
    environment="development",
    log_format="syslog",
    level="DEBUG",
    version=c.APPLICATION_VERSION
)

app_logger = get_logger(c.LOGGER_NAME)
app_logger.debug("---+++  Initialized Logger for %s  +++---", (__name__))
#app_logger.info('test log...')

app_logger.debug('Starting Scan Agent Process...')

#from .helpers import common
#from .helpers import config as conf
#from helpers.logger import AppLogger

def handler(args=None) -> None:
    """
    Docstring for handler

    Purpose: Main Function to start the application

    """

    #set_context(function=whoami(currentframe()))
    func_logger = get_logger(c.LOGGER_NAME).getChild(f'{whoami(currentframe())}')
    func_logger.info('Starting PowerIPAM Scan Agent Application...')

    import nmap
    from implementations.nmap import AsyncSubnetScanner

    scanner = nmap.PortScanner()
    aScan = AsyncSubnetScanner('10.160.0.0/24')
    results = scanner.scan(hosts='10.160.0.0/24',arguments=c.NMAP_ARGUMENTS["pingScan"])
    print(f'{results=}')

    #remove_context(function=None)
    return


if __name__ == "__main__":
    #set_context(file=__file__.rsplit(c.DELIM, maxsplit=1)[-1], module=__name__)
    #root_logger = get_logger(__name__)
    app_logger.info('Starting PowerIPAM Server from command line...')
    app_logger.debug('%s',__file__)

    #root_logger.debug('Checking for command line arguments')
    #from helpers.command_line import parse_args
    #args = parse_args()

    #handler(args)
    handler()

    app_logger.debug('Stopping PowerIPAM Server...')

