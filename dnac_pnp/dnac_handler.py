#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
First Edit
----------

First Edit Author: Kamlesh Koladiya

Email: kamlesh.koladiya@dimensiondata.com
"""

# Source code meta data
__author__ = "Dalwar Hossain"
__email__ = "dalwar.hossain@dimensiondata.com"

# Import builtin python libraries
import os
import sys

# import external python libraries
import click

# Import custom (local) python packages
from ._validators import divider
from .config_handler import config_files, load_config
from .device_import_handler import device_import_in_bulk, import_single_device

# Setting global host variable
all_configs = {}
dnac_configs = {}
host = ""


# Import one or more devices
def import_manager(inputs=None, import_type=None, **kwargs):
    """
    This module manages import of the device(s)

    :param inputs: (dict) A dictionary of user provided inputs
    :param import_type: (str) device import type "single" or "bulk"
    :param kwargs: (kwargs) Key value pair
    :returns: (str) import status
    """

    # Using the defined global variables
    global all_configs
    global dnac_configs
    global host

    divider("Configurations")
    if not all_configs:
        all_configs = load_config(config_files)
        dnac_configs = all_configs["dnac"]
        host = dnac_configs["host"]

    divider("Device Management")
    click.secho(f"[*] Starting device management.....", fg="cyan")
    click.secho(f"[*] Attempting {import_type} device import.....", fg="cyan")
    # ==================== SINGLE DEVICE IMPORT ===========================================
    if import_type == "single":
        import_single_device(configs=dnac_configs, data=inputs)
    # =================== IMPORT  IN BULK =================================================
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
def delete_devices(serials=None):
    """
    This function deletes one or more devices form DNAC PnP"

    :param serials: (str) comma separated string of serial numbers
    :return: (str) delete status on the screen
    """

    pass
