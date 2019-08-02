#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This module loads the different configurations"""


# Import builtin python libraries
import os
import sys
from pathlib import Path
import logging

# Import external python libraries
import yaml
from colorama import init, Fore

# Import custom python libraries
from dnac_pnp import __package_name__ as package_name

# Source code meta data
__author__ = "Dalwar Hossain"
__email__ = "dalwar.hossain@dimensiondata.com"


# Initialize wasabi
init(autoreset=True)

# Config and template path
base_locations = [
    os.path.join(os.path.expanduser("~"), f".{package_name}"),
    os.path.join(os.getcwd(), f".{package_name}"),
    f"/etc/{package_name}",
]
config_locations = [os.path.join(base_path, "configs") for base_path in base_locations]
base_file_names = ["config"]
base_file_extensions = ["yaml", "yml"]
file_names = [
    file_name + "." + file_extension
    for file_name in base_file_names
    for file_extension in base_file_extensions
]
config_files = [
    os.path.join(config_location, file_name)
    for config_location in config_locations
    for file_name in file_names
]


# Read configurations
def _read_configs(config_file_paths=None):
    """
    This function reads configurations from a .yml file

    :param config_file_paths: Configuration files full path (default and custom)
    """
    print(Fore.BLUE + "Reading configurations.....")
    for config_file in config_file_paths:
        with open(config_file, "r") as stream:
            try:
                defaults = yaml.load(stream, Loader=yaml.FullLoader)
            except Exception as err:
                print(Fore.RED + f"ERROR: {err}")
                sys.exit(1)
    return defaults


def load_config(config_file_paths=None):
    """
    This function reads and load the configurations into the system

    :param config_file_paths: (list) A list of paths for configuration lookup
    :return: (dict) Merged configurations
    """

    # Config finder flag
    file_flag = 0
    permission_flag = 0

    logging.info(f"Default lookup paths: {config_file_paths}")
    for path in config_file_paths:
        print(Fore.CYAN + f"Looking for config in: [{path}].....")
        if os.path.exists(path) and os.path.isfile(path):
            file_flag = 1
            if os.access(path, os.F_OK) and os.access(path, os.R_OK):
                print(Fore.GREEN + "Using configuration from: [{}]".format(path))
                default_config = path
                if os.path.exists(default_config) and os.path.isfile(default_config):
                    permission_flag = 1
                break
            else:
                print(Fore.YELLOW + "Permission ERROR: [{}]".format(path))
                permission_flag = 0
        else:
            file_flag = 0
    if file_flag == 1 and permission_flag == 1:
        # Read configurations
        all_configs = _read_configs(config_file_paths=[default_config])
    else:
        print(Fore.YELLOW + "Couldn't locate configuration file!")
        sys.exit(1)
    base_directory = Path(Path(default_config).parent).parent
    # Create "common" key at runtime
    all_configs["common"] = {}
    all_configs["common"]["base_directory"] = base_directory
    print(Fore.GREEN + "Configuration read complete!")
    logging.info(f"Configs: {all_configs}")
    return all_configs
