from logging import currentframe
from logging_lib import configure_logging, set_context, remove_context, get_logger, whoami

from config import get_settings

settings = get_settings()

configure_logging(
    service_name=f'[{settings.service_name} {settings.service_ver}]',
    environment=settings.environment,
    log_format="syslog",
    level=settings.log_level,
    version=settings.app_ver
)


app_logger = get_logger(settings.service_name)
app_logger.debug("---+++  Initialized Logger for %s  +++---", (__name__))

app_logger.debug('Starting Core Service Process...')


