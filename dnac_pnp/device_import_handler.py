#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Main module for dnac-pnp"""

# Import builtin python libraries
import sys
import json
import logging

# Import external python libraries
import click

# Import custom (local) python packages
from dnac_pnp.api_endpoint_handler import generate_api_url
from dnac_pnp.api_call_handler import call_api_endpoint
from dnac_pnp._validators import accepted_status_codes

# Source code meta data
__author__ = "Dalwar Hossain"
__email__ = "dalwar.hossain@dimensiondata.com"


# Single device import
def import_single_device(host=None, api_headers=None, data=None):
    """
    This module imports single device into dnac

    :param host: (str) DNAc IP or FQDN
    :param api_headers: (dict) API headers
    :param data: (dict) API body data
    :returns: (int) Server response status code
    """

    method, api_url, parameters = generate_api_url(host=host, api_type="import-device")

    logging.info(f"Method: {method}, API:{api_url}, Parameters:{parameters}")
    response = call_api_endpoint(
        method=method,
        api_url=api_url,
        data=data,
        api_headers=api_headers,
        parameters=parameters,
    )
    if response.status_code in accepted_status_codes:
        click.secho(f"[#] Device Add API call accepted!", fg="green")
    else:
        logging.info(f"Response from server: {response.text}")
        click.secho(f"[x] Error: [{response.status_code}] ({response.reason})", fg="red")
        sys.exit(1)


# Bulk device import
def import_bulk_device(api_headers=None, **kwargs):
    """This module imports devices in bulk"""
    pass
