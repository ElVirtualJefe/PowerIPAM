import logging


# Logging Constants
DEFAULT_LOG_FORMAT = '%(asctime)s.%(msecs)03dZ %(name)s %(processName)s[%(process)d]: %(levelname)s >>> %(message)s'
DEFAULT_LOG_DATE_FORMAT = '%Y-%m-%dT%H:%M:%S'  #2022-09-27 18:00:00.000
EXTRA_LOGGING_FORMAT = '%(asctime)s.%(msecs)03dZ %(name)s %(processName)s[%(process)d] <%(module)s.%(funcName)s:%(lineno)d> %(levelname)s >>> %(message)s'
DEFAULT_LOG_FORMATTER = logging.Formatter('%(asctime)s.%(msecs)03dZ %(name)s %(processName)s[%(process)d]: %(levelname)s >>> %(message)s', 
                                          datefmt='%Y-%m-%dT%H:%M:%S')

DEFAULT_LOG_DIR = './logs'
DEFAULT_DEBUG_LOG_FILE = 'PowerIPAM-debug.log'
DEFAULT_DEBUG_LOG_LOCATION = f'{DEFAULT_LOG_DIR}/{DEFAULT_DEBUG_LOG_FILE}'

DEFAULT_LOG_LEVEL:str='INFO'
