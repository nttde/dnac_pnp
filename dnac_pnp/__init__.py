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
from . import utils
from .api_call_handler import call_api_endpoint, get_response
from .api_endpoint_handler import generate_api_url
from .api_response_handler import handle_response
from .dnac_handler import import_manager, delete_manager
from .header_handler import get_headers

# urllib3's DependencyWarnings, InsecureRequestWarning should be silenced.
warnings.simplefilter('ignore', DependencyWarning)
warnings.simplefilter('ignore', InsecureRequestWarning)

# Set default logging handler to avoid "No handler found" warnings
logging.getLogger(__name__).addHandler(NullHandler())

# Package Metadata
__package_name__ = "dnac_pnp"
__author__ = """NTT Dimensiondata PS Automation Team"""
__email__ = "DE.PS.DI.Automation@dimensiondata.com"
__version__ = "0.2.2"
__license__ = "ntt-eula-1.0.1"

