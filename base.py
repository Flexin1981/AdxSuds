from suds.xsd.doctor import Import, ImportDoctor
from suds.transport.http import HttpAuthenticated as HttpAuthenticated
from suds.transport.https import HttpAuthenticated as HttpsAuthenticated
import ssl
from base64 import encodestring
from suds.client import Client
from plugins import EnvelopeFixer
from suds.cache import ObjectCache
import re


class MyCache(ObjectCache):
    pass


class AdxBase(object):

    def __init__(self, parent):
        """
            Class constructor for the Adx device.
        :param parent:
        """
        self.parent = parent
        self.wsdl = None
        self.b64_credentials = None
        self.PREFIX = self.parent.PREFIX
        self.cache = self.parent.cache

        # This is a patch to not verify the certificate and is discouraged in the documentation.
        if (not self.parent.SSL_VERIFY) and (self.PREFIX is not "http://"):
            ssl._create_default_https_context = ssl._create_unverified_context

        self.get_namespace()

    def set_cache(self):
        """
            Method to set the cache file on and off.
        :return:
        """
        if self.cache:
            self.wsdl.set_options(cache=MyCache())
        else:
            self.wsdl.set_options(cache=None)

    def set_cache_location(self, location):
        """
            Method to allow the cache location to be changed.
        :return:
        """
        cache = self.wsdl.options.cache
        cache.setlocation = location

    def get_namespace(self):

        """
            Method to download the wsdl files from the device. and populate the supported methods.
        :return:
        """

        self.b64_credentials = encodestring(
            '%s:%s' % (
                self.parent.username,
                self.parent.password
            )
        ).replace('\n', '')

        kwargs = dict()

        if self.PREFIX == "https://":
            kwargs['transport'] = HttpsAuthenticated()
        elif self.PREFIX == "http://":
            kwargs['transport'] = HttpAuthenticated()

        self.wsdl = Client(
            "{0}{1}{2}".format(
                self.PREFIX,
                self.parent.host,
                self.WSDL
            ),
            doctor=ImportDoctor(Import('http://schemas.xmlsoap.org/soap/encoding/')),
            plugins=[EnvelopeFixer(self.parent.debug)],
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

        self.set_cache()

    def __getattr__(self, item):
        """
            This is a shortcut to the 'wsdl.service' namespace to remove the need to call this.
            It also makes the module easier to read.

            This may also shortcut the factory at some point to create adx objects.
        :param item:
        :return:
        """
        try:
            # This is the shortcut for the methods on the device.
            if hasattr(self.wsdl.service, item):
                return getattr(self.wsdl.service, item)
            elif self.__dict__[item]:
                return self.__dict__[item]

        except KeyError:
            raise AttributeError("Method {0} not recognised".format(item))

    def get_method_in(self, method):
        """
            Method to return a list of types required as inputs to a requested method.
        :param method:
        :return:
        """
        wsdl_list = str(self.wsdl)

        method_re_string = r"{0}\((.*)\)".format(method)

        return re.search(method_re_string, wsdl_list).group(1).split(",")
