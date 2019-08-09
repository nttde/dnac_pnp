#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Main module for dnac-pnp"""

# Import builtin python libraries
import json
import logging
import sys

# Import external python libraries
import click

# Import custom (local) python packages
from ._validators import accepted_status_codes

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
        response_status = True
        click.secho(
            f"[#] [{response.status_code}] API call accepted by the server!", fg="green"
        )
        if "application/json" in response.headers["Content-Type"]:
            response_body = response.json()
            response_body_logging = json.dumps(
                response.json(), indent=4, sort_keys=True
            )
            logging.debug(f"{type(response_body_logging)}")
            logging.debug(f"JSON response content: {response_body_logging}")
        else:
            response_body = response.text
            logging.debug(f"Text response content: {response_body}")
        return response_status, response_body
    else:
        logging.debug(f"Response from server: {response.text}")
        click.secho(
            f"[x] Error: [{response.status_code}] ({response.reason})", fg="red"
        )
        sys.exit(1)
