#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Main module for dnac-pnp"""

# Import builtin python libraries
import sys

# Import external python libraries
import click

# Import custom (local) python packages
from .api_call_handler import call_api_endpoint, get_response
from .api_endpoint_handler import generate_api_url
from .header_handler import get_headers

# Source code meta data
__author__ = "Dalwar Hossain"
__email__ = "dalwar.hossain@global.ntt"


# Generate claim payload
def _generate_claim_payload(device_id=None, raw_payload=None, image_id=None):
    """
    This private function generates device claim payload

    :param device_id: (str) Device ID obtained form DNAC against serial number
    :param raw_payload: (dict) Input payload raw data
    :param image_id: (str) Image ID obtained form DNAC against image full name
    :return: (json) Payload for requests object
    """

    site_id = raw_payload["deviceInfo"]["siteId"]
    config_id = raw_payload["deviceInfo"]["configId"]
    config_parameters = raw_payload["deviceInfo"]["configParameters"]
    dict_payload = {
        "siteId": site_id,
        "deviceId": device_id,
        "type": "Default",
        "imageInfo": {"imageId": "", "skip": "true"},
        "configInfo": {"configId": config_id, "configParameters": config_parameters},
    }
    return dict_payload


# Claim device
def claim(auth_token=None, headers=None, device_id=None, data=None):
    """
    This function claims device according to device ID

    :param auth_token: (str) DNA center authentication token
    :param headers: (dict) API headers
    :param device_id: (str) Device ID obtained form DNAC against serial number
    :param data: (dict) payload data for api request
    :return: (object) Response object
    """

    method, api_url, parameters = generate_api_url(api_type="claim-device")
    if headers is None:
        headers = get_headers(auth_token=auth_token)
    payload = _generate_claim_payload(device_id=device_id, raw_payload=data)
    api_response = call_api_endpoint(
        method=method,
        api_url=api_url,
        data=payload,
        api_headers=headers,
        parameters=parameters,
        check_payload=False,
    )
    response_status, response_body = get_response(response=api_response)
    if response_status:
        return True
    else:
        click.secho(f"[x] Device claim failed!", fg="red")
        return False
