#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Main module for dnac-pnp"""

# Import external python libraries
from colorama import init, Fore

# Import custom python libraries
from dnac_pnp.dnac_handler import dnac_login
from dnac_pnp.config_handler import config_files, load_config

# Source code meta data
__author__ = "Dalwar Hossain"
__email__ = "dalwar.hossain@dimensiondata.com"

# Initialize text coloring
init(autoreset=True)


def mission_control():
    """Mission control module for this application"""
    all_configs = load_config(config_files)
    dnac_configs = all_configs['dnac']
    token = dnac_login(host=dnac_configs['host'], username=dnac_configs['username'], password=dnac_configs['password'])
    print(Fore.GREEN + "Token received!")
    print(f"Token: {token}")


if __name__ == "__main__":
    mission_control()
