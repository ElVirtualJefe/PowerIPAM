"""
Docstring for main.app.helpers.logger
"""

from pathlib import Path
import logging
from logging.config import dictConfig
from helpers.constants import EXTRA_LOGGING_FORMAT,DEFAULT_LOG_DATE_FORMAT,DEFAULT_DEBUG_LOG_LOCATION,DEFAULT_LOG_DIR,DEFAULT_LOG_FORMAT,APPLICATION_NAME

DEFAULT_LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
#            "json": {
#                "format": "%(asctime)s %(levelname)s %(message)s",
#                "class": "pythonjsonlogger.jsonlogger.JsonFormatter",
#            },
        "debug": {
            "format": EXTRA_LOGGING_FORMAT,
            "datefmt": DEFAULT_LOG_DATE_FORMAT
        }
    },
    "handlers": {
        "root_console": {
            "level": "INFO",
            "formatter": "debug",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout"
        },
        "debug_file": {
            "level": "DEBUG",
            "formatter": "debug",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": DEFAULT_DEBUG_LOG_LOCATION,
            "mode": "a",
            "maxBytes": 10485760,
            "backupCount": 10
        }
    },
    "loggers": {
        "": {
            "level": "NOTSET",
            "handlers": ["root_console", "debug_file"],
            "propagate": False
        }
    }
}

if not Path.is_dir(DEFAULT_LOG_DIR):
    Path(DEFAULT_LOG_DIR).mkdir(644,parents=True)
dictConfig(DEFAULT_LOGGING_CONFIG)
logging.debug('----------===== Configured default root logger =====----------')


from helpers.config import LOG_LEVEL,LOG_FILE_LEVEL,LOG_LOCATION
#from helpers.constants import DEFAULT_LOG_FORMATTER,DEFAULT_DEBUG_LOG_LOCATION,DEFAULT_LOG_FORMAT,DEFAULT_LOG_DATE_FORMAT,EXTRA_LOGGING_FORMAT

def configure_logging():
    LOGGING_CONFIG = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
#            "json": {
#                "format": "%(asctime)s %(levelname)s %(message)s",
#                "class": "pythonjsonlogger.jsonlogger.JsonFormatter",
#            },
            "syslog": {
                "format": DEFAULT_LOG_FORMAT,
                "datefmt": DEFAULT_LOG_DATE_FORMAT,
                "defaults": {
                    "ip": None
                }
            },
            "standard": {
                "format": DEFAULT_LOG_FORMAT,
                "datefmt": DEFAULT_LOG_DATE_FORMAT
            },
            "debug": {
                "format": EXTRA_LOGGING_FORMAT,
                "datefmt": DEFAULT_LOG_DATE_FORMAT
            }
        },
        "handlers": {
            "console": {
                "level": "INFO",
                "formatter": "standard",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout"
            },
            "log_file": {
                "level": LOG_FILE_LEVEL,
                "formatter": "standard",
                "class": "logging.handlers.RotatingFileHandler",
                "filename": f"{LOG_LOCATION}",
                "mode": "a",
                "maxBytes": 10485760,
                "backupCount": 5
            },
            "debug_file": {
                "level": "DEBUG",
                "formatter": "debug",
                "class": "logging.handlers.RotatingFileHandler",
                "filename": DEFAULT_DEBUG_LOG_LOCATION,
                "mode": "a",
                "maxBytes": 10485760,
                "backupCount": 10
            }
        },
        "loggers": {
            "": {
                "level": "NOTSET",
                "handlers": ["console", "debug_file"],
                "propagate": False
            },
            APPLICATION_NAME: {
                "level": LOG_LEVEL,
                "handlers": ["console", "log_file", "debug_file"],
                "propagate": False
            },
            "__main__": {
                "level": "WARNING",
                "handlers": ["log_file"],
                "propagate": True
            }
        }
    }



    dictConfig(LOGGING_CONFIG)

