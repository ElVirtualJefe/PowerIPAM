""" from logging_lib.logger import APP_LOG_MANAGER

APPLICATION_NAME = "PowerIPAM-Scan_Agent"
LOG_LEVEL = "DEBUG"
LOG_FILE_LEVEL = "DEBUG"
LOG_LOCATION = "./logs/PowerIPAM-scan_agent.log"

log_manager = APP_LOG_MANAGER(
    application_name = APPLICATION_NAME,
    log_level=LOG_LEVEL,
    log_file_level=LOG_FILE_LEVEL,
    log_location=LOG_LOCATION)
 """

import logging
from logging_lib import configure_logging, set_context

configure_logging(
    service_name="scan_agent",
    environment="development",
    log_format="syslog",
    level="DEBUG"
)

logger = logging.getLogger(__name__)

set_context(
    request_id = "req-123",
    order_id="order-456"
)

logger.info("Order processed")
