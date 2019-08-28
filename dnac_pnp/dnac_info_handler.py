#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Information handler functions"""

# Import builtin python libraries
import json
import logging
import sys

# Import external python libraries
import click
from tabulate import tabulate

# Import custom (local) python packages
from .dnac_info_butler import get_template_id, get_template_parameters, get_device_id
from .dnac_token_generator import generate_token
from .header_handler import get_headers
from .utils import divider, goodbye

# Source code meta data
__author__ = "Dalwar Hossain"
__email__ = "dalwar.hossain@dimensiondata.com"


# Show template body and the parameters
def show_template_info(dnac_configs=None, template_name=None, show_all=False):
    """
    This function shows details about template(s)

    :param dnac_configs: (dict) DNA Center username/password configurations
    :param template_name: (str) Name of the template
    :param show_all: (boolean) List all or show details of one
    :return: (stdOut) On screen output
    """

    token = generate_token(configs=dnac_configs)
    headers = get_headers(auth_token=token)

    divider("Template(s)")
    template_id = get_template_id(
        api_headers=headers, show_all=show_all, template=template_name
    )
    if not show_all:
        if template_id is not None:
            template_content, template_parameters = get_template_parameters(
                api_headers=headers, config_id=template_id
            )
            if template_content and template_parameters:
                click.secho(f"[$] Template Body:", fg="blue")
                print(template_content)
                click.secho(f"[$] Template Parameters:", fg="blue")
                print(template_parameters)
            else:
                click.secho(
                    f"[x] Could not retrieve parameters! Use --debug to get "
                    f"more information",
                    fg="red",
                )
        else:
            click.secho("[x] No template found!", fg="red")
            click.secho(
                f"[*] Make sure that the spelling is correct and has "
                f"[project_name/template_name] syntax",
                fg="blue",
            )
    else:
        if template_id:
            logging.debug(f"Found template: [{template_id}]")
    goodbye()


# Show device information from DNA Center PnP
def show_pnp_device_info(dnac_configs=None, device_serial=None, show_all=False):
    """
    This function shows details about device(s)

    :param dnac_configs: (dict) DNA Center username/password configurations
    :param device_serial: (str) Name of the template
    :param show_all: (boolean) List all or show details of one
    :return: (stdOut) On screen output
    """

    token = generate_token(configs=dnac_configs)
    headers = get_headers(auth_token=token)

    divider("Device(s)")
    device_id, device_status, device_extra = get_device_id(
        dnac_api_headers=headers,
        serial_number=device_serial,
        dnac_tab="pnp",
        show_all=show_all,
    )
    if device_id:
        if not show_all:
            logging.debug(f"Showing single device information")
            click.secho(f"[$] Device information for [{device_serial}]", fg="blue")
            for key, value in device_extra.items():
                click.secho(f"{key}: ", fg="cyan", nl=False)
                click.secho(f"{value}", fg="yellow")
        else:
            logging.debug(f"Showing all devices!")
            click.secho(f"[$] All available devices in PnP", fg="blue")
            table_rows = []
            for index, item in enumerate(device_extra):
                table_header = list(item.keys())
                table_rows.append(list(item.values()))
            print(tabulate(table_rows, table_header, tablefmt='grid'))
    goodbye()
