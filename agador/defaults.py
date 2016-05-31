""" Agador defaults. """


import os


HOST = os.getenv("AGADOR_HOST", "localhost")
PORT = int(os.getenv("AGADOR_PORT", "9999"))
SCHEME = os.getenv("AGADOR_SCHEME", "http")
