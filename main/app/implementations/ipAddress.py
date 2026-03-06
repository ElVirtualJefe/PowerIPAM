import logging

from helpers.constants import APPLICATION_NAME
from helpers.common import whoami
import psycopg2.errors as err
from models.ipAddress import IpAddressModel
import re

current_frame_name = whoami(logging.currentframe())
mod_logger = logging.getLogger(f'{APPLICATION_NAME}').getChild(f'{current_frame_name}')
mod_logger.debug('Entering module %s', current_frame_name)

class IpAddressImplementation():
    session = None
    re_pattern_ip = r'^(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'

    def __init__(self,session=None):
        if session == None:
            mod_logger.critical('No current DB Session Connection...')
            raise 'Missing SESSION connection to DB...'
        
        self.session = session
        return

    def putIpAddress(self,request):
        current_func_name = whoami(logging.currentframe())
        mod_logger.debug('Entering function %s', current_func_name)

        try:
            print(f'{request!r}')
            if request.ipAddress == None or request.ipAddress == '':
                raise err.InvalidParameterValue('ipAddress is missing...')
            if re.match(self.re_pattern_ip,request.ipAddress) == None:
                raise err.InvalidParameterValue('ipAddress is not a valid ipAddress')
            
            if request.is_gateway == None:
                request.is_gateway = False
            if request.is_available == None:
                request.is_available = False
            if request.subnet_id == None:
                raise err.InvalidParameterValue('Missing or Invalid subnet_id...')
            if request.state_id == None:
                from implementations import settings,addressState
                set_impl = settings.SettingsImplementation(self.session)
                as_impl = addressState.AddressStateImplementation(self.session)
                setting = set_impl._getSettingByName('default_address_state').value
                #print(f'{setting=}')
                request.state_id = as_impl._getIpAddressStateByName(setting).id
                #print(request.state_id)
                #raise 'Killing for logging purposes...'

            
            return self._addIpAddress(request)
        except err.InvalidParameterValue as e:
            raise e
        except Exception as e:
            mod_logger.error('Something went wrong...')
            mod_logger.error(e)
            raise e
        finally:
            mod_logger.debug('Leaving function %s', current_func_name)

    def getIpAddress(self,request,context,session=None):
        current_func_name = whoami(logging.currentframe())
        mod_logger.debug('Entering function %s', current_func_name)

        try:
            print('')
        finally:
            mod_logger.debug('Leaving function %s', current_func_name)

        return
    
    def removeIpAddress(self,id):
        current_func_name = whoami(logging.currentframe())
        mod_logger.debug('Entering function %s', current_func_name)

        try:
            mod_logger.debug('Deleting record: %s' % id)
            print(id)
            return self._deleteIpAddress(id)

        finally:
            mod_logger.debug('Leaving function %s', current_func_name)

    def _addIpAddress(self,request):
        current_func_name = whoami(logging.currentframe())
        mod_logger.debug('Entering function %s', current_func_name)

        try:
            print("%r" % request)
            #newIp = IpAddressModel(**columns)
            self.session.add(request)
            self.session.flush()
            new_id = request.id
            self.session.commit()

            ip = self.session.query(IpAddressModel).filter_by(id=new_id).first()
            return ip
        finally:
            mod_logger.debug('Leaving function %s', current_func_name)

    def _getIpAddressById(self,id) -> IpAddressModel:
        current_func_name = whoami(logging.currentframe())
        mod_logger.debug('Entering function %s', current_func_name)

        try:
            print(f'{ip=}')
            ip = self.session.query(IpAddressModel).filter_by(id=id).all()

            if len(ip) > 1:
                raise err.TooManyRows('More than one row contains the same unique ID...')
            elif len(ip) <= 0:
                raise err.NoDataFound('No rows found matching id=%s' % id)

            return ip[0]
        finally:
            mod_logger.debug('Leaving function %s', current_func_name)

    def _deleteIpAddress(self,id):
        current_func_name = whoami(logging.currentframe())
        mod_logger.debug('Entering function %s', current_func_name)

        try:
            mod_logger.debug('Deleting record: %s' % id)
            #print("%r" % request)
            #newSubnet = SubnetModel(**columns)
            ip = self._getIpAddressById(id)
            self.session.delete(ip)
            self.session.commit()

            mod_logger.info('Successfully deleted row(s) - %s' % ip)

            mod_logger.debug(f'Leaving function {__name__}.{current_func_name}')
            return True

        except Exception:
            mod_logger.error('Could not delete row with ID - %s' % id)
            return False
        finally:
            mod_logger.debug('Leaving function %s', current_func_name)


mod_logger.debug('Leaving module %s', current_frame_name)
