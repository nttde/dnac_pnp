#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Site handler functions"""

# Import builtin python libraries
import json
import logging
import sys

# import external python libraries
import click
from yaml import load
import yaml

# Import custom (local) python packages
from .api_call_handler import call_api_endpoint, get_response
from .api_endpoint_handler import generate_api_url
from .dnac_params import area_essentials, building_essentials, floor_essentials
from .dnac_token_generator import generate_token
from .header_handler import get_headers
from .utils import divider, goodbye

# Source code meta data
__author__ = "Dalwar Hossain"
__email__ = "dalwar.hossain@global.ntt"


# Check dict keys
def _check_dict_keys(dict_to_check=None, dnac_site_type=None):
    """
    This private function checks dict keys

    :param dict_to_check: (dict) Dictionary that is being checked
    :param dnac_site_type: (str) Cisco DNA center site type (area, building, floor)
    :returns: (dict) Checked and modified dictionary
    """

    click.secho(f"[$] Checking config file keys.....", fg="blue")
    dict_status = False
    site_type_map = {
        "area": area_essentials,
        "building": building_essentials,
        "floor": floor_essentials,
    }
    try:
        for item in site_type_map[dnac_site_type]:
            if item in dict_to_check.keys():
                dict_status = True
            else:
                click.secho(
                    f"[x] [{item}] key is missing for site type: [{dnac_site_type}]!",
                    fg="red",
                )
                sys.exit(1)
    except KeyError:
        click.secho(f"[x] Essential key is missing from site configuration!", fg="red")
        sys.exit(1)
    return dict_status


# Generate site payload
def _generate_site_payload(site=None):
    """
    This private function generates site payload

    :param site: (dict) Single site config as python dict
    :returns: (dict) payload for api call
    """

    site_name = list(site.keys())[0]
    site_type = site[site_name]["type"]
    logging.debug(f"Site Name: {site_name}, Site Type: {site_type}")
    divider(text=f"Adding {site_type} [{site_name}]", char="-")

    payload = {"type": site_type}
    if site_type == "floor":
        # If any keys are not present leave it blank
        site_dict_status = _check_dict_keys(
            dict_to_check=site[site_name], dnac_site_type=site_type
        )
        if site_dict_status:
            payload["site"] = {
                "floor": {
                    key: value
                    for key, value in site[site_name].items()
                    if not key.startswith("type")
                }
            }
    elif site_type == "building":
        # If any keys are not present leave it blank
        site_dict_status = _check_dict_keys(
            dict_to_check=site[site_name], dnac_site_type=site_type
        )
        if site_dict_status:
            payload["site"] = {
                "building": {
                    key: value
                    for key, value in site[site_name].items()
                    if not key.startswith("type")
                }
            }
    elif site_type == "area":
        # If any keys are not present leave it blank
        site_dict_status = _check_dict_keys(
            dict_to_check=site[site_name], dnac_site_type=site_type
        )
        if site_dict_status:
            payload["site"] = {
                "area": {
                    "name": site[site_name]["name"],
                    "parentName": site[site_name]["parentName"],
                }
            }
    return payload


# Read sites configuration
def _read_site_configs(file_to_read=None):
    """This private function reads sites configurations file"""

    try:
        with open(file_to_read, "r") as stream:
            configs = load(stream, Loader=yaml.FullLoader)
            return configs
    except Exception as err:
        click.secho(f"[x] Sites configuration read error!", fg="red")
        click.secho(f"[x] ERROR: {err}", fg="red")
        sys.exit(1)


# Site management
def add_site(dnac_auth_configs=None, locations_file_path=None):
    """
    This function adds site(s) to DNA center

    :param dnac_auth_configs: (dict) DNA Center authentication configurations
    :param locations_file_path: (str) Full file path to the sites configuration
    :returns: (stdOut) Output on screen
    """

    # Read site configurations
    logging.debug(f"Location File: {locations_file_path}")
    site_configs = _read_site_configs(file_to_read=locations_file_path)
    logging.debug(f"Site Configurations: {json.dumps(site_configs, indent=4)}")
    if "sites" in site_configs.keys():
        sites = site_configs["sites"]
    else:
        click.secho(f"[x] Site configuration file is malformed", fg="red")
        sys.exit(1)

    # Authentication token
    token = generate_token(configs=dnac_auth_configs)
    headers = get_headers(auth_token=token)
    headers["__runsync"] = "true"
    headers["__persistbapioutput"] = "true"
    method, api_url, parameters = generate_api_url(api_type="add-site")
    divider("Adding Site(s)")
    click.secho(f"[$] Attempting to add sites.....", fg="blue")
    for item in sites:
        payload = _generate_site_payload(site=item)
        api_response = call_api_endpoint(
            method=method,
            api_url=api_url,
            data=payload,
            api_headers=headers,
            check_payload=False,
        )
        response_status, response_body = get_response(response=api_response)
        # Response header is in plain/text so try to convert it into json
        try:
            json_response_body = json.loads(response_body)
            if response_status:
                site_status = json_response_body["status"]
                if site_status:
                    site_msg = json_response_body["result"]["result"]["progress"]
                    prefix = "[#] "
                    color = "green"
                else:
                    site_msg = json_response_body["result"]["result"]
                    prefix = "[x] "
                    color = "red"
                click.secho(f"{prefix}{site_msg}", fg=color)
            else:
                click.secho(f"[x] {json_response_body['result']['result']}", fg="red")
        except Exception as err:
            click.secho(f"[x] ERROR: {err}")
            sys.exit(1)
    goodbye()
