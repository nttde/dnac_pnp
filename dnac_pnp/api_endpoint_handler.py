#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This module handles the URL creation for API call"""


# Import builtin python libraries
import os
import sys
import json
import logging

# Import external python libraries
import click

# Import custom (local) python packages
from dnac_pnp.config_handler import config_files, load_config

# Source code meta data
__author__ = "Dalwar Hossain"
__email__ = "dalwar.hossain@dimensiondata.com"


# Define API URL generator
def generate_api_url(api_type=None):
    """
    This function creates appropriate API URL based on vendor and api call type

    :param api_type: (str) API call type (name) e.g. deploy-vm, nfv-status
    :return: (str) API endpoint
    """

    all_configs = load_config(config_files)
    dnac_configs = all_configs["dnac"]
    host = dnac_configs["host"]

    api_collection = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), "endpoints.json"
    )
    logging.debug(f"Endpoint file: {api_collection}")
    if os.path.isfile(api_collection):
        if os.access(api_collection, os.F_OK) and os.access(api_collection, os.R_OK):
            click.secho(f"[$] Reading API collection for [{api_type}].....", fg="blue")
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
    click.secho(f"[#] API endpoint URL created!", fg="green")
    return method, api_url, parameters
