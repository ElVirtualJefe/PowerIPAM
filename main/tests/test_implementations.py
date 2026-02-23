import logging

from helpers.constants import APPLICATION_NAME
from helpers.common import whoami

current_frame_name = whoami(logging.currentframe())
testing_logger = logging.getLogger(f'{APPLICATION_NAME}.tests')
testing_logger.debug('Entering module %s', current_frame_name)

class PowerIPAMtesting():
    def __init__(self,session):
        from implementations import subnet

        self.session = session
        self.sn_impl = subnet.SubnetImplementation(self.session)

        return

    def do_testing(self):

        # Testing for subnets

        test_subnet_name = '192.168.47.0/24'
        test_invalid_subnet_name = '260.168.47.0/24'

        testing_logger.info('Testing valid subnet name input...')
        new_sn = self._test_create_new_subnet(test_subnet_name)
        if new_sn.name == test_subnet_name:
            testing_logger.info('Successfully tested inserting new subnet...')
        else:
            testing_logger.warning('Something went wrong with test of inserting new subnet...')

        testing_logger.info('Testing invalid subnet name input...')
        failed_sn = self._test_create_new_subnet(test_invalid_subnet_name)
        if failed_sn:
            testing_logger.info('Successfully handled invalid subnet name input...')


        # Testing for ipAddresses

        from implementations import ipAddress
        from models.ipAddress import IpAddressModel

        ip = IpAddressModel()


        # Remove previously created tests

        if self.sn_impl.removeSubnet(new_sn.id):
            testing_logger.info('Successfully tested deleting new subnet...')
        else:
            testing_logger.warning('Something went wrong with test of deleting new subnet...')

    def _test_create_new_subnet(self,name):
        try:
            from models.subnet import SubnetModel

            sn = SubnetModel(name=name)

            new_sn = self.sn_impl.putSubnet(sn)
            return new_sn
            #print(new_sn_id)
        except Exception:
            return True

