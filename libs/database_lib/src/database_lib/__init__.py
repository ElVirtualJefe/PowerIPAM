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
