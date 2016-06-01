""" Agador Metaservice """


from . import consul
from . import defaults
from . import metaclient


__version__ = "0.0.6"


def client(host=defaults.HOST, port=defaults.PORT, scheme=defaults.SCHEME):
    """ Get MetaClient """
    return metaclient.AgadorClient(host, port, scheme)


def response(svc_name, host=defaults.HOST, port=defaults.PORT, scheme=defaults.SCHEME):
    """ Helper to get service. """
    return client(host, port, scheme).response(svc_name)


def service(svc_name, host=defaults.HOST, port=defaults.PORT, scheme=defaults.SCHEME):
    """ Helper to get service. """
    return client(host, port, scheme).service(svc_name)
