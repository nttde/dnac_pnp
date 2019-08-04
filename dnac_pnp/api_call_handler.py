#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This module handles the API calls"""

# Import builtin python libraries
import sys
import json
import logging

# Import external python libraries
from wasabi import Printer
import requests
import click

# Source code meta data
__author__ = "Dalwar Hossain"
__email__ = "dalwar.hossain@dimensiondata.com"

# Initialize wasabi
msg = Printer()


# Define a private method to make the api call
def call_api_endpoint(
    method=None,
    api_url=None,
    data=None,
    api_headers=None,
    parameters=None,
):
    """
    This module makes the API call

    :param method: (str) API call method e.g. GET, POST etc
    :param api_url: (str) API endpoint
    :param data: (str) API call payload body [should be JSON]
    :param api_headers: (dict) API headers to be appended to the call
    :param parameters: (dict) Querystring for the API call
    :returns: (response) Python requests response
    """

    click.secho(f"[*] Checking payload.....", fg='cyan')
    try:
        json_input = json.loads(data)
    except TypeError:
        click.secho(f"[!] Warning: Input data stream is not valid JSON format!", fg="yellow")
        logging.info(f"Input data is not valid JSON format")
        click.secho(f"[$] Trying to convert the input stream into JSON.....", fg="blue")
        try:
            json_input = json.dumps([data], indent=4, sort_keys=True)
            logging.info(f"JSON formatted input: {json_input}")
        except Exception as err:
            logging.debug(f"Error: {err}")
            click.secho(f"Error! while creating json object", fg="red")
            sys.exit(1)
    click.secho(f"[$] Making API call.....", fg="blue")
    response = requests.request(
        method,
        api_url,
        data=json_input,
        headers=api_headers,
        params=parameters,
        verify=False,
    )
    return response
