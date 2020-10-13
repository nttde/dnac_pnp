#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This module handles the API calls"""

# Import builtin python libraries
import json
import logging
import sys

# Import external python libraries
import click
import requests

# Import custom (local) python packages
from .header_handler import get_headers
from .dnac_params import accepted_status_codes

# Source code meta data
__author__ = "Dalwar Hossain"
__email__ = "dalwar.hossain@global.ntt"


# Content type check
def _content_type_check(response=None):
    """This private function checks response content type"""

    if "application/json" in response.headers["Content-Type"]:
        response_body = response.json()
        response_body_logging = json.dumps(response.json(), indent=4, sort_keys=True)
        logging.debug(f"{type(response_body_logging)}")
        logging.debug(f"JSON response content: {response_body_logging}")
    else:
        response_body = response.text
        logging.debug(f"Text response content: {response_body}")
    logging.debug(f"{type(response_body)}")
    return response_body


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
            logging.debug(f"[!] Warning: Input data stream is not valid JSON!")
            logging.debug(f"Input data is not valid JSON format")
            logging.debug(f"[$] Trying to convert the input stream into JSON.....")
            try:
                json_input = json.dumps([payload], indent=4, sort_keys=True)
                logging.debug(f"JSON formatted payload: {json_input}")
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
            logging.debug(f"[*] Checking payload.....")
            json_input = _check_payload(payload=data, check=True)
        else:
            json_input = _check_payload(payload=data, check=False)
    else:
        json_input = None
    logging.debug(f"JSON INPUT (call_api_endpoint): {json_input}")
    logging.debug(f"[$] Making API call.....")
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
    except Exception as err:
        click.secho(f"[x] ERROR: {err}", fg="red")
        sys.exit(1)
    else:
        return response


# API call control for device id, site id
def get_response(
    authentication_token=None,
    method=None,
    endpoint_url=None,
    headers=None,
    parameters=None,
    response=None,
):
    """
    This private method returns response body as json (if applicable)

    :param authentication_token:  (str) Authentication token for X-Auth-Token header
    :param method: (str) http/https
    :param endpoint_url: (str) API call endpoint
    :param headers: (dict) API headers
    :param parameters: (dict) API call parameters
    :param response: (object) Python requests response object
    :return: (json) Response body
    """

    if response is None:
        if headers is None:
            headers = get_headers(auth_token=authentication_token)
        response = call_api_endpoint(
            method=method,
            api_url=endpoint_url,
            api_headers=headers,
            parameters=parameters,
        )
    if response.status_code in accepted_status_codes:
        logging.debug(f"Response status code found in accepted codes!")
        response_status = True
        logging.debug(f"[#] [{response.status_code}] API call accepted by the server!")
        response_body = _content_type_check(response=response)
    else:
        logging.debug(f"Response status code not found in accepted codes!")
        response_status = False
        logging.debug(f"Response Status: {response_status}")
        response_body = _content_type_check(response=response)
    return response_status, response_body
