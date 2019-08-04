#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This module handles the API calls"""

# Import builtin python libraries
import logging

# Import external python libraries
from wasabi import Printer
import requests
from requests.auth import HTTPBasicAuth
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
    :param data: (str) API call payload body
    :param api_headers: (dict) API headers to be appended to the call
    :param parameters: (dict) Querystring for the API call
    :returns: (response) Python requests response
    """

    click.secho(f"[$] Making API call.....", fg="blue")
    response = requests.request(
        method,
        api_url,
        data=data,
        headers=api_headers,
        params=parameters,
        verify=False,
    )
    return response
