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

    def __getattr__(self, item):
        """
            Method to build the namespaces from the WSDL file upon first request.
        :param item:
        :return:
        """
        if hasattr(self, item):
            return self.__dict__[item]

        if item in self.NAMESPACES.keys():
            self.__setattr__(item, self.NAMESPACES[item](self))
        else:
            raise AttributeError()

    def get_namespaces(self):
        """
            Method to show the available Namespaces.
        :return:
        """
        pprint.pprint(self.NAMESPACES.keys())
