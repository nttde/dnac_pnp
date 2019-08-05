#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Main module for dnac-pnp"""

# Import builtin python libraries
import sys
import logging

# Import external python libraries
import click

# Import custom (local) python packages
from dnac_pnp.api_endpoint_handler import generate_api_url
from dnac_pnp.header_handler import get_headers
from dnac_pnp.api_call_handler import call_api_endpoint
from dnac_pnp.api_response_handler import handle_response
from dnac_pnp.device_claim_handler import get_device_id

# Source code meta data
__author__ = "Dalwar Hossain"
__email__ = "dalwar.hossain@dimensiondata.com"


# Single device import
def import_single_device(host=None, dnac_token=None, data=None):
    """
    This module imports single device into dnac

    :param host: (str) DNAc IP or FQDN
    :param dnac_token: (str) Authentication token
    :param data: (dict) API body data
    :returns: (int) Server response status code
    """

    device_serial_number = data['deviceInfo']['serialNumber']
    method, api_url, parameters = generate_api_url(host=host, api_type="import-device")
    logging.debug(f"Method: {method}, API:{api_url}, Parameters:{parameters}")
    dnac_api_headers = get_headers(auth_token=dnac_token)
    api_response = call_api_endpoint(
        method=method,
        api_url=api_url,
        data=data,
        api_headers=dnac_api_headers,
        parameters=parameters,
    )
    response_status = handle_response(response=api_response)
    if response_status:
        click.secho(f"[*] Starting CLAIM process for serial [{device_serial_number}].....", fg="cyan")
        device_id = get_device_id(dnac_host=host, authentication_token=dnac_token, serial_number=device_serial_number)


# Bulk device import
def import_bulk_device(host=None, authentication_token=None, data=None):
    """This module imports devices in bulk"""
    pass
