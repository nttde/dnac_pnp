#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Template handler module"""

# Import builtin python libraries
import logging

# Import external python libraries
import click

# Import custom (local) python packages
from .api_call_handler import call_api_endpoint, get_response
from .api_endpoint_handler import generate_api_url
from .header_handler import get_headers

# Source code meta data
__author__ = "Dalwar Hossain"
__email__ = "dalwar.hossain@dimensiondata.com"


def get_template_id(dnac_auth_token=None, api_headers=None, config_data=None):
    """
    This function retrieves configuration ID by template name

    :param dnac_auth_token: (str) DNA center authentication token
    :param api_headers: (dict) DNA Center API headers
    :param config_data: (dict) data <- CSV or CLI input
    :return: (string) Config ID (Config ID==Template ID) from DNA Center
    """

    logging.debug(f"Retrieving config ID by template name")
    template_name = config_data["deviceInfo"]["template_name"]
    if api_headers is None:
        api_headers = get_headers(auth_token=dnac_auth_token)
    method, api_url, parameters = generate_api_url(api_type="get-template-id")
    parameters["name"] = template_name
    api_response = call_api_endpoint(
        method=method, api_url=api_url, api_headers=api_headers, parameters=parameters
    )
    response_status, response_body = get_response(response=api_response)
    if response_status:
        try:
            config_id = response_body[0]["templateId"]
            logging.debug(f"Config ID received from template editor: [{config_id}]")
            return config_id
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
    api_response = call_api_endpoint(
        method=method, api_url=api_url, api_headers=api_headers
    )
    response_status, response_body = get_response(response=api_response)
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
