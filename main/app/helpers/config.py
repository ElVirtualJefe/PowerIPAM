

import logging
from helpers.constants import APPLICATION_NAME
from helpers.common import whoami
from inspect import currentframe

mod_logger = logging.getLogger(f'{APPLICATION_NAME}.{whoami(currentframe()).split(".")[0]}')
mod_logger.propagate = True
mod_logger.debug('Entering module %s', whoami(currentframe()))
print(f'{mod_logger.parent=}')

def check_for_config_file(config_file="config.ini") -> str:
    """
    Docstring for __check_for_config_file
    
    :param confFile: Location for configuration file.
    """

    mod_logger.debug('Entering function %s', whoami(currentframe()))

    try:
        from pathlib import Path
        if Path.is_file(config_file):
            mod_logger.debug('Found config file - %s', config_file)
            return config_file

        else:
            mod_logger.debug('Could not find %s file...', config_file)
            mod_logger.debug('Using DEFAULT configuration settings...')
            return 'DEFAULTS'

    finally:
        mod_logger.debug('Leaving function %s', whoami(currentframe()))


def process_config(config_file):
    """
    Docstring for process_config
    
    :param config_file: str -> File location of config file
    """
    mod_logger.debug('Entering function %s', whoami(currentframe()))

    try:
        from configparser import ConfigParser

        config = ConfigParser()
        config.read(config_file)

        return config
    finally:
        mod_logger.debug('Leaving function %s', whoami(currentframe()))

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
mod_logger.debug(f'{DB_URI=}')
