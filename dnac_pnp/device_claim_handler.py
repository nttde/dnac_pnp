#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Main module for dnac-pnp"""

# Import builtin python libraries
import sys
import logging

# Import external python libraries
import requests
import click

# Import custom (local) python packages
from dnac_pnp.api_endpoint_handler import generate_api_url
from dnac_pnp.header_handler import get_headers
from dnac_pnp.api_call_handler import call_api_endpoint
from dnac_pnp.api_response_handler import handle_response

# Source code meta data
__author__ = "Dalwar Hossain"
__email__ = "dalwar.hossain@dimensiondata.com"

# TODO: Get device ID by serial number
# TODO: Get site ID for the site attached to the device
# TODO: Get image ID for a given image name/version


# Retrieve device ID
def get_device_id(dnac_host=None, authentication_token=None, serial_number=None):
    """
    This module retrieves the device id by serial number

    :param dnac_host: (str) IP or FQDN for DNAc
    :param authentication_token: (str) Authentication token for X-Auth-Token header
    :param serial_number: (str) Device serial number
    :returns: (str) device ID from DNAC
    """

    method, api_url, parameters = generate_api_url(host=dnac_host, api_type="get-device-info")
    parameters['serialNumber'] = serial_number
    headers = get_headers(auth_token=authentication_token)
    api_response = call_api_endpoint(method=method, api_url=api_url, api_headers=headers, parameters=parameters)
    response_status = handle_response(response=api_response)
    if response_status:
        print(api_response.text)
