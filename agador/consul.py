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
        args = "v1", "kv", "agador", "?recurse"
        endpoint = os.path.join(self.url.geturl(), *args)
        return get_config(endpoint)[svc_name]


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


def get_config(endpoint="http://localhost:8500/v1/kv/agador/?recurse"):
    """ Read consul KV and translate into agador dict.

        Arguments:
            endpoint (str):  URL of consul agent KV store
    """
    config = {}
    response = requests.get(endpoint)
    json = response.json()
    for item in json:

        # Get typed value
        val = base64.b64decode(item["Value"])
        typ = item["Flags"]

        # Add to config
        service, obj, arg = item["Key"].split("/")[1:]
        if service not in config:
            config[service] = {}
        if obj not in config[service]:
            config[service][obj] = {}
        if arg not in config[service][obj]:
            if typ == FLOAT:
                config[service][obj][arg] = float(val)
            elif typ == INT:
                config[service][obj][arg] = int(val)
            else:
                config[service][obj][arg] = str(val)

    return config


def load_config(endpoint="http://localhost:8500/v1/kv/agador", **config):
    """ Load a configuration mapping into consul.

        Arguments:
            endpoint (str):   URL of consul agent KV store
            config   (dict):  Agador configuration dict
    """
    for key, val in config.iteritems():

        # Recurse on config
        try:
            key = os.path.join(endpoint, key)
            load_config(key, **val)

        # Load config
        except TypeError:
            if isinstance(val, float):
                load_key(key, str(val), flags=FLOAT)
            elif isinstance(val, int):
                load_key(key, str(val), flags=INT)
            else:
                load_key(key, str(val), flags=STRING)


def load_key(path, value, **extras):
    """ Load a key into consul

        Arguments:
            path   (str):   URL to consul KV key
            value  (str):   Consul key value
            extras (dict):  Extra consul values to set (eg, flags)
    """
    path += "?%s" % urllib.urlencode(extras.items())
    return requests.put(path, value)
