#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Main module for dnac-pnp"""

# Import builtin python libraries
import sys
import logging

# Import external python libraries
from colorama import init, Fore
from wasabi import Printer

# Import custom (local) python packages
from dnac_pnp.api_endpoint_handler import generate_api_url

# Source code meta data
__author__ = "Dalwar Hossain"
__email__ = "dalwar.hossain@dimensiondata.com"

# Initialize
init(autoreset=True)
msg = Printer()


# Single device import
def import_single_device(host=None, api_headers=None, payload=None):
    """
    This module imports single device into dnac

    :param host: (str) DNAc IP or FQDN
    :param api_headers: (dict) API headers
    :param payload: (dict) API payload (data=payload)
    :returns: (int) Server response status code
    """

    logging.info(f"Payload: {payload}")
    method, api_url, parameters = generate_api_url(host=host, api_type="import-device")
    print(method, api_url, parameters)


# Bulk device import
def import_bulk_device(api_headers=None, **kwargs):
    """This module imports devices in bulk"""
    pass
