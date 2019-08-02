#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Main module for dnac-pnp"""

# Import builtin python libraries
import sys
import logging

# Import external python libraries
import click
from colorama import init, Fore

# Import custom (local) python libraries
from dnac_pnp._validators import (
    show_info,
    validate_alphanumeric,
    validate_file_extension,
)
from dnac_pnp.dnac_handler import import_manager

# Source code meta data
__author__ = "Dalwar Hossain"
__email__ = "dalwar.hossain@dimensiondata.com"

# Initialize text coloring
init(autoreset=True)


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
def mission_control(debug):
    """ Application mission control module"""
    if debug:
        try:
            from http.client import HTTPConnection
        except ImportError:
            print(Fore.RED + f"[x] Can't import http client")
            sys.exit(1)
        print(Fore.YELLOW + f"[+] DEBUG MODE IS ON")
        debug_format = Fore.YELLOW + f"[+] %(levelname)s %(asctime)-15s %(message)s"
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
def acclaim_one(serial_number, product_id, site_name, host_name):
    if host_name is None:
        host_name = serial_number
    air_config = {
        "serial_number": serial_number,
        "product_id": product_id,
        "site_name": site_name,
        "host_name": host_name,
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
# Add multiple devices
def acclaim_in_bulk(catalog_file):
    """Add and claim multiple devices"""

    print(catalog_file)


@mission_control.command(short_help="Shows package information.")
# Information about this package
def info():
    """This module prints information about the package"""

    show_info()
