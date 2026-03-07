import logging

from helpers.constants import APPLICATION_NAME
from helpers.common import whoami
import psycopg2.errors as err
from models.settings import SettingsModel
import re

current_frame_name = whoami(logging.currentframe())
mod_logger = logging.getLogger(f'{APPLICATION_NAME}').getChild(f'{current_frame_name}')
mod_logger.debug('Entering module %s', current_frame_name)

class SettingsImplementation():
    session = None

    def __init__(self,session=None):
        if session is None:
            mod_logger.critical('No current DB Session Connection...')
            raise 'Missing SESSION connection to DB...'
        
        self.session = session
        return
    
    def _getSettingByName(self,name):
        current_func_name = whoami(logging.currentframe())
        mod_logger.debug('Entering function %s', current_func_name)

        try:
            setting = self.session.query(SettingsModel).filter_by(name=name).all()
            if len(setting) > 1:
                raise err.TooManyRows('More than one row contains the same unique name...')
            elif len(setting) <= 0:
                raise err.NoDataFound('No rows found matching name=%s' % name)

            return setting[0]


        finally:
            mod_logger.debug('Leaving function %s', current_func_name)
    
    def _getSettingById(self,id):
        return
    
mod_logger.debug('Leaving module %s', current_frame_name)
    
