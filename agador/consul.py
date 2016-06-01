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
    def _response(self, svc_name):
        """ Helper to get response from consul key value store. """
        args = "v1", "kv", "agador", "?recurse"
        endpoint = os.path.join(self.url.geturl(), *args)
        return get_config(endpoint)[svc_name]


def client(host=defaults.HOST, port=defaults.PORT, scheme=defaults.SCHEME):
    """ Get MetaClient """
    return ConsulClient(host, port, scheme)


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
        if typ == FLOAT:
            val = float(val)
        elif typ == INT:
            val = int(val)

        # Add to config
        service, obj, arg = item["Key"].split("/")[1:]
        if service not in config:
            config[service] = {}
        if obj not in config[service]:
            config[service][obj] = {}
        if arg not in config[service][obj]:
            config[service][obj][arg] = val

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
    path += "?%s" % urllib.urlencode(extras.items())
    return requests.put(path, value)
