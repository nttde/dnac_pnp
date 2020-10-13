#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Information handler functions"""

# Import builtin python libraries
from collections import OrderedDict
import csv
import logging

# Import external python libraries
import click
from tabulate import tabulate

# Import custom (local) python packages
from .dnac_info_butler import (
    get_template_id,
    get_template_parameters,
    get_device_id,
    get_full_site_list,
)
from .dnac_token_generator import generate_token
from .header_handler import get_headers
from .utils import divider, goodbye

# Source code meta data
__author__ = "Dalwar Hossain"
__email__ = "dalwar.hossain@global.ntt"


# Export into csv file
def _export_to_csv(data=None, output_file=None):
    """
    This private function exports pnp device list into csv

    :param data: (dict) Data to be exported to csv
    :param output_file: (str) Full export file location
    :return: (object) File object
    """

    csv_headers = list(data[0].keys())
    logging.debug(f"CSV Headers: {csv_headers}")
    logging.debug(f"CSV Data: {data}")

    try:
        with open(output_file, "w", newline="", encoding="utf-8") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=csv_headers)
            writer.writeheader()
            for row in data:
                writer.writerow(row)
        return True
    except IOError:
        click.secho(f"[x] IO exception happened!")
        return False


# Print output based on show_all
def _print_device_info(device_serial_number=None, show_all=None, data=None):
    """
    This private function prints device information

    :param device_serial_number: (str) Device serial number
    :param show_all: (boolean) List all or show details of one
    :param data: (dict) device information from DNAC
    :return: (stdOut) Print on screen
    """

    if not show_all:
        logging.debug(f"Showing single device information")
        click.secho(f"[$] Device information for [{device_serial_number}]", fg="blue")
        for key, value in data.items():
            click.secho(f"{key}: ", fg="cyan", nl=False)
            click.secho(f"{value}", fg="yellow")
    else:
        logging.debug(f"Showing all devices!")
        click.secho(f"[$] All available devices in PnP", fg="blue")
        table_rows = []
        for index, item in enumerate(data):
            table_header = ["No", *list(item.keys())]
            tmp_row = [index + 1, *list(item.values())]
            table_rows.append(tmp_row)
        print(tabulate(table_rows, table_header, tablefmt="psql"))


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
def show_pnp_device_info(
    dnac_configs=None, device_serial=None, show_all=False, export_path=None
):
    """
    This function shows details about device(s)

    :param dnac_configs: (dict) DNA Center username/password configurations
    :param device_serial: (str) Device serial number
    :param show_all: (boolean) List all or show details of one
    :param export_path: (str) Export file path
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
        if export_path:
            click.secho(f"[$] Trying to export PnP devices into csv.....", fg="blue")
            export_status = _export_to_csv(data=device_extra, output_file=export_path)
            if export_status:
                click.secho(f"[#] PnP device list export successful!", fg="green")
                click.secho(f"[*] Exported to[{export_path}]", fg="cyan")
            else:
                click.secho(f"[x] CSV export failed!", fg="red")
        else:
            _print_device_info(
                device_serial_number=device_serial, show_all=show_all, data=device_extra
            )
    goodbye()


def show_site_info(dnac_configs=None, show_all=True):
    """
    This function shows a list of all available sites from DNA center

    :param dnac_configs: (dict) DNA Center username/password configurations
    :param show_all: (boolean) List all or show details of one
    :return: (stdOut) On screen output
    """

    token = generate_token(configs=dnac_configs)
    headers = get_headers(auth_token=token)
    divider("Sites")
    site_dict = get_full_site_list(api_headers=headers)
    if site_dict:
        click.secho("[$] All available sites:", fg="blue")
        table_headers = ["Serial", "Site Name", "Site Type"]
        table_rows = []
        row_count = 1
        for key in sorted(site_dict.keys()):
            row = [row_count, key, site_dict[key]]
            table_rows.append(row)
            row_count += 1
        print(tabulate(table_rows, headers=table_headers, tablefmt="psql"))
    goodbye()
