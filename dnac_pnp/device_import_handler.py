#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Main module for dnac-pnp"""

# Import builtin python libraries
import json
import logging
import sys

# Import external python libraries
import click
from tqdm import tqdm

# Import custom (local) python packages
from .api_call_handler import call_api_endpoint, get_response
from .api_endpoint_handler import generate_api_url
from .dnac_token_generator import generate_token
from .dnac_params import max_col_length
from .device_claim_handler import claim
from .dnac_info_butler import (
    get_device_id,
    get_site_id,
    get_template_id,
    get_template_parameters,
)
from .header_handler import get_headers
from .utils import divider, goodbye, parse_csv

# Source code meta data
__author__ = "Dalwar Hossain"
__email__ = "dalwar.hossain@global.ntt"

# Keep track of skipped serials
skip_tracer = []


# Template parameter check
def _check_template_parameters(dnac_api_headers=None, data=None):
    """
    This private function checks day0 template parameters

    :param dnac_api_headers: (dict) DNA center api headers
    :param data: (dict) Input data, This is same as payload data / air-config
    :return: (boolean, dict) True if input is consistent, False, otherwise and data
    """

    # Template variable validation
    # Template ID == Config ID
    template_name = data["deviceInfo"]["template_name"]
    input_parameters = data["deviceInfo"].keys()
    config_id = get_template_id(api_headers=dnac_api_headers, config_data=data)
    if config_id:
        logging.debug(f"[#] Configuration ID received!")
        data["deviceInfo"]["configId"] = config_id
        logging.debug(f"Configuration ID: [{config_id}]")
        _, template_parameters = get_template_parameters(
            api_headers=dnac_api_headers, config_id=config_id
        )
        if template_parameters:
            logging.debug(f"[#] Template parameters received!")
            logging.debug(
                f"[$] Validating input parameters against "
                f"DNA center template parameters....."
            )
            logging.debug(f"[$] Parsing parameters.....")
            config_parameters = []
            for item in template_parameters:
                try:
                    conf_dict = {"key": item, "value": data["deviceInfo"][item]}
                    config_parameters.append(conf_dict)
                except KeyError as err:
                    click.secho(f"[x] Key error!", fg="red")
                    click.secho(f"[x] ERROR: Check parameter [{err}]", fg="red")
            data["deviceInfo"]["configParameters"] = config_parameters
            logging.debug(f"Data with config parameters: {data}")
            logging.debug(f"Parameter from DNA center: {template_parameters}")
            logging.debug(f"Input parameters: {input_parameters}")
            logging.debug(f"Input data: {json.dumps(data, indent=4)}")
            template_parameter_status = all(
                item in input_parameters for item in template_parameters
            )
        else:
            logging.debug(f"[x] Template parameters not found!")
            template_parameter_status = False
    else:
        logging.debug(f"[x] Template Name [{template_name}] is not present")
        template_parameter_status = False

    return template_parameter_status, data


# Site name check
def _check_device(headers=None, data=None):
    """
    This private function checks the site name validity

    :param headers: (dict) DNAC api headers
    :param data: (dict) This is same as payload data / air-config
    :return: (boolean, dict) Site status and data
    """

    device_serial_number = data["deviceInfo"]["serialNumber"]
    device_id, device_state, _ = get_device_id(
        dnac_api_headers=headers, serial_number=device_serial_number, dnac_tab="pnp"
    )
    if device_id:
        logging.debug(f"Device ID: {device_id}")
        device_status = True
        data["deviceInfo"]["deviceId"] = device_id
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

    dnac_site_name = data["deviceInfo"]["siteName"]
    site_id = get_site_id(dnac_api_headers=headers, site_name=dnac_site_name)
    if site_id:
        logging.debug(f"Site ID: {site_id}")
        site_status = True
        data["deviceInfo"]["siteId"] = site_id
    else:
        logging.debug(f"Site not found!")
        site_status = False
    return site_status, data


