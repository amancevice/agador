""" Agador defaults. """


import os


HOST = os.getenv("AGADOR_HOST", "localhost")
PORT = int(os.getenv("AGADOR_PORT", "8500"))
SCHEME = os.getenv("AGADOR_SCHEME", "http")
KVPATH = os.getenv("AGADOR_KVPATH", "/v1/kv/agador")
