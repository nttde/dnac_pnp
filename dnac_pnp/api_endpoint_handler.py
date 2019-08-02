#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This module handles the URL creation for API call"""


# Import builtin python libraries
import os
import sys
import json
import logging

# Import external python libraries
from colorama import init, Fore

# Source code meta data
__author__ = "Dalwar Hossain"
__email__ = "dalwar.hossain@dimensiondata.com"

# Initialize colorama
init(autoreset=True)


# Define API URL generator
def generate_api_url(host=None, api_type=None):
    """
    This function creates appropriate API URL based on vendor and api call type

    :param host: (str) IP address or FQDN
    :param api_type: (str) API call type (name) e.g. deploy-vm, nfv-status
    :return: (str) API endpoint
    """

    # Check if the collection fine is available or not
    api_collection = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), "endpoints.json"
    )
    logging.info(f"Endpoint file: {api_collection}")
    if os.path.isfile(api_collection):
        if os.access(api_collection, os.F_OK) and os.access(api_collection, os.R_OK):
            print(Fore.CYAN + "Reading API collection.....")
            with open(api_collection, "r") as collection:
                api_collection = json.load(collection)
            api_components = api_collection[api_type]
            logging.info(f"API components: {api_components}")
        else:
            print(Fore.RED + f"Read permission error")
            sys.exit(1)
    else:
        print(Fore.RED + f"Can't find API collection!")
        sys.exit(1)
    protocol = api_components["protocol"]
    api = api_components["api"]
    method = api_components["method"]
    parameters = api_components["parameters"]

    api_url = f"{protocol}://{host}{api}"

    return method, api_url, parameters