# Add a device
def add_device(dnac_api_headers=None, payload_data=None):
    """
    This function adds a device

    :param dnac_api_headers: (dict) API headers
    :param payload_data: (dict) Payload data for adding a device
    :return: (obj) Requests response object
    """
    # ========================== Add device to PnP list ================================
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
    logging.debug(
        f"[*] Starting CLAIM process for serial [{device_serial_number}]....."
    )
    device_id, _, _ = get_device_id(
        serial_number=device_serial_number,
        dnac_api_headers=dnac_api_headers,
        dnac_tab="pnp",
    )
    logging.debug(f"DeviceID: {device_id}")
    if device_id:
        claim_status = claim(
            headers=dnac_api_headers, device_id=device_id, data=payload_data
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
    :return: (stdout) On screen output
    """

    # ========================== Check device state ====================================
    non_claimable_states = ["Planned", "Onboarding", "Provisioned"]
    ready_to_add = False
    ready_to_claim = False
    serial_number = data["deviceInfo"]["serialNumber"]
    device_attached, device_state, data = _check_device(headers=api_headers, data=data)
    logging.debug(
        f"Device attached?: {device_attached}, State: {device_state}, Data={data}"
    )
    if device_attached:
        if device_state == "Unclaimed":
            ready_to_claim = True
        elif device_state in non_claimable_states:
            logging.debug(f"[!] Warning: Skipping [{serial_number}].....")
            logging.debug(
                f"[!] Reason: Device [{serial_number}] State: [{device_state}]"
            )
            skip_tracer.append(serial_number)
    else:
        ready_to_add = True
    # ========================== Add device ============================================
    if ready_to_add:
        api_response = add_device(dnac_api_headers=api_headers, payload_data=data)
        response_status, response_body = get_response(response=api_response)
        if response_status and response_body["successList"]:
            ready_to_claim = True
        else:
            click.secho(
                f"[x] Server responded with status code [{api_response.status_code}] "
                f"but with a FAILED response",
                fg="red",
            )
            err_msg = response_body["failureList"][0]["msg"]
            err_serial = response_body["failureList"][0]["serialNum"]
            click.secho(
                f"[x] Error: [{err_msg}], Serial Number: [{err_serial}]", fg="red"
            )
            sys.exit(1)
    # ======================== Claim device ============================================
    if ready_to_claim:
        claim_status = claim_device(dnac_api_headers=api_headers, payload_data=data)
        if not claim_status:
            click.secho(f"[x] Claim status: {claim_status}", fg="red")


# Single device import
def import_single_device(configs=None, data=None):
    """
    This module imports single device into dnac

    :param configs: (dict) DNAC configurations
    :param data: (dict) API body data
    :returns: (stdout) output to the screen
    """

    token = generate_token(configs=configs)
    headers = get_headers(auth_token=token)
    site_name = data["deviceInfo"]["siteName"]
    serial_number = data["deviceInfo"]["serialNumber"]
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
        token = generate_token(configs=configs)
        headers = get_headers(auth_token=token)
        divider("Device Management")
        click.secho(
            f"[*] Starting device management (add + claim) engine.....", fg="cyan"
        )
        for index, row in enumerate(
            tqdm(
                csv_rows,
                ascii=True,
                ncols=max_col_length,
                unit="device",
                desc="[*] Device claim progress",
            )
        ):
            air_config = {"deviceInfo": row}
            logging.debug(json.dumps(air_config, indent=4, sort_keys=True))
            # Site Validation
            site_status, data = _check_site_name(headers=headers, data=air_config)
            site_name = data["deviceInfo"]["siteName"]
            serial_number = data["deviceInfo"]["serialNumber"]
            if site_status:
                template_parameter_status, mod_data = _check_template_parameters(
                    dnac_api_headers=headers, data=air_config
                )
                if template_parameter_status:
                    acclaim_device(api_headers=headers, data=mod_data)
                else:
                    logging.debug(f"[x] Parameter mismatch!")
                    skip_tracer.append(serial_number)
            else:
                logging.debug(f"[x] Site name [{site_name}] is not valid!")
                logging.debug(f"[!] Warning: Skipping [{serial_number}].....")
                skip_tracer.append(serial_number)
        goodbye(before=True, data=skip_tracer)
