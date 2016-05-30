from suds.client import Client


class AdxBase(object):

    def __init__(self, parent):
        self.parent = parent
        self.wsdl = None

        self.get_namespace()

    def get_namespace(self):
        """
            Method to download the wsdl files from the device.
        :return:
        """
        try:
            self.wsdl = Client(
                "http://{0}{1}".format(
                    self.parent.host,
                    WSDL
                ),
                self.parent.username,
                self.parent.password
            )
        except Exception:
            raise StandardError("Unable to read WSDL file from device")


class SysService(AdxBase):
    WSDL = "wsdl/sys_service.wsdl"


class Networkservice(AdxBase):
    WSDL = "wsdl/network_service.wsdl"


class SlbService(AdxBase):
    WDSL = "wsdl/slb_service.wsdl"


class SecurityService(AdxBase):
    WDSL = "wsdl/security_service.wsdl"


class GslbService(AdxBase):
    WDSL = "wsdl/gslb_service.wsdl"


class Adx(object):

    """
        This is the ADX object for interaction with the ADX device.

        You should instantiate the device in the following manner.

        device = ADX(host, username, password, port=443)
    """

    def __init__(self, host, username, password, port=443):
        """
        Class Constructor.
        """
        self.host = host
        self.username = username
        self.password = password
        self.port = port

        self.sys_service = SysService(self)
        self.network_service = Networkservice(self)
        self.slb_service = SlbService(self)
        self.security_service = SecurityService(self)
        self.gslb_service = GslbService(self)


if __name__ == '__main__':
    adx = Adx("", "", "")

