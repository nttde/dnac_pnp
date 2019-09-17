#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Source code meta data
__author__ = "Dalwar Hossain"
__email__ = "dalwar.hossain@dimensiondata.com"

# Import builtin python libraries
import logging
import os
import sys

# import external python libraries
import click

# Import custom (local) python packages
from .utils import divider, parse_txt
from .config_handler import config_files, load_config
from .device_import_handler import device_import_in_bulk, import_single_device
from .dnac_info_handler import show_template_info, show_pnp_device_info, show_site_info
from .device_delete_handler import remove_devices

# Setting global host variable
all_configs = {}
dnac_configs = {}
host = ""


# Populate configurations
def populate_config():
    """This function loads the configurations for DNA center"""

    # Using the defined global variables
    global all_configs
    global dnac_configs
    global host

    divider("Configurations")
    if not all_configs:
        all_configs = load_config(config_files)
        dnac_configs = all_configs["dnac"]
        host = dnac_configs["host"]


# Import one or more devices
def import_manager(inputs=None, import_type=None, **kwargs):
    """
    This module manages import of the device(s)

    :param inputs: (dict) A dictionary of user provided inputs
    :param import_type: (str) device import type "single" or "bulk"
    :param kwargs: (kwargs) Key value pair
    :returns: (str) import status
    """

    populate_config()
    divider("Device Management")
    click.secho(f"[*] Starting device management.....", fg="cyan")
    click.secho(f"[*] Attempting {import_type} device import.....", fg="cyan")
    # ==================== SINGLE DEVICE IMPORT ========================================
    if import_type == "single":
        click.secho(f"[!] Attention: ", fg="yellow", nl=False)
        click.secho(f"Claiming single device does not support ", nl=False, fg="red")
        click.secho(f"day0 template configurations!", fg="red")
        if click.confirm(text=f"[-] Proceed?", abort=True):
            import_single_device(configs=dnac_configs, data=inputs)
    # =================== IMPORT  IN BULK ==============================================
    elif import_type == "bulk":
        if "device_catalog" not in kwargs:
            device_catalog_dir = os.path.join(
                all_configs["common"]["base_directory"], "catalog"
            )
            device_catalog_file = os.path.join(device_catalog_dir, "DeviceImport.csv")
            click.secho(
                f"[*] Looking for device catalog file in [{device_catalog_file}].....",
                fg="cyan",
            )
        else:
            device_catalog_file = kwargs.get("device_catalog")
            click.secho(
                f"[#] Using device import catalog file from: [{device_catalog_file}]",
                fg="green",
            )
        device_import_in_bulk(configs=dnac_configs, import_file=device_catalog_file)
    else:
        click.secho(f"Invalid import type!", fg="red")
        sys.exit(1)


# DNA center device deletion
def delete_manager(serials=None, delete_file=None, dry_run=None):
    """
    This function deletes one or more devices form DNA Center

    :param serials: (str) comma separated string of serial numbers
    :param delete_file: (str) Full file path with serial numbers
    :param dry_run: (boolean) True or False, to just show what serials will be deleted
    :return: (str) delete status on the screen
    """

    logging.debug(f"Dry run state: {dry_run}")
    if serials:
        try:
            logging.debug(f"Serials received from input: [{serials}]")
            serials_to_delete = serials.split(",")
        except Exception as err:
            click.secho(f"[x] Can't parse the input properly!", fg="red")
            click.secho(f"[x] ERROR: {err}")
            sys.exit(1)
    elif delete_file:
        logging.debug(f"File path: [{delete_file}]")
        delete_serials_file_path = delete_file
        serials_to_delete = parse_txt(serials_file_path=delete_serials_file_path)
    else:
        click.secho(
            f"[@] We are not that sure what you are trying to do. Make up your mind!",
            fg="red",
        )
        sys.exit(1)
    if dry_run is None:
        if click.confirm(
            text=f"[-] Delete {len(serials_to_delete)} devices?", abort=True
        ):
            populate_config()
            logging.debug(
                f"User confirmed deletion of [{len(serials_to_delete)}]devices"
            )
            divider("Deleting devices")
            click.secho(f"[*] Starting device deletion engine.....", fg="cyan")
            remove_devices(configs=dnac_configs, serials=serials_to_delete)
    else:
        for serial in serials_to_delete:
            click.secho(
                f"[*] Device with serial number [{serial}] will " f"be deleted.",
                fg="cyan",
            )


# DNA Center information showcase handler
def info_showcase_manager(**kwargs):
    """This function controls information showcase"""

    populate_config()
    if kwargs["command"] == "all_locations":
        do_show_all = True
        show_site_info(dnac_configs=dnac_configs, show_all=do_show_all)
    elif kwargs["command"] == "all_templates":
        do_show_all = True
        show_template_info(dnac_configs=dnac_configs, show_all=do_show_all)
    elif kwargs["command"] == "single_template":
        do_show_all = False
        dnac_template_name = kwargs["template"]
        logging.debug(f"Template Name from INPUT: {dnac_template_name}")
        show_template_info(
            dnac_configs=dnac_configs,
            template_name=dnac_template_name,
            show_all=do_show_all,
        )
    elif kwargs["command"] == "all_pnp_devices":
        do_show_all = True
        show_pnp_device_info(dnac_configs=dnac_configs, show_all=do_show_all)
    elif kwargs["command"] == "single_pnp_device":
        do_show_all = False
        dnac_device_serial = kwargs["device"]
        show_pnp_device_info(
            dnac_configs=dnac_configs,
            device_serial=dnac_device_serial,
            show_all=do_show_all,
        )
    elif kwargs["command"] == "export_pnp_to_csv":
        export_file = kwargs["file_path"]
        click.secho(f"[$] Export file path location: [{export_file}]", fg="blue")
        show_pnp_device_info(
            dnac_configs=dnac_configs, show_all=True, export_path=export_file
        )
