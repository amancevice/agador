""" Agador Metaservice

    Usage:
        agador [options]

    Options:
        -c --config URI  # Service config URI
        -d --debug       # Run in debug mode
        -h --host HOST   # Host IP [default: 0.0.0.0]
        -p --port PORT   # Port no [default: 9999]
"""


import furi
from envopt import envopt
from flask import Flask
from flask import jsonify
from . import __version__


APP = Flask("Agador")
OPT = envopt(__doc__, env_prefix="MRMET")


def config():
    """ Helper to get server config. """
    return dict(furi.map(OPT["--config"]))

@APP.route("/")
def version():
    """ Health Check. """
    return jsonify(version=__version__, services=config())


@APP.route("/<svc>")
def service(svc):
    """ Get microservice. """
    return jsonify(service=config().get(svc, {}))


def runserver():
    """ Run microservice. """
    # Strip -- from opts
    opts = dict((key.lstrip("-"), val) for key, val in OPT.iteritems())
    opts["port"] = int(opts["port"])
    del opts["config"]

    # Try to load config
    config()

    # Start engine!
    APP.run(**opts)
