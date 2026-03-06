import logging

from helpers.constants import APPLICATION_NAME
from helpers.common import whoami
import psycopg2.errors as err
from models.subnet import SubnetModel
import re

current_frame_name = whoami(logging.currentframe())
mod_logger = logging.getLogger(f'{APPLICATION_NAME}').getChild(f'{current_frame_name}')
mod_logger.debug('Entering module %s', current_frame_name)

class SubnetImplementation():
    session = None
    common_impl = None
    re_pattern_subnet = r'^(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)/(?:2[0-4]|[01]?[0-9])$'

    def __init__(self,session=None):
        if session is None:
            mod_logger.critical('No current DB Session Connection...')
            raise 'Missing SESSION connection to DB...'
        
        self.session = session

        from implementations import common_db
        self.common_impl = common_db.DbImplementation(session)

        return
    
    def _addSubnet(self,request) -> SubnetModel:
        current_func_name = whoami(logging.currentframe())
        mod_logger.debug('Entering function %s', current_func_name)

        try:
            mod_logger.debug('Inserting record: %s' % request.name)
            #print("%r" % request)
            #newSubnet = SubnetModel(**columns)
            self.session.add(request)
            self.session.flush()
            #print(f'{request.id=}')
            new_id = request.id
            self.session.commit()

            subnet = self._getSubnetById(new_id)
            mod_logger.info('Successfully inserted row: %s' % subnet)

            mod_logger.debug(f'Leaving function {__name__}.{current_func_name}')
            return subnet


        finally:
            mod_logger.debug('Leaving function %s', current_func_name)

        return None

    def _getSubnetById(self,id) -> SubnetModel:
        current_func_name = whoami(logging.currentframe())
        mod_logger.debug('Entering function %s', current_func_name)

        try:
            #print("%s" % id)
            sn = self.session.query(SubnetModel).filter_by(id=id).all()
            if len(sn) > 1:
                raise err.TooManyRows('More than one row contains the same unique ID...')
            elif len(sn) <= 0:
                raise err.NoDataFound('No rows found matching id=%s' % id)
            #self.session.add(newSubnet)
            #self.session.commit()

            #subnet = _getSubnetById(session,newSubnet.id)

            return sn[0]


        finally:
            mod_logger.debug('Leaving function %s', current_func_name)

        return None

    def _deleteSubnet(self,id):
        current_func_name = whoami(logging.currentframe())
        mod_logger.debug('Entering function %s', current_func_name)

        try:
            mod_logger.debug('Deleting record: %s' % id)
            #print("%r" % request)
            #newSubnet = SubnetModel(**columns)
            sn = self._getSubnetById(id)
            self.session.delete(sn)
            self.session.commit()

            mod_logger.info('Successfully deleted row(s)')

            mod_logger.debug(f'Leaving function {__name__}.{current_func_name}')
            return True

        except Exception:
            mod_logger.error('Could not delete row with ID - %s' % id)
            return False
        finally:
            mod_logger.debug('Leaving function %s', current_func_name)

        return None

    def putSubnet(self,request) -> SubnetModel:
        current_func_name = whoami(logging.currentframe())
        mod_logger.debug('Entering function %s', current_func_name)

        try:
            print(f'{request=}')
            print(f'{request.__class__=}')
            print(f'{request.__class__.__name__=}')
            if request.name is None or request.name == '':
                raise err.InvalidParameterValue('Value missing for Subnet/Mask')
            mod_logger.debug('Subnet name input is present - %s' % request.name)

            #print(re.match(self.re_pattern_subnet,request.name))
            if re.match(self.re_pattern_subnet,request.name) is None:
                raise err.InvalidParameterValue('Subnet/Mask combination is not valid.')
        
            return self.common_impl.ADD_RECORD(request,SubnetModel)

        except Exception as e:
            mod_logger.error('Something went wrong...')
            mod_logger.error(e)
            raise e

        finally:
            mod_logger.debug('Leaving function %s', current_func_name)

        return

    def removeSubnet(self,id=None) -> bool:
        current_func_name = whoami(logging.currentframe())
        mod_logger.debug('Entering function %s', current_func_name)

        try:
            if id == None or id == '':
                raise err.InvalidParameterValue('Value missing for Subnet/Mask ID')
        
            return self._deleteSubnet(id)

        finally:
            mod_logger.debug('Leaving function %s', current_func_name)

mod_logger.debug('Leaving module %s', current_frame_name)
