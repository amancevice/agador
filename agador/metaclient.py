""" Mr. Met Metaservice Client. """


#import base64
import os
import pydoc
from urlparse import urlparse

import requests
from .defaults import HOST
from .defaults import PORT
from .defaults import SCHEME


class AgadorClient(object):
    """ Metaservice client.

        Arguments:
            host (str):    SyMUX microservice host
            port (int):    SyMUX microservice port
            scheme (str):  SyMUX microservice scheme
    """
    def __init__(self, host=HOST, port=PORT, scheme=SCHEME):
        self.host = host
        self.port = port
        self.scheme = scheme

    @property
    def url(self):
        """ Helper to get client URL. """
        return urlparse("%(scheme)s://%(host)s:%(port)s" \
            % {'scheme': self.scheme, 'host': self.host, 'port': self.port})

    def response(self, svc_name):
        """ Get service response.

            Arguments:
                svc_name (str):  Name of service

            Returns:
                JSON response.
        """
        if self.host.endswith("consul"):
            return self._consul_response(svc_name)
        else:
            return self._response(svc_name)

    def _response(self, svc_name):
        """ Helper to get response from agador server. """
        endpoint = os.path.join(self.url.geturl(), svc_name)
        response = requests.get(endpoint)
        if response.ok:
            try:
                return response.json()["service"]
            except KeyError:
                raise requests.HTTPError("Malformed JSON")
        raise requests.HTTPError("Bad Response [%d]" % response.status_code)

    def _consul_response(self, svc_name, consul_version="v1"):
        """ Helper to get response from consul key value store. """
        args = consul_version, "kv", "agador", svc_name, "?recurse"
        endpoint = os.path.join(self.url.geturl(), *args)
        response = requests.get(endpoint)
        if response.ok:
            raise NotImplementedError("consul not yet supported")
        raise requests.HTTPError("Bad Response [%d]" % response.status_code)

    def _load_consul(self, config, path=("v1", "kv", "agador")):
        """ Load a configuration into consul key value store. """
        try:
            for key, value in config.iteritems():
                self.load_consul(value, path + (key,))
        except AttributeError:
            endpoint = os.path.join(self.url.geturl(), *path)
            requests.put(endpoint, unicode(config))

    def service(self, svc_name):
        """ Get service.

            Arguments:
                svc_name (str):  Name of service

            Returns:
                Instance of service client.
        """
        svc = self.response(svc_name)
        obj = pydoc.locate(svc["object"])
        return obj(**svc["args"])
