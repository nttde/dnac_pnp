#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Main module for dnac-pnp"""

# Import builtin python libraries
import sys
import json
import logging

# Import external python libraries
import click

# Import custom (local) python packages
from dnac_pnp.api_endpoint_handler import generate_api_url
from dnac_pnp.header_handler import get_headers
from dnac_pnp.api_call_handler import call_api_endpoint
from dnac_pnp.api_response_handler import handle_response

# Source code meta data
__author__ = "Dalwar Hossain"
__email__ = "dalwar.hossain@dimensiondata.com"

# TODO: Get image ID for a given image name/version


# API call control for device id, site id
def _get_response(authentication_token=None, method=None, endpoint_url=None, parameters=None):
    """
    This private method returns response body as json (if applicable)

    :param authentication_token:  (str) Authentication token for X-Auth-Token header
    :param method: (str) http/https
    :param endpoint_url: (str) API call endpoint
    :param parameters: (dict) API call parameters
    :return: (json) Response body
    """

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
            click.secho("[!] Warning: Response from server is not valid JSON", fg="yellow")
            sys.exit(1)


# Retrieve device ID
def get_device_id(dnac_host=None, authentication_token=None, serial_number=None):
    """
    This module retrieves the device id by serial number

    :param dnac_host: (str) IP or FQDN for DNAc
    :param authentication_token: (str) Authentication token for X-Auth-Token header
    :param serial_number: (str) Device serial number
    :returns: (str) device ID from DNAC
    """

    method, api_url, parameters = generate_api_url(host=dnac_host, api_type="get-device-info")
    parameters["serialNumber"] = serial_number
    response_body = _get_response(
        authentication_token=authentication_token,
        method=method,
        endpoint_url=api_url,
        parameters=parameters,
    )
    try:
        device_id = response_body[0]["id"]
        logging.debug(f"Device ID: {device_id}")
        return device_id
    except KeyError as err:
        click.secho(f"[x] Key not found in the response!", fg="red")
        logging.debug(f"Error: {err}")
        sys.exit(1)


# Retrieve site ID
def get_site_id(dnac_host=None, authentication_token=None, site_name=None):
    """
    This module retrieves site id based on site name

    :param dnac_host: (str) IP or FQDN for DNAc
    :param authentication_token: (str) Authentication token for X-Auth-Token header
    :param site_name: (str) Site name with full hierarchy
    :return: (str) site ID from DNAC
    """

    method, api_url, parameters = generate_api_url(host=dnac_host, api_type="get-site-info")
    parameters["name"] = site_name
    response_body = _get_response(
        authentication_token=authentication_token,
        method=method,
        endpoint_url=api_url,
        parameters=parameters,
    )
    try:
        logging.debug(f"Type: {type(response_body)}")
        if response_body['status']:
            site_id = response_body['response'][0]['id']
            logging.debug(f"Site ID: {site_id}")
            return site_id
        else:
            click.secho(f"[x] {response_body['message']} ")
            sys.exit(1)
    except KeyError as err:
        click.secho(f"[x] Key not found in the response!", fg="red")
        logging.debug(f"Error: {err}")
        sys.exit(1)


# Retrieve image ID
def get_image_id(dnac_host=None, authentication_token=None, image_name=None):
    """
    This module retrieves site id based on site name

    :param dnac_host: (str) IP or FQDN for DNAc
    :param authentication_token: (str) Authentication token for X-Auth-Token header
    :param image_name: (str) Full image name with extension
    :return: (str) Image ID from DNAC
    """

    method, api_url, parameters = generate_api_url(host=dnac_host, api_type="get-image-info")
    parameters["name"] = image_name
    response_body = _get_response(
        authentication_token=authentication_token,
        method=method,
        endpoint_url=api_url,
        parameters=parameters,
    )
    try:
        logging.debug(f"Type: {type(response_body)}")
        image_id = response_body['response'][0]['imageUuid']
        logging.debug(f"Image ID: {image_id}")
        return image_id
    except KeyError as err:
        logging.debug(f"Error: {err}")
        click.secho(f"[x] Key not found in the response!", fg="red")
        sys.exit(1)
