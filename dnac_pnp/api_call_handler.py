#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This module handles the API calls"""

# Import builtin python libraries
import sys
import json
import logging

# Import external python libraries
import requests
from requests.exceptions import HTTPError
import click
from wasabi import Printer

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

    if data:
        click.secho(f"[*] Checking payload.....", fg='cyan')
        try:
            json_input = json.loads([data])
        except TypeError:
            click.secho(f"[!] Warning: Input data stream is not valid JSON!", fg="yellow")
            logging.debug(f"Input data is not valid JSON format")
            click.secho(f"[$] Trying to convert the input stream into JSON.....", fg="blue")
            try:
                json_input = json.dumps([data], indent=4, sort_keys=True)
                logging.debug(f"JSON formatted payload: {json_input}")
                click.secho(f"[#] Payload converted into valid JSON!", fg="green")
            except Exception as err:
                logging.debug(f"Error: {err}")
                click.secho(f"Error! while creating json object", fg="red")
                sys.exit(1)
    else:
        json_input = None
    click.secho(f"[$] Making API call.....", fg="blue")
    try:
        response = requests.request(
            method,
            api_url,
            data=json_input,
            headers=api_headers,
            params=parameters,
            verify=False,
        )
        response.raise_for_status()
    except HTTPError as http_err:
        click.secho(f"[X] HTTP Error! ERROR: {http_err}", fg="red")
        sys.exit(1)
    except Exception as err:
        click.secho(f"[x] ERROR: {err}", fg="red")
        sys.exit(1)
    else:
        return response
