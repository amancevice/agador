""" Mr. Met Metaservice Client. """


import importlib
import os

import requests
from urlparse import urlparse
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
        endpoint = os.path.join(self.url.geturl(), svc_name)
        response = requests.get(endpoint)
        if response.ok:
            try:
                return response.json()["service"]
            except KeyError:
                raise requests.HTTPError("Malformed JSON")
        raise requests.HTTPError("Bad Response [%d]" % response.status_code)

    def service(self, svc_name):
        """ Get service.

            Arguments:
                svc_name (str):  Name of service

            Returns:
                Instance of service client.
        """
        svc = self.response(svc_name)
        mdl = importlib.import_module(**svc["module"])
        cls = getattr(mdl, svc["class"])
        return cls(**svc["args"])
