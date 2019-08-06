#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Main module for dnac-pnp"""

# Import builtin python libraries
import logging

# Import external python libraries
import click

# Import custom (local) python libraries
from dnac_pnp._validators import (
    initial_message,
    show_info,
    validate_serial,
    validate_input,
    validate_file_extension,
    debug_manager,
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
    context.initial_msg = True
    context.dry_run = True


@mission_control.command(short_help="Add and claim a single device.")
@click.option(
    "-s",
    "--serial-number",
    "serial_number",
    help="Serial number of the device.",
    required=True,
    type=str,
    callback=validate_serial,
)
@click.option(
    "-p",
    "--product-id",
    "product_id",
    help="Product ID of the device. (e.g. Cisco2690)",
    required=True,
    type=str,
    callback=validate_input,
)
@click.option(
    "-b",
    "--site-name",
    "site_name",
    help="Site name with full hierarchy.",
    required=True,
    type=str,
)
@click.option(
    "-i",
    "--image-name",
    "image_name",
    help="Image full name with extension.",
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
@click.option(
    "-t",
    "--device-type",
    "device_type",
    help="Device type.",
    required=False,
    default="Router",
    show_default=True,
    type=str,
    callback=validate_input,
)
@click.option(
    "--debug",
    "sub_debug",
    is_flag=True,
    default=False,
    show_default=True,
    help="Turns on DEBUG mode.",
    type=str,
)
@pass_context
def acclaim_one(context, serial_number, product_id, site_name, image_name, host_name, device_type, sub_debug):
    """This module is the entry-point for single device add and claim"""

    if context.initial_msg:
        initial_message()
    if context.debug or sub_debug:
        debug_manager()
    if host_name is None:
        click.secho(
            f"[!] Warning: No hostname provided! Serial number will be used as hostname",
            fg="yellow",
        )
        host_name = serial_number
    air_config = {
        "deviceInfo": {
            "name": host_name,
            "serialNumber": serial_number,
            "deviceType": device_type,
            "pid": product_id,
            "imageName": image_name,
            "tags": {"siteName": [site_name], "rfProfile": ["TYPICAL"]},
        }
    }
    logging.debug(f"Air Config: {air_config}")
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
@click.option(
    "--debug",
    "sub_debug",
    is_flag=True,
    default=False,
    show_default=True,
    help="Turns on DEBUG mode.",
    type=str,
)
@pass_context
def acclaim_in_bulk(context, catalog_file, sub_debug):
    """Add and claim multiple devices"""

    if context.initial_msg:
        initial_message()
    if context.debug or sub_debug:
        debug_manager()
    print(catalog_file)


@mission_control.command(short_help="Shows package information.")
@pass_context
# Information about this package
def info(context):
    """This module prints information about the package"""

    show_info()


@mission_control.command(short_help="Delete [un-claim + remove] or more devices.")
@click.option(
    "-s",
    "--serial-numbers",
    "serial_numbers",
    help="Comma separated serial numbers.",
    required=True,
    type=str,
    callback=validate_serial,
)
@click.option(
    "--dry-run",
    "dry_run",
    help="Dry runs the process.",
    is_flag=True,
    default=False,
    show_default=True,
    type=str,
)
@pass_context
def delete(context, serial_numbers, dry_run):
    """Add and claim multiple devices"""

    print(serial_numbers)
