import logging

if __name__ == 'app.implementations.addressState':
    from app.helpers.constants import APPLICATION_NAME
    from app.helpers.common import whoami
    from app.models.addressState import AddressStateModel
else:
    from helpers.constants import APPLICATION_NAME
    from helpers.common import whoami
    from models.addressState import AddressStateModel
import psycopg2.errors as err
import re

current_frame_name = whoami(logging.currentframe())
mod_logger = logging.getLogger(f'{APPLICATION_NAME}').getChild(f'{current_frame_name}')
mod_logger.debug('Entering module %s', current_frame_name)

class AddressStateImplementation():
    session = None
    DEFAULT_STATES = ('OFFLINE','ONLINE','RESERVED','UNUSED')

    def __init__(self,session):
        if session == None:
            mod_logger.critical('No current DB Session Connection...')
            raise 'Missing SESSION connection to DB...'
        
        self.session = session
        
        if not self.__verify_default_states():
            mod_logger.warning('One or more Default ipAddressStates are missing...')
            mod_logger.warning('Will now attempt to re-create them...')
            for state in self.DEFAULT_STATES:
                a_s = self._getIpAddressStateByName(state=state)
                if a_s == None or len(a_s) == 0:
                    new_a_s = AddressStateModel(state=state.upper())
                    self._addAddressState(new_a_s)
        
        return
    
    def _addAddressState(self,request) -> AddressStateModel:
        current_func_name = whoami(logging.currentframe())
        mod_logger.debug('Entering function %s', current_func_name)

        try:
            mod_logger.debug('Inserting record: %s' % request.state)
            self.session.add(request)
            self.session.flush()
            new_id = request.id
            self.session.commit()

            return self._getIpAddressStateById(new_id)


        finally:
            mod_logger.debug('Leaving function %s', current_func_name)

        return
    
    def _getIpAddressStateById(self,id):
        current_func_name = whoami(logging.currentframe())
        mod_logger.debug('Entering function %s', current_func_name)

        try:
            mod_logger.debug('Attempting to get record with id = %s' % id)
            address_state = self.session.query(AddressStateModel).filter_by(id=id).all()
            print(address_state)
            if len(address_state) > 1:
                raise err.TooManyRows('More than one row contains the same unique ID...')
            elif len(address_state) <= 0:
                raise err.NoDataFound('No rows found matching id=%s' % id)
            
            return address_state[0]
        
        finally:
            mod_logger.debug('Leaving function %s', current_func_name)
    
    def _getIpAddressStateByName(self,state):
        current_func_name = whoami(logging.currentframe())
        mod_logger.debug('Entering function %s', current_func_name)

        try:
            mod_logger.debug('Attempting to get record with state = %s' % state)
            address_state = self.session.query(AddressStateModel).filter_by(state=state).first()
            print(address_state)
            mod_logger.debug(f'{address_state=}')
            return address_state if address_state == None else address_state[0]
        finally:
            mod_logger.debug('Leaving function %s', current_func_name)

    def __verify_default_states(self):
        current_func_name = whoami(logging.currentframe())
        mod_logger.debug('Entering function %s', current_func_name)

        try:
            states = self.session.query(AddressStateModel).all()
            mod_logger.debug(f'{states=}')
            states_list = []
            for s in states:
                states_list.append(s.state)

            mod_logger.debug(f'{states_list=}')

            if all(s in states_list for s in self.DEFAULT_STATES):
                return True
            else:
                return False
        finally:
            mod_logger.debug('Leaving function %s', current_func_name)

mod_logger.debug('Leaving module %s', current_frame_name)
