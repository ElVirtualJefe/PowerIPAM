from argparse import ArgumentParser
from  apps.scan_agent.src.helpers.constants import APPLICATION_NAME,APPLICATION_VERSION
import logging



def parse_args() -> dict:
    """
    Docstring for parse_args
    
    :return: Returns a dictionary with the command line options and their values (if any)
    :rtype: dict()
    """
    arg = ArgumentParser(prog=APPLICATION_NAME,
                         description='PowerIPAM is a software for tracking and managing IP Address usage in a Private Network',
                         epilog='© Copyright 2026 - ElVirtualJefe')
    
    arg.add_argument('--version', action='version', version='%(prog)s '+APPLICATION_VERSION)

    arg.add_argument('-v','--verbose',
                     action='count',
                     default=3)

    arg.add_argument('--config_file',
                     help='Location of the configuration file to use when running the program (default: %(default)s)')
    
    arg.add_argument('--db_hostname',
                     help='IP Address or FQDN of the host where the DB is running (default: %(default)s)',
                     default='localhost')
    
    arg.add_argument('--test-implementations',
                     dest='test_implementations',
                     help='Used to test current implementations in the code...',
                     action='store_true')
    
    parsed_args = arg.parse_args()

    logging.debug(f'{parsed_args=}')

    return parsed_args
