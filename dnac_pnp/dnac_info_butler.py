#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Information showcase functions"""

# Import builtin python libraries
import json
import logging
import sys

# Import external python libraries
import click

# Import custom (local) python packages
from .api_call_handler import get_response
from .api_endpoint_handler import generate_api_url
from .header_handler import get_headers

# Source code meta data
__author__ = "Dalwar Hossain"
__email__ = "dalwar.hossain@dimensiondata.com"


# Retrieve device ID
def get_device_id(
    authentication_token=None, dnac_api_headers=None, serial_number=None, dnac_tab=None
):
    """
    This function retrieves the device id by serial number

    :param authentication_token: (str) Authentication token
    :param dnac_api_headers: (dict) API headers
    :param serial_number: (str) Device serial number
    :param dnac_tab: (str) Where to look for the device info (PnP or Inventory)
    :returns: (str) device ID from DNAC
    """

    if dnac_tab == "pnp":
        dnac_api_type = "get-pnp-device-info"
    elif dnac_tab == "inventory":
        dnac_api_type = "get-inventory-device-info"
    else:
        dnac_api_type = "get-pnp-device-info"
    if dnac_api_headers is None:
        dnac_api_headers = get_headers(auth_token=authentication_token)
    method, api_url, parameters = generate_api_url(api_type=dnac_api_type)
    if serial_number is not None:
        parameters["serialNumber"] = serial_number
    _, response_body = get_response(
        headers=dnac_api_headers,
        authentication_token=authentication_token,
        method=method,
        endpoint_url=api_url,
        parameters=parameters,
    )
    try:
        if dnac_tab == "pnp":
            device_id = response_body[0]["id"]
            device_state = response_body[0]["deviceInfo"]["state"]
            logging.debug(f"Device ID: {device_id}")
        if dnac_tab == "inventory":
            device_id = response_body["response"][0]["id"]
            device_state = response_body["response"][0]["collectionStatus"]
            logging.debug(f"Device ID: {device_id}")
        return device_id, device_state
    except KeyError as err:
        click.secho(f"[x] Key not found in the response!", fg="red")
        logging.debug(f"Error: {err}")
        sys.exit(1)
    except IndexError as err:
        click.secho(f"[!] Index error! "
                    f"Device might not be available in PnP", fg="yellow")
        logging.debug(f"Error: {err}")
        device_state = "Unavailable"
        return False, device_state


# Retrieve site ID
def get_site_id(authentication_token=None, dnac_api_headers=None, site_name=None):
    """
    This function retrieves site id based on site name

    :param authentication_token: (str) Authentication token
    :param dnac_api_headers: (dict) DNAC api headers
    :param site_name: (str) Site name with full hierarchy
    :return: (str) site ID from DNAC
    """

    if dnac_api_headers is None:
        dnac_api_headers = get_headers(auth_token=authentication_token)
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
    This function retrieves site id based on site name

    :param authentication_token: (str) Authentication token
    :param dnac_api_headers: (dict) DNAC api headers
    :param image_name: (str) Full image name with extension
    :return: (str) Image ID from DNAC
    """

    if dnac_api_headers is None:
        dnac_api_headers = get_headers(auth_token=authentication_token)
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


def get_template_id(
    dnac_auth_token=None, api_headers=None, config_data=None, show_all=False
):
    """
    This function retrieves configuration ID by template name

    :param dnac_auth_token: (str) DNA center authentication token
    :param api_headers: (dict) DNA Center API headers
    :param config_data: (dict) data <- CSV or CLI input
    :param show_all: (boolean) To show whole list or not
    :return: (string) Config ID (Config ID==Template ID) from DNA Center
    """

    logging.debug(f"Retrieving config ID by template name")
    template_name = config_data["deviceInfo"]["template_name"]
    if api_headers is None:
        api_headers = get_headers(auth_token=dnac_auth_token)
    method, api_url, parameters = generate_api_url(api_type="get-template-id")
    if not show_all:
        parameters["name"] = template_name
    response_status, response_body = get_response(
        method=method, endpoint_url=api_url, headers=api_headers, parameters=parameters
    )
    if response_status:
        try:
            if not show_all:
                config_id = response_body[0]["templateId"]
                logging.debug(f"Config ID received from template editor: [{config_id}]")
                return config_id
            else:
                print(
                    "\n".join(
                        sorted(
                            [
                                "  {0}/{1}".format(
                                    project["projectName"], project["name"]
                                )
                                for project in response_body
                            ]
                        )
                    )
                )
        except IndexError:
            click.secho(f"[x] Index error! Template [{template_name}] might not exists")
            return False
    else:
        return False


def get_template_parameters(dnac_auth_token=None, api_headers=None, config_id=None):
    """
    This function retrieves parameters from the specified templates

    :param dnac_auth_token: (str) DNA center authentication token
    :param api_headers: (dict) DNA Center API headers
    :param config_id: (str) Template id/config ID (templateId==configId)
    :return: (list) Template parameters
    """

    click.secho(
        f"[$] Retrieving template parameters for template ID [{config_id}]", fg="blue"
    )
    if api_headers is None:
        api_headers = get_headers(auth_token=dnac_auth_token)
    method, r_api_url, parameters = generate_api_url(api_type="get-template-parameters")
    api_url = f"{r_api_url}{config_id}"
    response_status, response_body = get_response(
        method=method, endpoint_url=api_url, headers=api_headers
    )
    if response_status:
        template_parameters = []
        try:
            template_parameters_detailed = response_body["templateParams"]
            for item in template_parameters_detailed:
                template_parameters.append(item["parameterName"])
            logging.debug(
                f"Parameters received from template " f"editor: {template_parameters}"
            )
            return template_parameters
        except Exception as err:
            click.secho(f"[x] Exception! Error: {err}")
            return template_parameters
    else:
        template_parameters = []
        logging.debug(f"Parameters received for template editor: {template_parameters}")
        return template_parameters
