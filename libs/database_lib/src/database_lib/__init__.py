
"""
from logging_lib.logger import APP_LOG_MANAGER
from logging import getLogger

APPLICATION_NAME = "PowerIPAM-Database_Library"
LOG_FILE_LEVEL = "DEBUG"
LOG_LOCATION = "./logs/PowerIPAM-database_lib.log"

log_manager = APP_LOG_MANAGER(
    application_name = APPLICATION_NAME,
    log_file_level=LOG_FILE_LEVEL,
    log_location=LOG_LOCATION)
log_manager.configure_logging()
app_logger = getLogger(log_manager.application_name)
app_logger.debug("---+++  Initialized Logger for %s  +++---",APPLICATION_NAME)

"""

#from logging import currentframe
#from logging_lib import set_context, get_logger
from logging_lib import configure_logging, set_context, remove_context, get_logger, whoami

if __package__:
    from .config import get_database_settings
else:
    from config import get_database_settings

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
