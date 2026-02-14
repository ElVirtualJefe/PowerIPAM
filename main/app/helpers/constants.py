
import logging
from pathlib import Path

# Generic Constants
APPLICATION_NAME = "PowerIPAM"
APPLICATION_VERSION = "v0.0.1-alpha"

# Logging Constants
DEFAULT_LOG_FORMAT = '%(asctime)sZ %(name)s %(processName)s[%(process)d]: %(levelname)s >>> %(message)s'
DEFAULT_LOG_FORMATTER = logging.Formatter('%(asctime)s.%(msecs)dZ %(name)s %(processName)s[%(process)d]: %(levelname)s >>> %(message)s', 
                                          datefmt='%Y-%m-%dT%H:%M:%S')
DEFAULT_LOG_DIR = './logs'
DEFAULT_DEBUG_LOG_FILE = 'PowerIPAM-debug.log'
DEFAULT_DEBUG_LOG_LOCATION = f'{DEFAULT_LOG_DIR}/{DEFAULT_DEBUG_LOG_FILE}'