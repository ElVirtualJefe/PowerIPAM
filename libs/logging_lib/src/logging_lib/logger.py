"""
Docstring for main.app.helpers.logger
"""

from __future__ import annotations

from pathlib import Path
import logging
from logging.config import dictConfig
import sys
from typing import Literal, Any
from .helpers import logging_constants as con
from .helpers import logging_classes as classes

from .formatters import (
    ConsoleFormatter,
    JsonMicroserviceFormatter,
    SyslogConsoleFormatter,
)


DEFAULT_LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "json": {
            "()": JsonMicroserviceFormatter
        },
        "debug": {
            "format": con.EXTRA_LOGGING_FORMAT,
            "datefmt": con.DEFAULT_LOG_DATE_FORMAT
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
            "filename": con.DEFAULT_DEBUG_LOG_LOCATION,
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

if not Path.is_dir(con.DEFAULT_LOG_DIR):
    Path(con.DEFAULT_LOG_DIR).mkdir(644,parents=True)
#dictConfig(DEFAULT_LOGGING_CONFIG)
logging.debug('----------===== Configured default root logger =====----------')


APP_LOG_MANAGER = classes.PowerIpamLoggingManager


LogFormat = Literal["console", "json", "syslog"]


def configure_logging(
    *,
    service_name: str,
    environment: str = "development",
    version: str | None = None,
    level: int | str = logging.INFO,
    log_format: LogFormat | None = None,
) -> None:
    """
    Configure application logging.

    This function is intended to be called once by the application entry point.
    """
    if isinstance(level, str):
        level = getattr(logging, level.upper(), logging.INFO)

    if log_format is None:
        log_format = (
            "json"
            if environment.lower() in {"production", "staging"}
            else "console"
        )

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(level)

    if log_format == "syslog":
        handler.setFormatter(
            SyslogConsoleFormatter(
                service_name=service_name,
                facility=16,  # local0
            )
        )

    elif log_format == "json":
        handler.setFormatter(
            JsonMicroserviceFormatter(
                service_name=service_name,
                environment=environment,
                version=version,
            )
        )

    else:
        handler.setFormatter(
            ConsoleFormatter(
                fmt="%(asctime)s %(levelname)s %(name)s: %(message)s",
                datefmt="%Y-%m-%dT%H:%M:%S%z",
            )
        )

    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    root_logger.handlers.clear()
    root_logger.addHandler(handler)

    # Optional: reduce noisy dependency logs.
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)

def log_exception(
    logger: logging.Logger,
    message: str,
    *,
    extra: dict[str, Any] | None = None,
) -> None:
    """Log an exception with optional structured fields."""
    logger.exception(message, extra=extra or {})
