#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Main module for dnac-pnp"""

# Import builtin python libraries
import sys
import logging
import json

# Import external python libraries
import click

# Import custom (local) python packages
from dnac_pnp._validators import accepted_status_codes

# Source code meta data
__author__ = "Dalwar Hossain"
__email__ = "dalwar.hossain@dimensiondata.com"


# API response handler
def handle_response(response=None):
    """
    This module handles the response from the server

    :param response: (requests.response object) Response from server
    :returns: (boolean) OK or NOT OK
    """

    if response.status_code in accepted_status_codes:
        click.secho(f"[#] [{response.status_code}] API call accepted!", fg="green")
        if response.headers["Content-Type"] == "application/json":
            json_response_body = json.dumps(response.json(), indent=4, sort_keys=True)
            logging.debug(f"Response content: {json_response_body}")
        else:
            logging.debug(f"Response content: {response.text}")
        return True
    else:
        logging.debug(f"Response from server: {response.text}")
        click.secho(f"[x] Error: [{response.status_code}] ({response.reason})", fg="red")
        sys.exit(1)
