import logging

if __name__ == 'app.helpers.config':
    from app.helpers.constants import APPLICATION_NAME,DEFAULT_DEBUG_LOG_FILE
    from app.helpers.common import whoami
else:
    from helpers.constants import APPLICATION_NAME,DEFAULT_DEBUG_LOG_FILE
    from helpers.common import whoami

current_frame_name = whoami(logging.currentframe())
#from helpers.logger import AppLogger
#from inspect import currentframe

mod_logger = logging.getLogger(f'{APPLICATION_NAME}').getChild(f'{current_frame_name}')
#mod_logger.propagate = True
#mod_logger.debug('Entering module %s', whoami(currentframe()))
mod_logger.debug('Entering module %s', current_frame_name)
#print(f'{mod_logger.name=}')
#print(f'{mod_logger.parent=}')
#print(f'{mod_logger.parent=}')


def check_for_config_file(config_file="config.ini") -> str:
    """
    Docstring for __check_for_config_file
    
    :param confFile: Location for configuration file.
    """
    current_func_name = whoami(logging.currentframe())
    mod_logger.debug('Entering function %s', current_func_name)

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
        mod_logger.debug('Leaving function %s', current_func_name)


def process_config(config_file):
    """
    Docstring for process_config
    
    :param config_file: str -> File location of config file
    """
    current_func_name = whoami(logging.currentframe())
    mod_logger.debug('Entering function %s', current_func_name)

    try:
        from configparser import ConfigParser

        config = ConfigParser()
        config.read(config_file)

        return config
    finally:
        mod_logger.debug('Leaving function %s', current_func_name)

conf_file = check_for_config_file()
conf = process_config(conf_file)


"""
Constants Section for Config Values
"""

try:
    # Database Constants
    DB_HOSTNAME = conf.get('database','db_server',fallback='database')
    DB_PORT = conf.get('database','db_port',fallback='5432')
    DB_NAME = conf.get('database','db_name',fallback='poweripam')
    DB_USER = conf.get('database','db_username',fallback='postgres')
    DB_PASSWORD = conf.get('database','db_password',fallback='postgres')

    DB_URI = f'postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOSTNAME}:{DB_PORT}/{DB_NAME}'
    # Scheme: "postgres+psycopg2://<USERNAME>:<PASSWORD>@<IP_ADDRESS>:<PORT>/<DATABASE_NAME>"
    mod_logger.debug(f'{DB_URI=}')


    # Logging Constants
    LOG_LEVEL = logging.getLevelNamesMapping()[conf.get('logging','log_level',fallback='info').upper()]
    LOG_FILE_LEVEL = logging.getLevelNamesMapping()[conf.get('logging','log_file_level',fallback='warning').upper()]
    mod_logger.debug(f'{LOG_FILE_LEVEL=}')
    LOG_FILE = conf.get('logging','log_file',fallback='PowerIPAM.log')
    LOG_DIR = conf.get('logging','log_dir',fallback='./logs')

    LOG_LOCATION = f'{LOG_DIR}/{LOG_FILE}'
finally:
    mod_logger.debug('Leaving module %s', current_frame_name)

