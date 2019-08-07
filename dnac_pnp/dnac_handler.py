#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
First Edit
----------

First Edit Author: Kamlesh Koladiya

Email: kamlesh.koladiya@dimensiondata.com
"""

# Source code meta data
__author__ = "Dalwar Hossain"
__email__ = "dalwar.hossain@dimensiondata.com"

# Import builtin python libraries
import logging
import os
import sys

# import external python libraries
import click
import requests
import urllib3
from requests.auth import HTTPBasicAuth

# Import custom (local) python packages
from dnac_pnp.config_handler import config_files, load_config
from dnac_pnp.api_call_handler import call_api_endpoint
from dnac_pnp.api_endpoint_handler import generate_api_url
from dnac_pnp.api_response_handler import handle_response
from dnac_pnp.device_import_handler import import_single_device, device_import_in_bulk
from dnac_pnp._validators import divider

# Disable SSL warning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# Login to DNAC
def dnac_token_generator(host=None, username=None, password=None):
    """
    This function logs into DNAC

    :param host: (str) DNAC host IP
    :param username: (str) DNAC login username
    :param password: (str) DNAC login password
    :returns (str) Authentication token
    """

    headers = {"content-type": "application/json"}
    method, api_url, parameters = generate_api_url(host=host, api_type="generate-token")
    logging.debug(f"Method: {method}, API:{api_url}, Parameters:{parameters}")
    click.secho(f"[$] Generating authentication token.....", fg="blue")
    api_response = call_api_endpoint(
        method=method,
        api_url=api_url,
        api_headers=headers,
        auth=HTTPBasicAuth(username, password),
    )
    response_status, response_body = handle_response(response=api_response)
    if response_status:
        token = response_body["Token"]
    else:
        click.secho(
            f"[x] Server responded with [{api_response.status_code}] [{api_response.text}]",
            fg="red",
        )
        sys.exit(1)
    if token:
        click.secho(f"[#] Token received!", fg="green")
        return token
    else:
        click.secho(
            f"[x] Server responded with [{api_response.status_code}] [{api_response.text}]",
            fg="red",
        )
        sys.exit(1)


# Import one or more devices
def import_manager(inputs=None, import_type=None, **kwargs):
    """
    This module manages import of the device(s)

    :param inputs: (dict) A dictionary of user provided inputs
    :param import_type: (str) device import type "single" or "bulk"
    :param kwargs: (kwargs) Key value pair
    :returns: (str) import status
    """

    divider("Configurations")
    all_configs = load_config(config_files)
    dnac_configs = all_configs["dnac"]
    dnac_host = dnac_configs["host"]
    dnac_username = dnac_configs["username"]
    dnac_password = dnac_configs["password"]

    divider("Device Management")
    click.secho(f"[*] Starting device management.....", fg="cyan")
    click.secho(f"[*] Attempting {import_type} device import.....", fg="cyan")
    # ==================== SINGLE DEVICE IMPORT ===========================================
    if import_type == "single":
        token = dnac_token_generator(
            host=dnac_host, username=dnac_username, password=dnac_password
        )
        import_single_device(host=dnac_host, dnac_token=token, data=inputs)
    # =================== IMPORT  IN BULK =================================================
    elif import_type == "bulk":
        if "device_catalog" not in kwargs:
            device_catalog_dir = os.path.join(
                all_configs["common"]["base_directory"], "catalog"
            )
            device_catalog_file = os.path.join(device_catalog_dir, "DeviceImport.csv")
            click.secho(
                f"[*] Looking for device catalog file in [{device_catalog_file}].....",
                fg="cyan",
            )
        else:
            device_catalog_file = kwargs.get("device_catalog")
            click.secho(
                f"[#] Using device import catalog file from: [{device_catalog_file}]",
                fg="green",
            )
        device_import_in_bulk(host=dnac_host, import_file=device_catalog_file)
    else:
        click.secho(f"Invalid import type!", fg="red")
        sys.exit(1)


# DNA center device deletion
def delete_devices(serials=None):
    """
    This function deletes one or more devices form DNAC PnP"

    :param serials: (str) comma separated string of serial numbers
    :return: (str) delete status on the screen
    """

    pass
