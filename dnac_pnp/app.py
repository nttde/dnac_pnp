#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Main module for dnac-pnp"""

# Import builtin python libraries
import logging
import sys

# Import external python libraries
import click

# Import custom (local) python libraries
from .utils import (
    debug_manager,
    initial_message,
    show_info,
    validate_file_extension,
    validate_input,
    validate_serial,
)
from .dnac_handler import import_manager, delete_manager

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
    """Mission control module"""

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
    "-h",
    "--host-name",
    "host_name",
    help="hostname of the device [if not provided, serial number will be used].",
    required=False,
    type=str,
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
def acclaim_one(context, serial_number, product_id, site_name, host_name, sub_debug):
    """This module is the entry-point for single device add and claim"""

    if context.initial_msg:
        initial_message()
    if context.debug or sub_debug:
        debug_manager()
    if host_name is None:
        click.secho(
            f"[!] Warning: No hostname provided! Serial number will be used as device name",
            fg="yellow",
        )
        host_name = serial_number
    air_config = {
        "deviceInfo": {
            "name": host_name,
            "serialNumber": serial_number,
            "pid": product_id,
            "siteName": site_name,
        }
    }
    logging.debug(f"Air Config: {air_config}")
    import_manager(inputs=air_config, import_type="single")


@mission_control.command(short_help="Add and claim multiple devices.")
@click.option(
    "-f",
    "--catalog-file",
    "catalog_file",
    help="Device catalog full file path",
    required=False,
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
    if catalog_file:
        logging.debug(f"Catalog file: {catalog_file}")
        click.secho(
            f"[!] warning: Device import catalog detected at input!", fg="yellow"
        )
        click.secho(f"[*] Device Import file location: [{catalog_file}]", fg="cyan")
        import_manager(import_type="bulk", device_catalog=catalog_file)
    else:
        import_manager(import_type="bulk")


@mission_control.command(short_help="Shows package information.")
@click.option(
    "--all",
    "all_info",
    is_flag=True,
    default=False,
    show_default=True,
    help="Shows full information.",
    type=str,
)
@click.option(
    "--author",
    "author",
    is_flag=True,
    default=False,
    show_default=True,
    help="Shows author information.",
    type=str,
    hidden=True,
)
@pass_context
# Information about this package
def info(context, all_info, author):
    """This module prints information about the package"""

    if all_info:
        show_info(view_type="more")
    else:
        show_info(view_type="less")
    if author:
        show_info(view_type="author")


@mission_control.command(short_help="Delete [un-claim + remove] or more devices.")
@click.option(
    "-s",
    "--serial-numbers",
    "serial_numbers",
    help="Comma separated serial numbers.",
    required=False,
    type=str,
)
@click.option(
    "-f",
    "--delete-from-file",
    "delete_entries",
    help="Device delete full file path.",
    required=False,
    type=click.Path(exists=True, dir_okay=False),
    callback=validate_file_extension,
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
@click.option(
    "--debug",
    "delete_debug",
    is_flag=True,
    default=False,
    show_default=True,
    help="Turns on DEBUG mode.",
    type=str,
)
@pass_context
def delete(context, serial_numbers, delete_entries, dry_run, delete_debug):
    """Delete one or multiple devices"""

    if context.initial_msg:
        initial_message()
    if context.debug or delete_debug:
        debug_manager()
    if delete_entries:
        logging.debug(f"Catalog file: {delete_entries}")
        click.secho(
            f"[!] warning: Devices will be deleted according to the serial numbers in file",
            fg="yellow",
        )
        click.secho(f"[*] File location: [{delete_entries}]", fg="cyan")
        delete_manager(delete_from_file=delete_entries, dry_run=dry_run)
    elif serial_numbers:
        delete_manager(serials=serial_numbers, dry_run=dry_run)
    else:
        click.secho(f"[x] Provide at least one option! See --help for more!", fg="red")
        sys.exit(1)
