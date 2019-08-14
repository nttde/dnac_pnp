#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Main module for dnac-pnp"""

# Import builtin python libraries
import json
import logging
import sys

# Import external python libraries
import click
from requests.auth import HTTPBasicAuth

# Import custom (local) python packages
from .api_call_handler import call_api_endpoint, get_response
from .api_endpoint_handler import generate_api_url
from .device_claim_handler import claim
from .dnac_info_handler import get_device_id, get_site_id
from .header_handler import get_headers
from .utils import parse_csv, divider, goodbye

# Source code meta data
__author__ = "Dalwar Hossain"
__email__ = "dalwar.hossain@dimensiondata.com"


# Site name check
def _check_device(headers=None, data=None):
    """
    This private function checks the site name validity

    :param headers: (dict) DNAC api headers
    :param data: (dict) This is same as payload data / air-config
    :return: (boolean, dict) Site status and data
    """

    device_serial_number = data['deviceInfo']['serialNumber']
    device_id, device_state = get_device_id(dnac_api_headers=headers, serial_number=device_serial_number)
    if device_id:
        logging.debug(f"Device ID: {device_id}")
        device_status = True
        data['deviceInfo']["deviceId"] = device_id
    else:
        logging.debug(f"Device not available in DNAC!")
        device_status = False
    return device_status, device_state, data


# Site name check
def _check_site_name(headers=None, data=None):
    """
    This private function checks the site name validity

    :param headers: (dict) DNAC api headers
    :param data: (dict) This is same as payload data / air-config
    :return: (boolean, dict) Site status and data
    """

    dnac_site_name = data['deviceInfo']['siteName']
    site_id = get_site_id(dnac_api_headers=headers, site_name=dnac_site_name)
    if site_id:
        logging.debug(f"Site ID: {site_id}")
        site_status = True
        data['deviceInfo']["siteId"] = site_id
    else:
        logging.debug(f"Site not found!")
        site_status = False
    return site_status, data


# Login to DNAC
def dnac_token_generator(configs=None):
    """
    This function logs into DNAC and generates authentication token

    :param configs: (dict) DNAC configurations
    :returns (str) Authentication token
    """

    dnac_username = configs["username"]
    dnac_password = configs["password"]

    headers = get_headers()
    method, api_url, parameters = generate_api_url(api_type="generate-token")
    logging.debug(f"Method: {method}, API:{api_url}, Parameters:{parameters}")
    click.secho(f"[$] Generating authentication token.....", fg="blue")
    api_response = call_api_endpoint(
        method=method,
        api_url=api_url,
        api_headers=headers,
        auth=HTTPBasicAuth(dnac_username, dnac_password),
    )
    response_status, response_body = get_response(response=api_response)
    if response_status:
        token = response_body["Token"]
    else:
        click.secho(
            f"[x] Server responded with [{api_response.status_code}] [{api_response.text}]",
            fg="red",
        )
        sys.exit(1)
    if token:
        click.secho(f"[#] Token received!", fg="green")
        return token
    else:
        click.secho(
            f"[x] Server responded with [{api_response.status_code}] [{api_response.text}]",
            fg="red",
        )
        sys.exit(1)


# Add a device
def add_device(dnac_api_headers=None, payload_data=None):
    """
    This function adds a device

    :param dnac_api_headers: (dict) API headers
    :param payload_data: (dict) Payload data for adding a device
    :return: (obj) Requests response object
    """
    # ========================== Add device to PnP list ===================================
    device_serial_number = payload_data["deviceInfo"]["serialNumber"]
    divider(f"Add [{device_serial_number}]")
    method, api_url, parameters = generate_api_url(api_type="import-device")
    logging.debug(f"Method: {method}, API:{api_url}, Parameters:{parameters}")
    api_response = call_api_endpoint(
        method=method,
        api_url=api_url,
        data=payload_data,
        api_headers=dnac_api_headers,
        parameters=parameters,
    )
    return api_response


# Claim a device
def claim_device(dnac_api_headers=None, payload_data=None):
    """
    This function claims a device

    :param dnac_api_headers: (dict) API headers
    :param payload_data: (dict) Payload data for adding a device
    :return: (obj) Requests response object
    """
    device_serial_number = payload_data["deviceInfo"]["serialNumber"]
    divider(f"Claim [{device_serial_number}]")
    click.secho(
        f"[*] Starting CLAIM process for serial [{device_serial_number}].....",
        fg="cyan",
    )
    device_id, _ = get_device_id(
        serial_number=device_serial_number, dnac_api_headers=dnac_api_headers
    )
    site_id = payload_data['deviceInfo']['siteId']
    logging.debug(f"DeviceID: {device_id}, SiteID: {site_id}")
    if device_id and site_id:
        claim_status = claim(
            headers=dnac_api_headers, device_id=device_id, site_id=site_id
        )
        return claim_status
    else:
        click.secho(f"[x] Required information still missing!")
        sys.exit(1)


