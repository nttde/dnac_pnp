#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Main module for dnac-pnp"""

# Import builtin python libraries
import sys
import logging

# Import external python libraries
import click
from wasabi import Printer

# Import custom (local) python packages
from dnac_pnp.api_endpoint_handler import generate_api_url
from dnac_pnp.header_handler import get_headers
from dnac_pnp.api_call_handler import call_api_endpoint
from dnac_pnp.api_response_handler import handle_response
from dnac_pnp.dnac_info_handler import get_device_id, get_site_id, get_image_id

# Source code meta data
__author__ = "Dalwar Hossain"
__email__ = "dalwar.hossain@dimensiondata.com"

# Initialize
msg = Printer()


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
    image_name = data['deviceInfo']['imageName']
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
        msg.divider(f"Claiming [{device_serial_number}]")
        click.secho(f"[*] Starting CLAIM process for serial [{device_serial_number}].....", fg="cyan")
        device_id = get_device_id(dnac_host=host, authentication_token=dnac_token, serial_number=device_serial_number)
        site_id = get_site_id(dnac_host=host, authentication_token=dnac_token, site_name="Global/Demo_DE/B1/F3")
        image_id = get_image_id(dnac_host=host, authentication_token=dnac_token, image_name=image_name)
        logging.debug(f"DeviceID: {device_id}, SiteID: {site_id}, ImageID: {image_id}")


# Bulk device import
def import_bulk_device(host=None, authentication_token=None, data=None):
    """This module imports devices in bulk"""
    pass
