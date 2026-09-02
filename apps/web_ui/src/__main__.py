from logging import getLogger,currentframe
from . import log_manager,APPLICATION_NAME
app_logger = getLogger(f'{APPLICATION_NAME}').getChild(f'{log_manager.whoami(currentframe()).split(".")[0]}')
app_logger.debug('Loading db_classes...')

