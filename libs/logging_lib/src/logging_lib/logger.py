"""
Shared logging configuration helpers.

Libraries should configure logging explicitly from the application entry point.
This module intentionally avoids import-time configuration.
"""

from __future__ import annotations

import logging
import sys
from typing import Any, Literal

from .classes import (
    ConsoleFormatter,
    JsonDatabaseLogHandler,
    JsonMicroserviceFormatter,
    SyslogConsoleFormatter,
)

LogFormat = Literal["console", "json", "syslog"]


def _normalize_level(level: int | str) -> int:
    if isinstance(level, str):
        return getattr(logging, level.upper(), logging.INFO)
    return level


def _make_stream_logger(
    *,
    service_name: str,
    environment: str,
    version: str | None,
    level: int | str,
    log_format: LogFormat | None,
) -> logging.Handler:
    """
    Create a logging handler that writes to stdout with the given configuration.
    """
    resolved_level = _normalize_level(level)

    if log_format is None:
        log_format = "json" if environment.lower() in {"production", "staging"} else "console"

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(resolved_level)

    if log_format == "syslog":
        handler.setFormatter(
            SyslogConsoleFormatter(
                service_name=service_name,
                facility=16,
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


def _logger_has_stream_handler(logger: logging.Logger) -> bool:
    return any(
        isinstance(handler, logging.StreamHandler)
        and not isinstance(handler, JsonDatabaseLogHandler)
        for handler in logger.handlers
    )


def configure_logging(
    *,
    service_name: str,
    environment: str = "development",
    version: str | None = None,
    level: int | str = logging.INFO,
    log_format: LogFormat | None = None,
    logger_name: str | None = None,
    override_root: bool = False,
    database_connection: Any | None = None,
    database_table_name: str = "application_logs",
) -> None:
    """
    Configure logging for a named logger or the root logger.

    If database_connection is supplied, JSON records are also written
    to the specified database table.
    """
    resolved_level = _normalize_level(level)

    if logger_name:
        logger = logging.getLogger(logger_name)
        logger.setLevel(resolved_level)
        logger.propagate = False

        if override_root or not _logger_has_stream_handler(logger):
            logger.handlers.clear()
            logger.addHandler(
                _make_stream_logger(
                    service_name=service_name,
                    environment=environment,
                    version=version,
                    level=resolved_level,
                    log_format=log_format,
                )
            )

        if database_connection is not None and not any(
            isinstance(existing, JsonDatabaseLogHandler) for existing in logger.handlers
        ):
            logger.addHandler(
                JsonDatabaseLogHandler(
                    connection=database_connection,
                    table_name=database_table_name,
                    service_name=service_name,
                    environment=environment,
                    version=version,
                )
            )

        return

    root_logger = logging.getLogger()
    root_logger.setLevel(resolved_level)

    if override_root:
        root_logger.handlers.clear()

    if not _logger_has_stream_handler(root_logger):
        root_logger.addHandler(
            _make_stream_logger(
                service_name=service_name,
                environment=environment,
                version=version,
                level=resolved_level,
                log_format=log_format,
            )
        )

    if database_connection is not None and not any(
        isinstance(existing, JsonDatabaseLogHandler) for existing in root_logger.handlers
    ):
        root_logger.addHandler(
            JsonDatabaseLogHandler(
                connection=database_connection,
                table_name=database_table_name,
                service_name=service_name,
                environment=environment,
                version=version,
            )
        )


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)


def get_structured_logger(
    name: str,
    *,
    service_name: str,
    environment: str = "development",
    version: str | None = None,
    level: int | str = logging.INFO,
    log_format: LogFormat | None = None,
    database_connection: Any | None = None,
    database_table_name: str = "application_logs",
) -> logging.Logger:
    """
    Convenience helper that creates or reuses a logger and attaches handlers.
    """
    configure_logging(
        service_name=service_name,
        environment=environment,
        version=version,
        level=level,
        log_format=log_format,
        logger_name=name,
        database_connection=database_connection,
        database_table_name=database_table_name,
    )
    return get_logger(name)


def log_exception(
    logger: logging.Logger,
    message: str,
    *,
    extra: dict[str, Any] | None = None,
) -> None:
    """Log an exception with optional structured metadata."""
    logger.exception(message, extra=extra or {})
