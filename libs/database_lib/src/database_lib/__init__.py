
"""
Database Manager Library
"""

from logging_lib import configure_logging, set_context, remove_context, get_logger, whoami

from .config import get_database_settings

settings = get_database_settings()

configure_logging(
    service_name=f'[{settings.lib_name} {settings.lib_ver}]',
    environment=settings.environment,
    log_format="syslog",
    level=settings.log_level,
    version=settings.lib_ver
)

app_logger = get_logger(settings.lib_name)
app_logger.debug("---+++  Initialized Logger for %s  +++---", (__name__))
#app_logger.info('test log...')

app_logger.debug('Starting Database Manager Library Process...')

from .config import DatabaseSettings
from .db_classes import Base, DatabaseManager, TimestampMixin, UUIDPrimaryKeyMixin
from .alembic import run_migrations

__all__ = [
    "DatabaseSettings",
    "Base",
    "DatabaseManager",
    "TimestampMixin",
    "UUIDPrimaryKeyMixin",
    "run_migrations"
]
