import logging

from helpers.constants import APPLICATION_NAME
from helpers.common import whoami
import psycopg2.errors as err

current_frame_name = whoami(logging.currentframe())
mod_logger = logging.getLogger(f'{APPLICATION_NAME}').getChild(f'{current_frame_name}')
mod_logger.debug('Entering module %s', current_frame_name)

class IpAddressImplementation():
    def __init__():
        return

    def putIpAddress(self,request,context,session=None):
        current_func_name = whoami(logging.currentframe())
        mod_logger.debug('Entering function %s', current_func_name)

        try:
            print(request)
        finally:
            mod_logger.debug('Leaving function %s', current_func_name)

        return

    def getIpAddress(self,request,context,session=None):
        current_func_name = whoami(logging.currentframe())
        mod_logger.debug('Entering function %s', current_func_name)

        try:
            print('')
        finally:
            mod_logger.debug('Leaving function %s', current_func_name)

        return
    
    def _addIpAddress(self,session,**columns):
        current_func_name = whoami(logging.currentframe())
        mod_logger.debug('Entering function %s', current_func_name)

        from models.ipAddress import IpAddressModel

        try:
            if 'ipAddress' not in columns:
                raise err.InvalidParameterValue('Value missing for ipAddress')
            if 'is_gateway' not in columns:
                columns['is_gateway'] = False
            if 'is_available' not in columns:
                columns['is_available'] = False
#            if 'subnet_id' not in columns:
#                raise err.InvalidParameterValue('Value missing for subnet_id')
            
            for k,v in columns.items():
                mod_logger.debug(f'key {k} = {v}')

            newIp = IpAddressModel(**columns)
            session.add(newIp)
            session.commit()

            ip = session.query(IpAddressModel).filter_by(**columns).all()
            return ip
        finally:
            mod_logger.debug('Leaving function %s', current_func_name)

mod_logger.debug('Leaving module %s', current_frame_name)
