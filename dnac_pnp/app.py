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


# Show information abou the package
def show_info():
    """This module prints information about the package on screen"""

    try:
        from dnac_pnp import __package_name__ as package_name
        from dnac_pnp import __version__ as version
        from dnac_pnp import __license__ as package_license
        from dnac_pnp import __author__ as author
        from dnac_pnp import __email__ as email
    except ImportError:
        print(Fore.RED + f"[x] Can't import information")
        sys.exit(1)
    print(Fore.CYAN + f"Package Name: " + Fore.GREEN + f"{package_name}")
    print(Fore.CYAN + f"Version: " + Fore.GREEN + f"{version}")
    print(Fore.CYAN + f"License: " + Fore.GREEN + f"{package_license}")
    print(Fore.CYAN + f"Author: " + Fore.GREEN + f"{author}")
    print(Fore.CYAN + f"Contact: " + Fore.GREEN + f"{email}")


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


@mission_control.command(short_help="Shows package information.")
# Information about this package
def info():
    """This module prints informaion about the package"""

    show_info()
