import sys

sys.path.append("/path/to/pyCAF/repository
")

import pycaf.importer as importer
import pycaf.analyzer as analyzer
import pycaf.tools as tools
import pycaf.architecture as archi

import re
import urllib2
from subprocess import call

config = tools.GeneralConfigParse()
logs = tools.create_logger(__name__, config, True)
