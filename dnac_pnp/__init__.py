#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Top-level package for dnac-pnp."""

# Import builtin python libraries
import logging
from logging import NullHandler
import warnings

# Import external python libraries
from urllib3.exceptions import DependencyWarning, InsecureRequestWarning

# Import custom (local) python packages
from .__version__ import __package_name__, __version__
from .__version__ import __author__, __author_email
from .__version__ import __maintainer__, __maintainer_email__
from .__version__ import __copyright__, __license__
from . import dnac_handler

# urllib3's DependencyWarnings, InsecureRequestWarning should be silenced.
warnings.simplefilter("ignore", DependencyWarning)
warnings.simplefilter("ignore", InsecureRequestWarning)

# Set default logging handler to avoid "No handler found" warnings
logging.getLogger(__name__).addHandler(NullHandler())
