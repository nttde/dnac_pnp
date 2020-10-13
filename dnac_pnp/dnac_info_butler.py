#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Information butler functions"""

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
from .dnac_params import device_extra_param, device_extra_param_less, pnp_device_limit

# Source code meta data
__author__ = "Dalwar Hossain"
__email__ = "dalwar.hossain@global.ntt"


# Retrieve device ID
def get_device_id(
    authentication_token=None,
    dnac_api_headers=None,
    serial_number=None,
    dnac_tab=None,
    show_all=False,
):
    """
    This function retrieves the device id by serial number

    :param authentication_token: (str) Authentication token
    :param dnac_api_headers: (dict) API headers
    :param serial_number: (str) Device serial number
    :param dnac_tab: (str) Where to look for the device info (PnP or Inventory)
    :param show_all: (boolean) To show whole list or not
    :returns: (str) device ID from DNA center
    """

    logging.debug(f"TAB: {dnac_tab}")
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
    if dnac_tab == "pnp" and show_all:
        parameters["limit"] = get_pnp_device_count(api_headers=dnac_api_headers)
    _, response_body = get_response(
        headers=dnac_api_headers,
        authentication_token=authentication_token,
        method=method,
        endpoint_url=api_url,
        parameters=parameters,
    )
    try:
        if not show_all:
            logging.debug(f"dnac tab: {dnac_tab}")
            if dnac_tab == "pnp":
                device_id = response_body[0]["id"]
                device_state = response_body[0]["deviceInfo"]["state"]
                logging.debug(f"Device ID: {device_id}")
                if device_state.casefold() == "Provisioned".casefold():
                    ext_param = device_extra_param
                else:
                    ext_param = device_extra_param_less
                device_extra = {}
                for item in ext_param:
                    device_extra[item] = response_body[0]["deviceInfo"][item]
            elif dnac_tab == "inventory":
                device_id = response_body["response"][0]["id"]
                device_state = response_body["response"][0]["collectionStatus"]
                logging.debug(f"Device ID: {device_id}")
                device_extra = {}
            else:
                device_id = False
                device_state = "Unknown"
                device_extra = {}
            return device_id, device_state, device_extra
        else:
            if dnac_tab == "pnp":
                available_devices = []
                for item in response_body:
                    device_extra = {}
                    for param in device_extra_param_less:
                        device_extra[param] = item["deviceInfo"][param]
                    available_devices.append(device_extra)
                return True, True, available_devices
            else:
                available_devices = []
                return False, False, available_devices

    except KeyError as err:
        click.secho(f"[x] Key not found in the response!", fg="red")
        logging.debug(f"Error: {err}")
        sys.exit(1)
    except IndexError as err:
        logging.debug(f"[!] Index error! " f"Device might not be available in PnP")
        logging.debug(f"Error: {err}")
        device_state = "Unavailable"
        device_extra = {}
        return False, device_state, device_extra


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
        if response_json:
            site_id = response_json["response"][0]["id"]
            logging.debug(f"Site ID: {site_id}")
            return site_id
        else:
            err_msg = response_json["message"][0]
            logging.debug(f"[*] Message: {err_msg}")
            return False
    except KeyError as err:
        logging.debug(f"[x] {err} Key not found in the response!")
        logging.debug(f"Error: {err}")
        return False
    except IndexError as err:
        logging.debug(f"[x] {err} The input site is not valid or site is not present")
        logging.debug(f"Error: {err}")
        return False


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
    dnac_auth_token=None,
    api_headers=None,
    config_data=None,
    show_all=False,
    template=None,
):
    """
    This function retrieves configuration ID by template name

    :param dnac_auth_token: (str) DNA center authentication token
    :param api_headers: (dict) DNA Center API headers
    :param config_data: (dict) data <- CSV or CLI input
    :param show_all: (boolean) To show whole list or not
    :param template: (str) Template name
    :return: (string) Config ID (Config ID==Template ID) from DNA Center
    """

    logging.debug(f"Retrieving config ID by template name")
    if config_data:
        template_name = config_data["deviceInfo"]["template_name"]
    else:
        template_name = template
    logging.debug(f"Template Name: {template_name}")
    if api_headers is None:
        api_headers = get_headers(auth_token=dnac_auth_token)
    method, api_url, parameters = generate_api_url(api_type="get-template-id")
    response_status, response_body = get_response(
        method=method, endpoint_url=api_url, headers=api_headers, parameters=parameters
    )
    if response_status:
        try:
            if not show_all:
                max_version = 0
                for template in response_body:
                    project_name, project_template_name = template_name.split("/")
                    if (
                        template["projectName"] == project_name
                        and template["name"] == project_template_name
                    ):
                        for template_version in template["versionsInfo"]:
                            if int(template_version["version"]) > max_version:
                                max_version = int(template_version["version"])
                                template_id = template_version["id"]
                                logging.debug(
                                    f"Template ID received from template editor: "
                                    f"[{template_id}]"
                                )
                        logging.debug(f"ID:{template_id}, Version: {max_version}")
                        return template_id
            else:
                click.secho(f"[$] Available templates:", fg="blue")
                for index, template in enumerate(response_body):
                    print(f"{index+1}. {template['projectName']}/{template['name']}")
                return True
        except IndexError:
            click.secho(f"[x] Index error! Template [{template_name}] might not exists")
            return False
    else:
        return False


