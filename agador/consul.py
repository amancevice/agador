""" Consul Helper. """


import base64
import os
import urllib

import requests
from . import defaults
from . import metaclient


FLOAT = 0
INT = 1
STRING = 2


class ConsulClient(metaclient.AgadorClient):
    """ Cosul KV Client. """
    def _response(self, svc_name):
        """ Helper to get response from consul key value store. """
        return self.config()[svc_name]

    def config(self, endpoint=defaults.KVPATH):
        """ Read consul KV and translate into agador dict.

            Arguments:
                endpoint (str):  URL of consul agent KV store
        """
        config = {}
        json = requests.get(os.path.join(self.url.geturl(), endpoint)).json()
        for item in json:

            # Get typed value
            val = base64.b64decode(item["Value"])
            typ = item["Flags"]

            # Add to config
            svc, obj, arg = item["Key"].split("/")[1:]
            if svc not in config:
                config[svc] = {}
            if obj not in config[svc]:
                config[svc][obj] = {}
            if arg not in config[svc][obj]:
                if typ == FLOAT:
                    config[svc][obj][arg] = float(val)
                elif typ == INT:
                    config[svc][obj][arg] = int(val)
                else:
                    config[svc][obj][arg] = str(val)

        return config

    def load_config(self, endpoint=defaults.KVPATH, **config):
        """ Load a configuration mapping into consul.

            Arguments:
                endpoint (str):   URL of consul agent KV store
                config   (dict):  Agador configuration dict
        """
        for key, val in config.iteritems():

            # Recurse on config
            try:
                key = os.path.join(endpoint, key)
                self.load_config(key, **val)

            # Load config
            except TypeError:
                if isinstance(val, float):
                    self.load_key(key, str(val), flags=FLOAT)
                elif isinstance(val, int):
                    self.load_key(key, str(val), flags=INT)
                else:
                    self.load_key(key, str(val), flags=STRING)


    def load_key(self, path, value, **extras):
        """ Load a key into consul

            Arguments:
                path   (str):   URL to consul KV key
                value  (str):   Consul key value
                extras (dict):  Extra consul values to set (eg, flags)
        """
        path += "?%s" % urllib.urlencode(extras.items())
        return requests.put(os.path.join(self.url.geturl(), path), value)


# pylint: disable=redefined-outer-name
def client(host=defaults.HOST, port=defaults.PORT, scheme=defaults.SCHEME):
    """ Get MetaClient """
    return ConsulClient(host, port, scheme)


# pylint: disable=redefined-outer-name
def response(svc_name, host=defaults.HOST, port=defaults.PORT, scheme=defaults.SCHEME):
    """ Helper to get service. """
    return client(host, port, scheme).response(svc_name)


def service(svc_name, host=defaults.HOST, port=defaults.PORT, scheme=defaults.SCHEME):
    """ Helper to get service. """
    return client(host, port, scheme).service(svc_name)