# Acclaim device
def acclaim_device(api_headers=None, data=None):
    """
    This function add and claim devices based on device state

    :param api_headers: (dict) API headers
    :param data: (dict) Payload data for api calls
    :return:
    """

    # ========================== Check device state ======================================
    ready_to_add = False
    ready_to_claim = False
    serial_number = data['deviceInfo']['serialNumber']
    divider(f"Device state validation for [{serial_number}]")
    device_attached, device_state, data = _check_device(headers=api_headers, data=data)
    logging.debug(f"Device attached?: {device_attached}, Device State: {device_state}, Data={data}")
    if device_attached and device_state == "Unclaimed":
        ready_to_claim = True
    elif device_attached and device_state == "Planned":
        click.secho(f"[!] Device [{serial_number}] already claimed!", fg="yellow")
        click.secho(f"[!] Warning: Skipping [{serial_number}].....", fg="yellow")
    else:
        ready_to_add = True
    # ========================== Add device ==============================================
    if ready_to_add:
        api_response = add_device(dnac_api_headers=api_headers, payload_data=data)
        response_status, response_body = get_response(response=api_response)
        if response_status and response_body["successList"]:
            click.secho(f"[#] Device added!", fg="green")
            ready_to_claim = True
        else:
            click.secho(
                f"[x] Server responded with status code [{api_response.status_code}] but with a FAILED response",
                fg="red",
            )
            err_msg = response_body["failureList"][0]["msg"]
            err_serial = response_body["failureList"][0]["serialNum"]
            click.secho(f"[x] Error: [{err_msg}], Serial Number: [{err_serial}]", fg="red")
            sys.exit(1)
    # ======================== Claim device ==============================================
    if ready_to_claim:
        claim_status = claim_device(dnac_api_headers=api_headers, payload_data=data)
        if claim_status:
            click.secho(f"[#] DONE!", fg="green")
        else:
            click.secho(f"[X] Claim status: {claim_status}")
            sys.exit(1)


# Single device import
def import_single_device(configs=None, data=None):
    """
    This module imports single device into dnac

    :param configs: (dict) DNAC configurations
    :param data: (dict) API body data
    :returns: (stdout) output to the screen
    """

    token = dnac_token_generator(configs=configs)
    headers = get_headers(auth_token=token)
    site_name = data['deviceInfo']['siteName']
    serial_number = data['deviceInfo']['serialNumber']
    divider(f"Site [{site_name}] validation for [{serial_number}]")
    site_status, data = _check_site_name(headers=headers, data=data)
    if site_status:
        acclaim_device(api_headers=headers, data=data)
    else:
        click.secho(f"[x] Site name [{site_name}] is not valid!", fg="red")
        click.secho(f"[$] Exiting.....", fg="blue")
        sys.exit(1)
    goodbye()


# Device import in bulk
def device_import_in_bulk(configs=None, import_file=None):
    """
    This module imports devices in bulk

    :param configs: (dict) DNAc configurations
    :param import_file: (path) Full device list file path with extension
    :returns: (stdout) Output to the screen
    """

    csv_rows = parse_csv(file_to_parse=import_file)
    if csv_rows:
        token = dnac_token_generator(configs=configs)
        headers = get_headers(auth_token=token)
        skip_tracer = {}
        skipped = []
        for row in csv_rows:
            air_config = {"deviceInfo": row}
            logging.debug(json.dumps(air_config, indent=4, sort_keys=True))
            divider(f"Site [{row['siteName']}] validation for [{row['serialNumber']}]")
            site_status, data = _check_site_name(headers=headers, data=air_config)
            if site_status:
                acclaim_device(api_headers=headers, data=air_config)
            else:
                site_name = data['deviceInfo']['siteName']
                serial_number = data['deviceInfo']['serialNumber']
                click.secho(f"[x] Site name [{site_name}] is not valid!", fg="red")
                click.secho(f"[!] Warning: Skipping [{serial_number}].....", fg="yellow")
                skipped.append(serial_number)
        skip_tracer['skippedSerials'] = skipped
    goodbye(before=True, data=skip_tracer)
