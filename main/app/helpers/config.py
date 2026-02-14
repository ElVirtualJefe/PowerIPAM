

import logging
from helpers.constants import APPLICATION_NAME
from helpers.common import whoami
#from helpers.logger import AppLogger
from inspect import currentframe

#mod_logger = AppLogger(f'{APPLICATION_NAME}.{whoami(currentframe()).split(".")[0]}')
#mod_logger.propagate = True
logging.debug('Entering module %s', whoami(currentframe()))
#print(f'{mod_logger.parent=}')

def check_for_config_file(config_file="config.ini") -> str:
    """
    Docstring for __check_for_config_file
    
    :param confFile: Location for configuration file.
    """

    logging.debug('Entering function %s', whoami(currentframe()))

    try:
        from pathlib import Path
        if Path.is_file(config_file):
            logging.debug('Found config file - %s', config_file)
            return config_file

        else:
            logging.debug('Could not find %s file...', config_file)
            logging.debug('Using DEFAULT configuration settings...')
            return 'DEFAULTS'

    finally:
        logging.debug('Leaving function %s', whoami(currentframe()))


def process_config(config_file):
    """
    Docstring for process_config
    
    :param config_file: str -> File location of config file
    """
    logging.debug('Entering function %s', whoami(currentframe()))

    try:
        from configparser import ConfigParser

        config = ConfigParser()
        config.read(config_file)

        return config
    finally:
        logging.debug('Leaving function %s', whoami(currentframe()))

conf_file = check_for_config_file()
conf = process_config(conf_file)


"""
Constants Section for Config Values
"""


# Database Constants
DB_HOSTNAME = conf.get('database','db_server',fallback='database')
DB_PORT = conf.get('database','db_port',fallback='5432')
DB_NAME = conf.get('database','db_name',fallback='poweripam')
DB_USER = conf.get('database','db_username',fallback='postgres')
DB_PASSWORD = conf.get('database','db_password',fallback='postgres')

DB_URI = f'postgres+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOSTNAME}:{DB_PORT}/{DB_NAME}'
# Scheme: "postgres+psycopg2://<USERNAME>:<PASSWORD>@<IP_ADDRESS>:<PORT>/<DATABASE_NAME>"
logging.debug(f'{DB_URI=}')


# Logging Constants
LOG_LEVEL = logging.getLevelNamesMapping()[conf.get('logging','log_level',fallback='info').upper()]
LOG_FILE_LEVEL = logging.getLevelNamesMapping()[conf.get('logging','log_file_level',fallback='warning').upper()]
logging.debug(f'{LOG_FILE_LEVEL=}')
LOG_FILE = conf.get('logging','log_file',fallback='PowerIPAM.log')
LOG_DIR = conf.get('logging','log_dir',fallback='./logs')

LOG_LOCATION = f'{LOG_DIR}/{LOG_FILE}'
