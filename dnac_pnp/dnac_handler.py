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

# Import python libraries
import sys

# import external python library
import requests
from requests.auth import HTTPBasicAuth
import urllib3
from colorama import init, Fore, Back, Style

# Initialize
init(autoreset=True)

# Disable SSL warning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# Login to DNAC
def dnac_login(host=None, username=None, password=None):
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
