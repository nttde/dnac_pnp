#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Main module for dnac-pnp"""

# Import builtin python libraries
import sys
import logging

# Import external python libraries
import click

# Import custom (local) python packages
from dnac_pnp.api_endpoint_handler import generate_api_url
from dnac_pnp.api_call_handler import get_response


# Source code meta data
__author__ = "Dalwar Hossain"
__email__ = "dalwar.hossain@dimensiondata.com"


# Retrieve device ID
def get_device_id(authentication_token=None, dnac_api_headers=None, serial_number=None):
    """
    This module retrieves the device id by serial number

    :param authentication_token: (str) Authentication token
    :param dnac_api_headers: (dict) API headers
    :param serial_number: (str) Device serial number
    :returns: (str) device ID from DNAC
    """

    method, api_url, parameters = generate_api_url(api_type="get-device-info")
    parameters["serialNumber"] = serial_number
    response_body = get_response(
        headers=dnac_api_headers,
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
def get_site_id(authentication_token=None, dnac_api_headers=None, site_name=None):
    """
    This module retrieves site id based on site name

    :param authentication_token: (str) Authentication token
    :param dnac_api_headers: (dict) DNAC api headers
    :param site_name: (str) Site name with full hierarchy
    :return: (str) site ID from DNAC
    """

    method, api_url, parameters = generate_api_url(api_type="get-site-info")
    parameters["name"] = site_name
    response_body = get_response(
        authentication_token=authentication_token,
        headers=dnac_api_headers,
        method=method,
        endpoint_url=api_url,
        parameters=parameters,
    )
    try:
        logging.debug(f"Type: {type(response_body)}")
        if response_body["status"]:
            site_id = response_body["response"][0]["id"]
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
def get_image_id(authentication_token=None, dnac_api_headers=None, image_name=None):
    """
    This module retrieves site id based on site name

    :param authentication_token: (str) Authentication token
    :param dnac_api_headers: (dict) DNAC api headers
    :param image_name: (str) Full image name with extension
    :return: (str) Image ID from DNAC
    """

    method, api_url, parameters = generate_api_url(api_type="get-image-info")
    parameters["name"] = image_name
    response_body = get_response(
        authentication_token=authentication_token,
        headers=dnac_api_headers,
        method=method,
        endpoint_url=api_url,
        parameters=parameters,
    )
    try:
        logging.debug(f"Type: {type(response_body)}")
        image_id = response_body["response"][0]["imageUuid"]
        logging.debug(f"Image ID: {image_id}")
        return image_id
    except KeyError as err:
        logging.debug(f"Error: {err}")
        click.secho(f"[x] Key not found in the response!", fg="red")
        sys.exit(1)
