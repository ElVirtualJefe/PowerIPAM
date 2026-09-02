
import logging
from sqlalchemy.ext.declarative import declarative_base 

# Generic Constants
APPLICATION_NAME = "PowerIPAM Scan Agent"
APPLICATION_VERSION = "v0.0.1-alpha"

# Logging Constants
DEFAULT_LOG_FORMAT = '%(asctime)s.%(msecs)03dZ %(name)s %(processName)s[%(process)d]: %(levelname)s >>> %(message)s'
DEFAULT_LOG_DATE_FORMAT = '%Y-%m-%dT%H:%M:%S'  #2022-09-27 18:00:00.000
EXTRA_LOGGING_FORMAT = '%(asctime)s.%(msecs)03dZ %(name)s %(processName)s[%(process)d] <%(module)s.%(funcName)s:%(lineno)d> %(levelname)s >>> %(message)s'
DEFAULT_LOG_FORMATTER = logging.Formatter('%(asctime)s.%(msecs)03dZ %(name)s %(processName)s[%(process)d]: %(levelname)s >>> %(message)s', 
                                          datefmt='%Y-%m-%dT%H:%M:%S')
DEFAULT_LOG_DIR = './logs'
DEFAULT_DEBUG_LOG_FILE = 'PowerIPAM-debug.log'
DEFAULT_DEBUG_LOG_LOCATION = f'{DEFAULT_LOG_DIR}/{DEFAULT_DEBUG_LOG_FILE}'

# nmap Constants
NMAP_ARGUMENTS = {
    "pingScan": "-R -sP -PE -T4",
    "baseScan": "-T4 -PS21,22,80,443,3389 --open"
}

# Database Constants
BASE = declarative_base()
