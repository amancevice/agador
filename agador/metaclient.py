""" Mr. Met Metaservice Client. """


#import base64
import os
import pydoc
from urlparse import urlparse

import requests


class AgadorClient(object):
    """ Metaservice client.

        Arguments:
            host   (str):  Agador host
            port   (int):  Agador port
            scheme (str):  Agador scheme
            path   (str):  Agador path
    """
    def __init__(self, host, port, scheme, path):
        self.url = urlparse("%(scheme)s://%(host)s:%(port)s/%(path)s" \
            % {"scheme": scheme, "host": host, "port": port, "path": path})


    def service(self, svc_name, version):
        """ Get service.

            Arguments:
                svc_name (str):  Name of service
                version  (str):  Version of service

            Returns:
                Instance of service client.
        """
        svc_def = self.response(svc_name)
        for path, args in svc_def.iteritems():
            return pydoc.locate(path)(**args)

    def response(self, svc_name, version):
        """ Get service response.

            Arguments:
                svc_name (str):  Name of service
                version  (str):  Version of service

            Returns:
                JSON response.
        """
        if self.url.host.endswith("consul"):
            return self._consul_response(svc_name, version)
        return self._response(svc_name, version)

    def _response(self, svc_name, version):
        """ Helper to get response from agador server. """
        endpoint = os.path.join(self.url.geturl(), svc_name, version)
        response = requests.get(endpoint)
        if response.ok:
            try:
                return response.json()["service"]
            except KeyError:
                raise requests.HTTPError("Malformed JSON")
        raise requests.HTTPError("Bad Response [%d]" % response.status_code)


