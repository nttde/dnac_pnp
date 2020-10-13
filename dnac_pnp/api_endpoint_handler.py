#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This module handles API endpoints"""

# Import builtin python libraries
import json
import logging
import os
import sys

# Import external python libraries
import click

# Import custom (local) python packages
from . import dnac_handler as dnac

# Source code meta data
__author__ = "Dalwar Hossain"
__email__ = "dalwar.hossain@global.ntt"


# Define API URL generator
def generate_api_url(host=None, api_type=None):
    """
    This function creates appropriate API URL based on vendor and api call type

    :param host: (str) IP or FQDN of DNAC
    :param api_type: (str) API call type (name) e.g. generate-token, import-device
    :return: (str) API endpoint
    """

    if host is None:
        host = dnac.host
    api_collection = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), "endpoints.json"
    )
    logging.debug(f"Endpoint file: {api_collection}")
    if os.path.isfile(api_collection):
        if os.access(api_collection, os.F_OK) and os.access(api_collection, os.R_OK):
            logging.debug(f"[$] Reading API collection for [{api_type}].....")
            with open(api_collection, "r") as collection:
                api_collection = json.load(collection)
            api_components = api_collection[api_type]
        else:
            click.secho(f"[X] Read permission error", fg="red")
            sys.exit(1)
    else:
        click.secho(f"[x] Can't find API collection!", fg="red")
        sys.exit(1)
    protocol = api_components["protocol"]
    api = api_components["api"]
    method = api_components["method"]
    parameters = api_components["parameters"]
    api_url = f"{protocol}://{host}{api}"
    logging.debug(f"[#] API endpoint URL created!")
    return method, api_url, parameters
