#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This module handles the headers for API call"""

# Import builtin python libraries
import logging

# import external python libraries
import click
from wasabi import Printer

# Initialize
msg = Printer()

# Source code meta data
__author__ = "Dalwar Hossain"
__email__ = "dalwar.hossain@dimensiondata.com"


# Define get headers function
def get_headers(auth_token=None):
    """
    This function returns appropriate headers

    :param auth_token: (str) Authentication token
    :return: (dict) A python dictionary of headers
    """
    msg.divider("API header management")
    click.secho(f"[*] Generating API headers.....", fg="cyan")
    click.secho(f"[$] Setting API headers.....", fg="blue")
    headers = {"Content-Type": "application/json"}
    if auth_token is None:
        return headers
    else:
        logging.debug(f"Token in header:{auth_token}")
        click.secho(f"[$] Attaching authentication token to API header.....", fg="blue")
        headers["X-Auth-Token"] = auth_token
        click.secho(f"[#] Authentication token successfully attached to API header!", fg="green")
        logging.debug(f"Headers: {headers}")
        return headers