def get_template_parameters(dnac_auth_token=None, api_headers=None, config_id=None):
    """
    This function retrieves parameters from the specified templates

    :param dnac_auth_token: (str) DNA center authentication token
    :param api_headers: (dict) DNA center API headers
    :param config_id: (str) Template id/config ID (templateId==configId)
    :return: (str, list) Template content, Template parameters
    """

    logging.debug(f"[$] Template ID [{config_id}]")
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
            template_content = response_body["templateContent"]
            for item in template_parameters_detailed:
                template_parameters.append(item["parameterName"])
            logging.debug(
                f"Parameters received from template " f"editor: {template_parameters}"
            )
            return template_content, template_parameters
        except Exception as err:
            click.secho(f"[x] Exception! Error: {err}")
            return False, template_parameters
    else:
        template_parameters = []
        logging.debug(f"Parameters received for template editor: {template_parameters}")
        return False, template_parameters


# Get PnP device count
def get_pnp_device_count(dnac_auth_token=None, api_headers=None):
    """
    This function gets pnp device count and returns the number

    :param dnac_auth_token: (str) DNA center authentication string
    :param api_headers: (dict) DNA center API headers
    :return: (int) Total number of pnp devices available in DNA center
    """

    logging.debug(f"Getting dna center pnp device count!")
    if api_headers is None:
        api_headers = get_headers(auth_token=dnac_auth_token)
    method, api_url, parameters = generate_api_url(api_type="get-pnp-device-count")
    response_status, response_body = get_response(
        method=method, endpoint_url=api_url, headers=api_headers, parameters=parameters
    )
    if response_status:
        try:
            total_devices = int(response_body["response"])
            return total_devices
        except ValueError:
            return pnp_device_limit
    else:
        return pnp_device_limit


# Parse site data
def _parse_site_additional_info(sites=None):
    """
    This private function parses additional info of site response

    :param sites: (list) A list of dictionaries containing site information
    :return: (dict) Site and type
    """

    site_dict = {}
    for site in sites:
        try:
            for item in site["additionalInfo"]:
                if item["nameSpace"].casefold() == "Location".casefold():
                    site_type = item["attributes"]["type"]
        except KeyError:
            click.secho(f"[x] Key error! Error: {KeyError}")
            return False
        site_dict[site["groupNameHierarchy"]] = site_type
    logging.debug(f"Dictionary: {site_dict}")
    return site_dict


# Get full site list
def get_full_site_list(dnac_auth_token=None, api_headers=None):
    """
    This function retrieves the list of available sites and type form DNA center

    :param dnac_auth_token: (str) DNA center authentication string
    :param api_headers: (dict) DNA center API headers
    :return: (dict) a dictionary of sites and types
    """

    logging.debug(f"Getting full site list from DNA center")
    if api_headers is None:
        api_headers = get_headers(auth_token=dnac_auth_token)
    method, api_url, parameters = generate_api_url(api_type="get-all-sites")
    response_status, response_body = get_response(
        method=method, endpoint_url=api_url, headers=api_headers, parameters=parameters
    )
    if response_status:
        try:
            raw_sites = response_body["response"]
            sites_dict = _parse_site_additional_info(sites=raw_sites)
            return sites_dict
        except Exception as err:
            click.secho(f"[x] Exception! Error: [{err}]", fg="red")
            return False
