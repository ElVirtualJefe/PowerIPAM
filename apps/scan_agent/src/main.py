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

if __package__:
    from .config import get_settings
else:
    from config import get_settings

settings = get_settings()

configure_logging(
    service_name=f'[{settings.service_name} {settings.service_ver}]',
    environment=settings.environment,
    log_format="syslog",
    level=settings.log_level,
    version=settings.app_ver
)

app_logger = get_logger(settings.service_name)
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
    func_logger = get_logger(settings.service_name).getChild(f'{whoami(currentframe())}')
    func_logger.info('Starting PowerIPAM Scan Agent Application...')

    if __package__:
        from .implementations.nmap import AsyncSubnetScanner
    else:
        from implementations.nmap import AsyncSubnetScanner

    import nmap

    scanner = nmap.PortScanner()
    aScan = AsyncSubnetScanner('10.160.0.0/24')
    results = scanner.scan(hosts='10.160.0.0/24', arguments=settings.NMAP_ARGUMENTS["pingScan"])
    #print(f'{results=}')
    print(f'{results.get("scan",None)=}')

    for host in results.get("scan", {}):
        print(f"Host: {host}")
        print(results["scan"].get(host,{}))

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

