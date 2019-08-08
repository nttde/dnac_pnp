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

# Import custom (local) python packages
from dnac_pnp.header_handler import get_headers
from dnac_pnp.api_response_handler import handle_response

# Source code meta data
__author__ = "Dalwar Hossain"
__email__ = "dalwar.hossain@dimensiondata.com"


# Check payload and convert if required
def _check_payload(payload=None, check=None):
    """
    This private function check payload for different API calls

    :param payload: (dict) Payload body of API call
    :param check: (boolean) True or False it check the payload or not
    :returns: (json) payload in json format
    """
    if check:
        try:
            json_input = json.loads([payload])
            return json_input
        except TypeError:
            click.secho(
                f"[!] Warning: Input data stream is not valid JSON!", fg="yellow"
            )
            logging.debug(f"Input data is not valid JSON format")
            click.secho(
                f"[$] Trying to convert the input stream into JSON.....", fg="blue"
            )
            try:
                json_input = json.dumps([payload], indent=4, sort_keys=True)
                logging.debug(f"JSON formatted payload: {json_input}")
                click.secho(f"[#] Payload converted into valid JSON!", fg="green")
                return json_input
            except Exception as err:
                logging.debug(f"Error: {err}")
                click.secho(f"Error! while creating json object", fg="red")
                sys.exit(1)
    else:
        json_input = json.dumps(payload, indent=4, sort_keys=True)
        return json_input


# Define a private method to make the api call
def call_api_endpoint(
    method=None,
    api_url=None,
    data=None,
    api_headers=None,
    parameters=None,
    auth=None,
    check_payload=True,
):
    """
    This module makes the API call

    :param method: (str) API call method e.g. GET, POST etc
    :param api_url: (str) API endpoint
    :param data: (str) API call payload body [should be JSON]
    :param api_headers: (dict) API headers to be appended to the call
    :param parameters: (dict) Querystring for the API call
    :param auth: (base64) Authentication string
    :param check_payload: (boolean) whether to check the payload or not
    :returns: (response) Python requests response
    """

    if data:
        if check_payload:
            click.secho(f"[*] Checking payload.....", fg="cyan")
            json_input = _check_payload(payload=data, check=True)
        else:
            json_input = _check_payload(payload=data, check=False)
    else:
        json_input = None
    click.secho(f"[$] Making API call.....", fg="blue")
    try:
        response = requests.request(
            method,
            api_url,
            data=json_input,
            headers=api_headers,
            auth=auth,
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


# API call control for device id, site id
def get_response(
    authentication_token=None, method=None, endpoint_url=None, headers=None, parameters=None
):
    """
    This private method returns response body as json (if applicable)

    :param authentication_token:  (str) Authentication token for X-Auth-Token header
    :param method: (str) http/https
    :param endpoint_url: (str) API call endpoint
    :param headers: (dict) API headers
    :param parameters: (dict) API call parameters
    :return: (json) Response body
    """

    if headers is None:
        headers = get_headers(auth_token=authentication_token)
    api_response = call_api_endpoint(
        method=method, api_url=endpoint_url, api_headers=headers, parameters=parameters
    )
    response_status = handle_response(response=api_response)
    if response_status:
        if "application/json" in api_response.headers["content-type"]:
            response_body = api_response.json()
            return response_body
        if "text/plain" in api_response.headers["content-type"]:
            try:
                response_body = json.loads(api_response.text)
                return response_body
            except TypeError:
                click.secho(f"[x] Error")
                sys.exit(1)
        else:
            click.secho(
                "[!] Warning: Response from server is not valid JSON", fg="yellow"
            )
            sys.exit(1)
