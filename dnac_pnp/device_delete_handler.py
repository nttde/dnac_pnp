#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Device delete module for dnac-pnp"""

# Import builtin python libraries
import logging

# Import external python libraries
import click
from tqdm import tqdm
import urllib3

# Import custom (local) python packages
from .api_call_handler import call_api_endpoint
from .api_endpoint_handler import generate_api_url
from .api_call_handler import get_response
from .dnac_token_generator import generate_token
from .dnac_info_butler import get_device_id
from .dnac_params import max_col_length
from .header_handler import get_headers
from .utils import divider, goodbye

# Source code meta data
__author__ = "Dalwar Hossain"
__email__ = "dalwar.hossain@global.ntt"


# Disable SSL warning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# Remove device
def delete_device(api_headers=None, device_serial=None):
    """
    This function deletes device from DNA center

    :param api_headers: (dict) API headers
    :param device_serial: (str) Device serial number
    :return: (obj) Response object
    """

    pnp_device_states = ["Unclaimed", "Planned", "Error"]
    inventory_device_states = ["Onboarding", "Provisioned"]
    device_id, device_state, _ = get_device_id(
        dnac_api_headers=api_headers, serial_number=device_serial, dnac_tab="pnp"
    )
    logging.debug(f"Delete device ID: {device_id} in state: {device_state}")
    if device_id:
        logging.debug(f"[#] Device ID received!")
        logging.debug(f"[#] Device current state: [{device_state}]")
        if device_state in pnp_device_states:
            dnac_api_type = "remove-device-pnp"
        elif device_state in inventory_device_states:
            inv_device_id, device_state, _ = get_device_id(
                dnac_api_headers=api_headers,
                serial_number=device_serial,
                dnac_tab="inventory",
            )
            if inv_device_id:
                device_id = inv_device_id
            dnac_api_type = "remove-device-inventory"
        else:
            dnac_api_type = "remove-device-pnp"
        method, api_url, parameters = generate_api_url(api_type=dnac_api_type)
        logging.debug(f"Method: {method}, API:{api_url}, Parameters:{parameters}")
        delete_api_url = f"{api_url}{device_id}"
        api_response = call_api_endpoint(
            method=method,
            api_url=delete_api_url,
            api_headers=api_headers,
            parameters=parameters,
        )
        return api_response
    else:
        logging.debug(f"[!]Device ID not found. SKIPPING serial [{device_serial}].....")
        return False


# Delete device(s)
def remove_devices(configs=None, serials=None):
    """
    This function invokes device deletion form DNAC by serial number

    :param configs: (dict) DNAC configurations
    :param serials: (list) Serial numbers of the device to delete
    :returns: (obj) Returns response object from server
    """

    if serials:
        token = generate_token(configs=configs)
        headers = get_headers(auth_token=token)
        divider("Deleting devices")
        click.secho(f"[*] Starting device deletion engine.....", fg="cyan")
        skipped_serial = []
        for index, serial in enumerate(
            tqdm(
                serials, ascii=True, ncols=max_col_length, desc="[*] Deletion progress", unit="devices"
            )
        ):
            api_response = delete_device(api_headers=headers, device_serial=serial)
            logging.debug(f"API Response: {api_response}")
            if api_response:
                response_status, _ = get_response(response=api_response)
                if not response_status:
                    click.secho(f"[x] Device [{serial}] not removed!", fg="red")
                    logging.debug(f"[{serial}] not removed!")
                    continue
            else:
                skipped_serial.append(serial)
        goodbye(before=True, data=skipped_serial)
