import logging

from helpers.constants import APPLICATION_NAME
from helpers.common import whoami

current_frame_name = whoami(logging.currentframe())
testing_logger = logging.getLogger(f'{APPLICATION_NAME}.tests')
testing_logger.debug('Entering module %s', current_frame_name)

class PowerIPAMtesting():
    def __init__(self,session):
        from implementations import subnet,ipAddress

        self.session = session

        self.sn_impl = subnet.SubnetImplementation(self.session)
        self.ip_impl = ipAddress.IpAddressImplementation(self.session)

        return

    def do_testing(self):

        # Testing for subnets

        test_subnet_name = '192.168.47.0/24'
        test_invalid_subnet_name = '260.168.47.0/24'

        testing_logger.info('Testing valid subnet name input...')
        new_sn = self._test_create_new_subnet(name=test_subnet_name)
        if new_sn.name == test_subnet_name:
            testing_logger.info('Successfully tested inserting new subnet...')
        else:
            testing_logger.warning('Something went wrong with test of inserting new subnet...')

        testing_logger.info('Testing invalid subnet name input...')
        failed_sn = self._test_create_new_subnet(name=test_invalid_subnet_name)
        if failed_sn:
            testing_logger.info('Successfully handled invalid subnet name input...')


        # Testing for ipAddresses

        test_ip_address = '192.168.47.15'
        test_invalid_ip_address = '192.168.47.256'

        testing_logger.info('Testing valid ipAddress ip input...')
        new_ip = self._test_create_new_ip_address(name=test_ip_address,subnet_id=new_sn.id)
        if new_ip.ipAddress == test_ip_address:
            testing_logger.info('Successfully tested inserting new ipAddress...')
        else:
            testing_logger.warning('Something went wrong with test of inserting new ipAddress...')

        testing_logger.info('Testing invalid ipAddress ip input...')
        failed_ip = self._test_create_new_ip_address(name=test_invalid_ip_address,subnet_id=new_sn.id)
        if failed_ip:
            testing_logger.info('Successfully handled invalid ipAddress ip input...')

        print('Sleeping for 30 seconds...')
        from time import sleep
        sleep(30)

        # Remove previously created tests

        if self.ip_impl.removeIpAddress(new_ip):
            testing_logger.info('Successfully tested deleting new ipAddress...')

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
        except Exception as e:
            return True


    def _test_create_new_ip_address(self,name,subnet_id):
        try:
            from models.ipAddress import IpAddressModel

            ip = IpAddressModel(ipAddress=name,subnet_id=subnet_id)

            new_ip = self.ip_impl.putIpAddress(ip)
            return new_ip
            #print(new_sn_id)
        except Exception as e:
            #raise e
            return True

