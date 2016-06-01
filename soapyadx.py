from suds.client import Client
from suds.cache import ObjectCache
from suds.plugin import MessagePlugin
from sslcontext import create_ssl_context, HTTPSTransport
from base64 import encodestring
import logging


class MyCache(ObjectCache):
    pass


class EnvelopeFixer(MessagePlugin):
    """
        This is a patch to reset the body of the soap packet to the correct namespace (same as the header)
    """

    def marshalled(self, context):
        """
            Method that catches all soap packets before they get sent and changes the envelope
            body to match the header.
        :param context:
        :return:
        """
        root = context.envelope.getRoot()
        envelope = root.getChild("Envelope")
        children = envelope.getChildren()
        children[1].setPrefix(children[0].prefix)
        return context


class AdxBase(object):

    PREFIX = "https://"

    def __init__(self, parent):
        self.parent = parent
        self.wsdl = None
        self.b64_credentials = None

        self.get_namespace()

    def get_namespace(self):
        """
            Method to download the wsdl files from the device.
        :return:
        """
        self.b64_credentials = encodestring(
            '%s:%s' % (
                self.parent.username,
                self.parent.password
            )
        ).replace('\n', '')

        kwargs = dict()
        kwargs['transport'] = HTTPSTransport(create_ssl_context(False))

        self.wsdl = Client(
            "https://{0}{1}".format(
                self.parent.host,
                self.WSDL
            ),
            plugins=[EnvelopeFixer()],
            **kwargs
        )
        self.wsdl.set_options(headers={"Authorization": "Basic %s" % self.b64_credentials})
        self.wsdl.set_options(
            location="{0}{1}{2}".format(
                self.PREFIX,
                self.parent.host,
                self.LOCATION
            )
        )
        self.wsdl.set_options(cache=MyCache())
        # except Exception:
        #     raise StandardError("Unable to read WSDL file from device")


class SysService(AdxBase):
    WSDL = "/wsdl/sys_service.wsdl"
    LOCATION = "/WS/SYS"


class NetworkService(AdxBase):
    WSDL = "/wsdl/network_service.wsdl"
    LOCATION = "/WS/NET"


class SlbService(AdxBase):
    WSDL = "/wsdl/slb_service.wsdl"
    LOCATION = "/WS/SLB"


class SecurityService(AdxBase):
    WSDL = "/wsdl/security_service.wsdl"
    LOCATION = "/WS/SEC"


class GslbService(AdxBase):
    WSDL = "/wsdl/gslb_service.wsdl"
    LOCATION = "/WS/GLB"


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
        self.network_service = NetworkService(self)
        self.slb_service = SlbService(self)
        self.security_service = SecurityService(self)
        self.gslb_service = GslbService(self)

