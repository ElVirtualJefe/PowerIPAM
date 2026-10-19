"""
Shared logging configuration helpers.

Important: this module is intentionally side-effect free. Libraries must not
configure global logging at import time. Call configure_logging() from the
application entry point when you want to apply a concrete logging policy.
"""

from __future__ import annotations

import logging
#from logging.config import dictConfig
import sys
from typing import Literal, Any
from .helpers import logging_constants as con

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


LogFormat = Literal["console", "json", "syslog"]


def _make_stream_logger(
        *,
        service_name: str,
        environment: str,
        version: str | None,
        level: int | str,
        log_format: LogFormat
) -> logging.Handler:
    """
    Create a logging handler that writes to stdout with the given configuration.
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

    return handler


def configure_logging(
    *,
    service_name: str,
    environment: str = "development",
    version: str | None = None,
    level: int | str = logging.INFO,
    log_format: LogFormat | None = None,
    logger_name: str | None = None,
    override_root: bool = False
) -> None:
    """
    Configure logging for the application.

    By default this function will only attach a configured handler to the
    named logger (logger_name). If logger_name is None and override_root is
    False the function will configure the root logger handler but will NOT
    clear existing handlers. If override_root is True, the root logger's
    handlers will be cleared and replaced (use with care).

    Typical usage from an application:
      configure_logging(service_name=\"my-service\", environment=\"production\",
                        log_format=\"json\", logger_name=\"my.service\")
      logger = logging.getLogger(\"my.service\")
    """

    if log_format is None:
        log_format = (
            "json"
            if environment.lower() in {"production", "staging"}
            else "console"
        )

    handler = _make_stream_logger(
        service_name=service_name,
        environment=environment,
        version=version,
        level=level,
        log_format=log_format
    )

    if logger_name:
        logger = logging.getLogger(logger_name)
        logger.setLevel(level)
        logger.addHandler(handler)
        logger.propagate = False
    else:
        root_logger = logging.getLogger()
        root_logger.setLevel(level)

        if override_root:
            root_logger.handlers.clear()
        
        root_logger.addHandler(handler)


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)


def get_structured_logger(
    name: str,
    *,
    service_name: str,
    environment: str = "development",
    version: str | None = None,
    level: int | str = logging.INFO,
    log_format: LogFormat | None = None
) -> logging.Logger:
    """
    Convenience: create (or get) a logger and attach a structured handler
    to it. This does not touch the root logger and sets propagate=False,
    so the returned logger is isolated from other handlers unless the caller
    wants to re-enable propagation.
    """
    configure_logging(
        service_name=service_name,
        environment=environment,
        version=version,
        level=level,
        log_format=log_format,
        logger_name=name,
        override_root=False
    )
    return get_logger(name)


def log_exception(
    logger: logging.Logger,
    message: str,
    *,
    extra: dict[str, Any] | None = None,
) -> None:
    """Log an exception with optional structured fields."""
    logger.exception(message, extra=extra or {})
