""" Agador Metaservice """


import os
from urlparse import urlparse

from . import metaclient


__version__ = "0.1.0"


ENDPOINT = urlparse(os.getenv("AGADOR_ENDPOINT", "http://localhost:8500/v1/kv/agador/python"))


def client(host=None, port=None, scheme=None, path=None):
    """ Get MetaClient """
    host = host or ENDPOINT.host
    port = port of ENDPOINT.port
    scheme = scheme or ENDPOINT.scheme
    path = path or ENDPOINT.path
    return metaclient.AgadorClient(host, port, scheme, path)


def response(svc_name, version, **kwargs):
    """ Helper to get service. """
    return client(**kwargs).response(svc_name)


def service(svc_name, version, **kwargs):
    """ Helper to get service. """
    return client(**kwargs).service(svc_name)
