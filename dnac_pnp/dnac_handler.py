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
import sys
import os
import logging

# import external python libraries
import requests
from requests.auth import HTTPBasicAuth
import urllib3
import click
from wasabi import Printer

# Import custom (local) python packages
from dnac_pnp.config_handler import config_files, load_config
from dnac_pnp.device_import_handler import import_single_device, import_bulk_device

# Initialize
msg = Printer()

# Disable SSL warning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# Login to DNAC
def _dnac_login(host=None, username=None, password=None):
    """
    This function logs into DNAC

    :param host: (str) DNAC host IP
    :param username: (str) DNAC login username
    :param password: (str) DNAC login password
    """

    url = "https://{}/dna/system/api/v1/auth/token".format(host)
    headers = {"content-type": "application/json"}
    click.secho(f"[$] Generating authentication token.....", fg="blue")
    response = requests.request(
        "POST",
        url,
        auth=HTTPBasicAuth(username, password),
        headers=headers,
        verify=False,
    )

    if response.status_code == 200:
        return response.json()["Token"]
    else:
        click.secho(f"[x] Server responded with [{response.status_code}] [{response.text}]", fg="red")
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

    msg.divider("Configurations")
    all_configs = load_config(config_files)
    dnac_configs = all_configs["dnac"]
    dnac_host = dnac_configs["host"]
    dnac_username = dnac_configs["username"]
    dnac_password = dnac_configs["password"]

    msg.divider("DNAc login/Token creation")
    click.secho(f"[*] Logging in to DNAC at [{dnac_host}].....", fg="cyan")
    try:
        token = _dnac_login(
            host=dnac_host,
            username=dnac_username,
            password=dnac_password,
        )
    except KeyError:
        click.secho(f"[x] Key Value pair missing in config file.", fg="red")
        sys.exit(1)
    logging.debug(f"Token from DNAc: {token}")
    click.secho(f"[#] Token received!", fg="green")
    msg.divider(f"Device management")
    click.secho(f"[*] Starting device management.....", fg="cyan")
    click.secho(f"[*] Attempting {import_type} device import.....", fg="cyan")
    if import_type == "single":
        import_single_device(host=dnac_host, dnac_token=token, data=inputs)
    elif import_type == "bulk":
        device_catalog_dir = os.path.join(all_configs["common"]["base_directory"], "catalog")
        device_catalog_file = os.path.join(device_catalog_dir, "DeviceImport.csv")
        click.secho(f"[*] Looking for device catalog in [{device_catalog_file}].....", fg="cyan")
        import_bulk_device(authentication_token=token)
    else:
        click.secho(f"Invalid import type!", fg="red")
        sys.exit(1)
