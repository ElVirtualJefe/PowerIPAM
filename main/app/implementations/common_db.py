import logging

if __name__ == 'app.implementations.addressState':
    from app.helpers.constants import APPLICATION_NAME
    from app.helpers.common import whoami
    import app.models as models
else:
    from helpers.constants import APPLICATION_NAME
    from helpers.common import whoami
    import models as models
import psycopg2.errors as err
import re

current_frame_name = whoami(logging.currentframe())
mod_logger = logging.getLogger(f'{APPLICATION_NAME}').getChild(f'{current_frame_name}')
mod_logger.debug('Entering module %s', current_frame_name)

class DbImplementation():
    def __init__(self,session=None):
        if session == None:
            mod_logger.critical('No current DB Session Connection...')
            raise err.NullValueNotAllowed('Missing SESSION connection to DB...')
        
        self.session = session
        return
    
    def _deleteRecord(self,record):
        current_func_name = whoami(logging.currentframe())
        mod_logger.debug('Entering function %s', current_func_name)

        try:
            mod_logger.debug('Deleting record: %s' % record.id)
            #print("%r" % request)
            #newSubnet = SubnetModel(**columns)
            #sn = self._getSubnetById(id)
            self.session.delete(record)
            self.session.commit()

            mod_logger.info('Successfully deleted row(s)')

            mod_logger.debug(f'Leaving function {__name__}.{current_func_name}')
            return True

        except Exception:
            mod_logger.error('Could not delete row with ID - %s' % id)
            return False
        finally:
            mod_logger.debug('Leaving function %s', current_func_name)

    def _addRecord(self,record,model):
        current_func_name = whoami(logging.currentframe())
        mod_logger.debug('Entering function %s', current_func_name)

        try:
            mod_logger.debug('Inserting record: %s' % record.name)

            self.session.add(record)
            self.session.flush()
            new_id = record.id
            self.session.commit()
            mod_logger.info('Successfully inserted row: %s' % record)

            newRecord = self.session.query(record.__class__).filter_by(id=new_id).all()
            print(f'{newRecord=}')
            if len(newRecord) > 1:
                raise err.TooManyRows('More than one row contains the same unique ID...')
            elif len(newRecord) <= 0:
                raise err.NoDataFound('No rows found matching id=%s' % id)

            return newRecord[0]
        except Exception as e:
            raise e

        finally:
            mod_logger.debug('Leaving function %s', current_func_name)


    DELETE_RECORD = _deleteRecord
    ADD_RECORD = _addRecord

mod_logger.debug('Leaving module %s', current_frame_name)
