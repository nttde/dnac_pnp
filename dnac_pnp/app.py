#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Main module for dnac-pnp"""

# Import builtin python libraries
import sys
import logging

# Import external python libraries
import click
from colorama import init, Fore, Back

# Import custom (local) python libraries
from dnac_pnp._validators import (
    initial_message,
    show_info,
    validate_alphanumeric,
    validate_file_extension,
)
from dnac_pnp.dnac_handler import import_manager

# Source code meta data
__author__ = "Dalwar Hossain"
__email__ = "dalwar.hossain@dimensiondata.com"


# Click context manager class
class Context(object):
    """Click context manager class"""

    def __init__(self):
        """Constructor method for click context manager class"""

        self.debug = False
        self.initial_msg = False


pass_context = click.make_pass_decorator(Context, ensure=True)


@click.group()
@click.option(
    "--debug",
    "debug",
    is_flag=True,
    default=False,
    show_default=True,
    help="Turns on DEBUG mode.",
    type=str,
)
@click.version_option()
@pass_context
def mission_control(context, debug):
    """ Mission control module for the application"""
    context.debug = debug
    if debug:
        try:
            from http.client import HTTPConnection
        except ImportError:
            click.secho(f"[x] Can't import http client", fg="red")
            sys.exit(1)
        click.secho(f"[+] DEBUG mode is ON", fg="yellow")
        debug_format = "[+] %(levelname)s %(asctime)-15s %(message)s"
        HTTPConnection.debuglevel = 4
        logging.basicConfig(format=debug_format)
        logging.getLogger().setLevel(logging.DEBUG)
        requests_log = logging.getLogger("urllib3")
        requests_log.setLevel(logging.DEBUG)
        requests_log.propagate = True


@mission_control.command(short_help="Add and claim a single device.")
@click.option(
    "-s",
    "--serial-number",
    "serial_number",
    help="Serial number of the device.",
    required=True,
    type=str,
    callback=validate_alphanumeric,
)
@click.option(
    "-p",
    "--product-id",
    "product_id",
    help="Product ID of the device. (e.g. Cisco2690)",
    required=True,
    type=str,
    callback=validate_alphanumeric,
)
@click.option(
    "-b",
    "--site-name",
    "site_name",
    help="Site name for the device with full hierarchy.",
    required=True,
    type=str,
)
@click.option(
    "-h",
    "--host-name",
    "host_name",
    help="hostname of the device [if not provided, serial number will be used].",
    required=False,
    type=str,
)
@pass_context
def acclaim_one(context, serial_number, product_id, site_name, host_name):
    if host_name is None:
        click.secho("[^] Warning: ", nl=False, fg="yellow")
        click.secho(
            f"No hostname provided! Serial number will be used as hostname",
            fg="black",
            bg="yellow",
        )
        host_name = serial_number
    air_config = {
        "serialNumber": serial_number,
        "pid": product_id,
        "tags": {"siteName": [site_name], "rfProfile": ["TYPICAL"]},
        "hostname": host_name,
    }
    logging.info(f"Air Config: {air_config}")
    import_manager(inputs=air_config, import_type="single")


@mission_control.command(short_help="Add and claim multiple devices.")
@click.option(
    "-f",
    "--catalog-file",
    "catalog_file",
    help="Device catalog file path '.csv' format.",
    required=True,
    type=click.Path(exists=True, dir_okay=False),
    callback=validate_file_extension,
)
@pass_context
def acclaim_in_bulk(context, catalog_file):
    """Add and claim multiple devices"""

    print(catalog_file)


@mission_control.command(short_help="Shows package information.")
@pass_context
# Information about this package
def info(context):
    """This module prints information about the package"""

    show_info()
