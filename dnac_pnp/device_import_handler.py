#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Main module for dnac-pnp"""

# Import builtin python libraries
from collections import OrderedDict
import csv
import json
import sys
import logging

# Import external python libraries
import click
import urllib3
from requests.auth import HTTPBasicAuth

# Import custom (local) python packages
from dnac_pnp.api_endpoint_handler import generate_api_url
from dnac_pnp.header_handler import get_headers
from dnac_pnp.api_call_handler import call_api_endpoint
from dnac_pnp.api_response_handler import handle_response
from dnac_pnp.dnac_info_handler import get_device_id, get_site_id
from dnac_pnp.device_claim_handler import claim
from dnac_pnp._validators import check_csv_header, check_csv_cell_name, divider, goodbye

# Source code meta data
__author__ = "Dalwar Hossain"
__email__ = "dalwar.hossain@dimensiondata.com"


# Disable SSL warning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# Login to DNAC
def dnac_token_generator(configs=None):
    """
    This function logs into DNAC

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
    response_status, response_body = handle_response(response=api_response)
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
def add_device(dnac_configs=None, dnac_api_headers=None, payload_data=None):
    """
    This function adds a device

    :param dnac_configs: (dict) Configurations for DNAC
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
    site_name = payload_data["deviceInfo"]["siteName"]
    divider(f"Claim [{device_serial_number}]")
    click.secho(
        f"[*] Starting CLAIM process for serial [{device_serial_number}].....",
        fg="cyan",
    )
    device_id = get_device_id(serial_number=device_serial_number, dnac_api_headers=dnac_api_headers)
    site_id = get_site_id(dnac_api_headers=dnac_api_headers, site_name=site_name)
    logging.debug(f"DeviceID: {device_id}, SiteID: {site_id}")
    if device_id and site_id:
        claim_status = claim(
            headers=dnac_api_headers,
            device_id=device_id,
            site_id=site_id,
        )
        return claim_status
    else:
        click.secho(f"[x] Required information still missing!")
        sys.exit(1)


# Single device import
def import_single_device(configs=None, data=None):
    """
    This module imports single device into dnac

    :param configs: (dict) DNAC configurations
    :param data: (dict) API body data
    :returns: (stdout) output to the screen
    """

    # ========================== Add device ==============================================
    token = dnac_token_generator(configs=configs)
    api_headers = get_headers(auth_token=token)
    api_response = add_device(dnac_configs=configs, dnac_api_headers=api_headers, payload_data=data)
    response_status, response_body = handle_response(response=api_response)
    # ======================== Claim device ==============================================
    if response_status and response_body["successList"]:
        click.secho(f"[#] Device added!", fg="green")
        claim_status = claim_device(dnac_api_headers=api_headers, payload_data=data)
        if claim_status:
            goodbye()
        else:
            click.secho(f"[X] Claim status: {claim_status}")
            sys.exit(1)
    else:
        click.secho(
            f"[x] Server responded with status code [{api_response.status_code}] but with a FAILED response",
            fg="red",
        )
        err_msg = response_body["failureList"][0]["msg"]
        err_serial = response_body["failureList"][0]["serialNum"]
        click.secho(f"[x] Error: [{err_msg}], Serial Number: [{err_serial}]", fg="red")
        sys.exit(1)


# Device import in bulk
def device_import_in_bulk(configs=None, import_file=None):
    """
    This module imports devices in bulk

    :param configs: (dict) DNAc configurations
    :param import_file: (path) Full device list file path with extension
    :returns: (stdout) Output to the screen
    """

    # ============================ Parse CSV ============================================
    logging.debug(f"Reading csv from [{import_file}]")
    click.secho(f"[$] Reading CSV file.....", fg="blue")
    csv_rows = []
    with open(import_file) as csv_import_file:
        reader = csv.DictReader(csv_import_file)
        r_title = [item.strip() for item in reader.fieldnames]
        logging.debug(f"CSV file headers: {r_title}")
        title = check_csv_header(file_headers=r_title)
        for r_row in reader:
            logging.debug(f"Raw input row from file: {r_row}")
            try:
                row = OrderedDict(
                    [(check_csv_cell_name(key.strip()), value.strip()) for key, value in r_row.items()]
                )
            except AttributeError:
                logging.debug(f"AttributeError: An attribute error has occurred!")
                logging.debug(f"Skipping row: {r_row}")
                continue
            logging.debug(f"Stripped row: {row}")
            csv_rows.extend([{title[i]: row[title[i]] for i in range(len(title))}])
    click.secho(f"[#] Primary input check successful!", fg="green")
    # ========================== Execute add + claim ============================================
    for row in csv_rows:
        air_config = {"deviceInfo": row}
        logging.debug(json.dumps(air_config, indent=4, sort_keys=True))
