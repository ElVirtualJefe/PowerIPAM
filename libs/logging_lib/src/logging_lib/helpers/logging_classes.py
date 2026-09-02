from __future__ import annotations

import json
import logging
import traceback
from datetime import datetime, timezone
from typing import Any

from . import logging_constants as con

class JsonMicroserviceFormatter(logging.Formatter):

    def format(self, record:logging.LogRecord) -> str:
        log_data = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "logger": record.name,
            "message" : record.getMessage()
        }

        if hasattr(record, "trace_id"):
            log_data["trace_id"] = record.trace_id

        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)

        if hasattr(record,"__dict__"):
            standard_fields = {
                'args', 'asctime', 'created', 'exc_info', 'exc_text', 'filename',
                'funcName', 'levelname', 'levelno', 'lineno', 'module', 'msecs',
                'msg', 'name', 'pathname', 'process', 'processName', 'relativeCreated',
                'stack_info', 'thread', 'threadName', 'trace_id'
            }

            extra_fields = {k: v for k, v in record.__dict__.items() if k not in standard_fields}
            if extra_fields:
                log_data["extra"] = extra_fields

        return json.dumps(log_data)
    

    def formatTime(self, record:logging.LogRecord, datefmt: str = con.DEFAULT_LOG_DATE_FORMAT) -> str:

        ct = self.converter(record.created)
        t = time.strftime(datefmt, ct)

        return f"{t}.{int(record.msecs):03d}Z"

from contextvars import ContextVar
import uuid

trace_id_var: ContextVar[str] = ContextVar("trace_id", default="")

class TraceMicroserviceFilter(logging.Filter):

    def filter(self, record: logging.LogRecord) -> bool:

        record.trace_id = trace_id_var.get() or str(uuid.uuid4())
        return True

class PowerIpamLoggingManager():
    """
    Doctring for class MyLogger
    """

    def __init__(self,
        application_name:str="PowerIPAM-Core",
        log_level:str=con.DEFAULT_LOG_LEVEL,
        log_file_level:str=con.DEFAULT_LOG_LEVEL,
        log_location:str=con.DEFAULT_DEBUG_LOG_LOCATION
    ):

        self.application_name = application_name
        self.log_level = log_level
        self.log_file_level = log_file_level
        self.log_location = log_location

    def configure_logging(self):
        """
        Docstring for configure_logging
        """

        from logging.config import dictConfig

        LOGGING_CONFIG = {
            "version": 1,
            "disable_existing_loggers": False,
            "filters": {
                "trace_filter": {
                    "()": TraceMicroserviceFilter
                }
            },
            "formatters": {
                "json": {
                    "()": JsonMicroserviceFormatter
                },
                "syslog": {
                    "format": con.DEFAULT_LOG_FORMAT,
                    "datefmt": con.DEFAULT_LOG_DATE_FORMAT,
                    "defaults": {
                        "ip": None
                    }
                },
                "standard": {
                    "format": con.DEFAULT_LOG_FORMAT,
                    "datefmt": con.DEFAULT_LOG_DATE_FORMAT
                },
                "debug": {
                    "format": con.EXTRA_LOGGING_FORMAT,
                    "datefmt": con.DEFAULT_LOG_DATE_FORMAT
                }
            },
            "handlers": {
                "console": {
                    "level": self.log_level,
                    "formatter": "standard",
                    "class": "logging.StreamHandler",
                    "stream": "ext://sys.stdout"
                },
                "log_file": {
                    "level": self.log_file_level,
                    "formatter": "standard",
                    "class": "logging.handlers.RotatingFileHandler",
                    "filename": self.log_location,
                    "mode": "a",
                    "maxBytes": 10485760,
                    "backupCount": 5
                },
                "debug_file": {
                    "level": "DEBUG",
                    "formatter": "debug",
                    "class": "logging.handlers.RotatingFileHandler",
                    "filename": con.DEFAULT_DEBUG_LOG_LOCATION,
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
                self.application_name: {
                    "level": self.log_level,
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

    def whoami(self,frame):
        """
        Docstring for whoami
        
        :param frame: Description
        :return: Description
        :rtype: Any
        """

        from inspect import getframeinfo
        from pathlib import Path
        from os import getcwd

        frame_info = getframeinfo(frame)
        #print(f'{frame=}')
        #print(f'{frame_info.__module__=}')
        #print(f'{frame_info.function=}')
        #print(f'{frame_info.filename=}')
        #print(f'{Path(frame_info.filename).relative_to(getcwd())=}')
        module_name = ''
        for o in Path(frame_info.filename).relative_to(getcwd()).parts:
            #print(f"{o=}")
            if o == 'src':
                continue
            if not module_name == '':
                module_name += '.'
            module_name += o.split('.')[0]
        #print(f'{module_name=}')
        #filename = frame_info.filename.split('\\')[-1]
        if frame_info.function == "<module>":
            #print("It's a file...")
            return module_name
        return f'{module_name}::{frame_info.function}'
