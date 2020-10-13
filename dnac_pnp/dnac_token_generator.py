#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Cisco DNA center authentication token generator"""

# Import builtin python libraries
import logging
import sys

# Import external python libraries
import click
from requests.auth import HTTPBasicAuth

# Import custom (local) python packages
from .api_call_handler import call_api_endpoint, get_response
from .api_endpoint_handler import generate_api_url
from .header_handler import get_headers
from .utils import divider

# Source code meta data
__author__ = "Dalwar Hossain"
__email__ = "dalwar.hossain@global.ntt"


# Login to DNAC, generate token and return
def generate_token(configs=None):
    """
    This function logs into DNAC and generates authentication token

    :param configs: (dict) DNAC configurations
    :returns: (str) Authentication token
    """

    if configs:
        dnac_username = configs["username"]
        dnac_password = configs["password"]
    else:
        click.secho(f"[*] Please check DNA center configurations!", fg="blue")
        click.secho(f"[x] Configs not found!", fg="red")
        sys.exit(1)

    divider("Authentication")
    headers = get_headers()
    method, api_url, parameters = generate_api_url(api_type="generate-token")
    logging.debug(f"Method: {method}, API:{api_url}, Parameters:{parameters}")
    click.secho(f"[$] Generating authentication token.....", fg="blue")
    api_response = call_api_endpoint(
        method=method,
        api_url=api_url,
        api_headers=headers,
        auth=HTTPBasicAuth(dnac_username, dnac_password),
    )
    response_status, response_body = get_response(response=api_response)
    if response_status:
        token = response_body["Token"]
    else:
        click.secho(
            f"[x] Server response [{api_response.status_code}] [{api_response.text}]",
            fg="red",
        )
        sys.exit(1)
    if token:
        click.secho(f"[#] Token received!", fg="green")
        return token
    else:
        click.secho(
            f"[x] Server response [{api_response.status_code}] [{api_response.text}]",
            fg="red",
        )
        sys.exit(1)
