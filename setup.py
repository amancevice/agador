import os
import re
from setuptools import setup

NAME           = "agador"
AUTHOR         = "amancevice"
EMAIL          = "smallweirdnum@gmail.com"
DESC           = "Agador metaservice for microservices"
PACKAGES       = ["agador"]
PACKAGE_DATA   = {"agador": ['README.md']}
REQUIRES       = ["PyYAML>=3.11", "requests>=2.10.0"]
TESTS_REQUIRE  = ["httpretty", "nose", "mock"]
ENTRYPOINTS    = {'console_scripts': ['agador=agador.microservice:runserver']}
EXTRAS_REQUIRE = {
    "server": REQUIRES + [
        "envopt>=0.1.3",
        "Flask>=0.10.1",
        "furi[aws]>=0.6.12"]}

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

def version():
    search = r"^__version__ *= *['\"]([0-9.]+)['\"]"
    initpy = read("./%s/__init__.py" % NAME)
    return re.search(search, initpy, re.MULTILINE).group(1)

setup(
    name                 = NAME,
    version              = version(),
    author               = AUTHOR,
    author_email         = EMAIL,
    packages             = PACKAGES,
    package_data         = PACKAGE_DATA,
    include_package_data = True,
    url                  = 'http://www.smallweirdnumber.com',
    description          = DESC,
    long_description     = read('README.md'),
    entry_points         = ENTRYPOINTS,
    install_requires     = REQUIRES,
    extras_require       = EXTRAS_REQUIRE,
    tests_require        = TESTS_REQUIRE,
    test_suite           = "nose.collector" )