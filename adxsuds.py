import pprint
from namespaces import SysService, NetworkService, SlbService, SecurityService, GslbService


class Adx(object):

    """
        This is the ADX object for interaction with the ADX device.

        You should instantiate the device in the following manner.

        device = ADX(host, username, password)
    """

    NAMESPACES = {
        "sys": SysService,
        "network": NetworkService,
        "slb": SlbService,
        "security": SecurityService,
        "gslb": GslbService
    }

    def __init__(self, host, username, password, port=443, protocol="https", verify_ssl=True, debug=0, cache=True):
        """
            Class Constructor.
        """
        self.host = host
        self.username = username
        self.password = password
        self.port = port
        self.PREFIX = protocol + "://"
        self.SSL_VERIFY = verify_ssl
        self.debug = debug
        self.cache = cache

        self._build_namespaces()

    def _build_namespaces(self):
        for key, val in self.NAMESPACES.iteritems():
            self.__setattr__(key, val(self))

    def get_namespaces(self):
        """
            Method to show the available Namespaces.
        :return:
        """
        pprint.pprint(self.NAMESPACES.keys())


if __name__ == '__main__':

    adx = Adx("192.168.100.254", "john", "john", verify_ssl=False, debug=2)
    adx.security.getAllSslCertificateFilenames()

