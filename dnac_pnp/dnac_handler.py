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

# import external python libraries
import requests
from requests.auth import HTTPBasicAuth
import urllib3
from colorama import init, Fore
from wasabi import Printer

# Import custom (local) python packages
from dnac_pnp.config_handler import config_files, load_config
from dnac_pnp.header_handler import get_headers

# Initialize
init(autoreset=True)
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
    print(Fore.YELLOW + f"Logging in to DNAC at [{host}].....")
    response = requests.request(
        "POST",
        url,
        auth=HTTPBasicAuth(username, password),
        headers=headers,
        verify=False,
    )
    return response.json()["Token"]


# Import one or more devices
def import_manager(**kwargs):
    """
    This module manages import of the device(s)

    :param kwargs: (kwargs) Key value pair
    :returns: (str) import status
    """

    msg.divider("Configurations")
    all_configs = load_config(config_files)
    dnac_configs = all_configs['dnac']

    msg.divider("DNAc login/Token creation")
    try:
        token = _dnac_login(host=dnac_configs['host'], username=dnac_configs['username'], password=dnac_configs['password'])
    except KeyError:
        print(Fore.RED + "Key Value pair missing in config file.")
        sys.exit(1)
    print(Fore.GREEN + "Token received!")

    msg.divider("API header management")
    print(Fore.BLUE + f"Generating API headers.....")
    api_headers = get_headers()
    print(Fore.BLUE + f"Attaching authentication token to API header.....")
    api_headers['X-Auth-Token'] = token
    print(Fore.GREEN + f"Authentication token successfully attached to API header!")

    msg.divider(f"Device import")
    device_catalog_dir = os.path.join(all_configs['common']['base_directory'], 'catalog')
    device_catalog_file = os.path.join(device_catalog_dir, 'dnac_device_catalog.csv')
    print(Fore.YELLOW + f"Looking for device catalog in [{device_catalog_file}].....")
