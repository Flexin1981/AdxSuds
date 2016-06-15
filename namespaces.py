from base import AdxBase


class SysService(AdxBase):
    """
        This is a step through class to follow the structure os the ADX api
    """
    WSDL = "/wsdl/sys_service.wsdl"
    LOCATION = "/WS/SYS"


class NetworkService(AdxBase):
    """
        This is a step through class to follow the structure os the ADX api
    """
    WSDL = "/wsdl/network_service.wsdl"
    LOCATION = "/WS/NET"


class SlbService(AdxBase):
    """
        This is a step through class to follow the structure os the ADX api
    """
    WSDL = "/wsdl/slb_service.wsdl"
    LOCATION = "/WS/SLB"


class SecurityService(AdxBase):
    """
        This is a step through class to follow the structure os the ADX api
    """
    WSDL = "/wsdl/security_service.wsdl"
    LOCATION = "/WS/SEC"


class GslbService(AdxBase):
    """
        This is a step through class to follow the structure os the ADX api
    """
    WSDL = "/wsdl/gslb_service.wsdl"
    LOCATION = "/WS/GLB"
