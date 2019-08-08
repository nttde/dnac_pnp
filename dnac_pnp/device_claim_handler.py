#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Main module for dnac-pnp"""

# Import builtin python libraries
import sys

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


# Generate claim payload
def _generate_claim_payload(device_id=None, site_id=None, image_id=None):
    """
    This private function generates device claim payload

    :param device_id: (str) Device ID obtained form DNAC against serial number
    :param site_id: (str) Site ID obtained form DNAC against site name
    :param image_id: (str) Image ID obtained form DNAC against image full name
    :return: (json) Payload for requests object
    """

    dict_payload = {
        "siteId": site_id,
        "deviceId": device_id,
        "type": "Default",
        "imageInfo": {"imageId": "", "skip": False},
        "configInfo": {},
    }

    return dict_payload


# Claim device
def claim(auth_token=None, headers=None, device_id=None, site_id=None):
    """
    This function claims device according to device ID

    :param auth_token: (str) DNA center authentication token
    :param headers: (dict) API headers
    :param device_id: (str) Device ID obtained form DNAC against serial number
    :param site_id: (str) Site ID obtained form DNAC against site name
    :return: (object) Response object
    """

    method, api_url, parameters = generate_api_url(api_type="claim-device")
    if headers is None:
        headers = get_headers(auth_token=auth_token)
    payload = _generate_claim_payload(device_id=device_id, site_id=site_id)
    api_response = call_api_endpoint(
        method=method,
        api_url=api_url,
        data=payload,
        api_headers=headers,
        parameters=parameters,
        check_payload=False,
    )
    response_status = handle_response(response=api_response)
    if response_status:
        click.secho(f"[#] Device claimed!", fg="green")
        return True
    else:
        click.secho(f"[x] Device claim failed!")
        sys.exit(1)
