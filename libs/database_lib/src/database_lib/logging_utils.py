"""
Logging helpers for shared database infrastructure
"""

import logging
import sys

try:
    from logging_lib import get_logger as _get_logging_lib_logger
    from logging_lib import SyslogConsoleFormatter
except Exception:
    _get_logging_lib_logger = None
    SyslogConsoleFormatter = None


def get_db_logger(name: str = "database_lib") -> logging.Logger:
    """
    Return a logger that:
    - uses the adjacent logging-lib if installed
    - otherwise creates a basic handler if there are no handlers
    - avoids duplicate handlers
    """
    if _get_logging_lib_logger is not None:
        try:
            logger = _get_logging_lib_logger(name)
            if logger.handlers:
                logger.propagate = False
                return logger
        except Exception:
            pass

    logger = logging.getLogger(name)

    if not logger.hasHandlers():
        handler = logging.StreamHandler(sys.stdout)
        if SyslogConsoleFormatter is not None:
            handler.setFormatter(SyslogConsoleFormatter())
        else:
            handler.setFormatter(
                logging.Formatter("%(name)s[%(process)d]: %(levelname)s %(message)s")
            )
        logger.addHandler(handler)

    logger.setLevel(logging.INFO)
    logger.propagate = False
    return logger
