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
from .api_call_handler import get_response
from .api_endpoint_handler import generate_api_url

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
    _, response_body = get_response(
        headers=dnac_api_headers,
        authentication_token=authentication_token,
        method=method,
        endpoint_url=api_url,
        parameters=parameters,
    )
    try:
        device_id = response_body[0]["id"]
        device_state = response_body[0]["deviceInfo"]["state"]
        logging.debug(f"Device ID: {device_id}")
        click.secho(f"[#] Device ID received!", fg="green")
        return device_id, device_state
    except KeyError as err:
        click.secho(f"[x] Key not found in the response!", fg="red")
        logging.debug(f"Error: {err}")
        sys.exit(1)
    except IndexError as err:
        click.secho(
            f"[!] Index error! Device might not be available in PnP", fg="yellow"
        )
        logging.debug(f"Error: {err}")
        device_state = "Unavailable"
        return False, device_state


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
    _, response_body = get_response(
        authentication_token=authentication_token,
        headers=dnac_api_headers,
        method=method,
        endpoint_url=api_url,
        parameters=parameters,
    )
    try:
        logging.debug(f"Type: {type(response_body)}")
        response_json = json.loads(response_body)
        if response_json["status"]:
            site_id = response_json["response"][0]["id"]
            logging.debug(f"Site ID: {site_id}")
            click.secho(f"[#] Site ID received!", fg="green")
            return site_id
        else:
            err_msg = response_json["message"][0]
            click.secho(f"[*] Message: {err_msg}", fg="cyan")
            return False
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
    _, response_body = get_response(
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
        click.secho(f"[#] Image ID received!", fg="green")
        return image_id
    except KeyError as err:
        logging.debug(f"Error: {err}")
        click.secho(f"[x] Key not found in the response!", fg="red")
        sys.exit(1)
