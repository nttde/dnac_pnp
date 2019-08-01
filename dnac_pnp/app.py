#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Main module for dnac-pnp"""

# Import builtin python libraries
import sys

# Import external python libraries
import click
from colorama import init, Fore

# Import custom (local) python libraries
from dnac_pnp.dnac_handler import import_manager

# Source code meta data
__author__ = "Dalwar Hossain"
__email__ = "dalwar.hossain@dimensiondata.com"

# Initialize text coloring
init(autoreset=True)


# Validate input serial number
def validate_alphanumeric(ctx, param, value):
    """This function validates and allows only letters and numbers"""

    if not value.isalnum():
        print(Fore.RED + "[x] Invalid input!")
        ctx.abort()
    else:
        return value


# Validate file extension
def validate_file_extension(ctx, param, value):
    """This function validates file extensions"""
    allowed_extensions = ["csv"]
    if value.rsplit(".", 1)[1] not in allowed_extensions:
        print(Fore.RED + "[x] Provided file extension not allowed!")
        ctx.abort()
    else:
        return value


@click.group()
@click.version_option()
def mission_control():
    """ Application mission control module"""
    pass


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
    print(air_config)
    # import_manager(inputs=air_config, import_type="single")


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
    pass


if __name__ == "__main__":
    mission_control()
