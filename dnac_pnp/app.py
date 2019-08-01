#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Main module for dnac-pnp"""

# Import builtin python libraries
import sys

# Import external python libraries
from colorama import init, Fore

# Import custom (local) python libraries
from dnac_pnp.dnac_handler import import_manager

# Source code meta data
__author__ = "Dalwar Hossain"
__email__ = "dalwar.hossain@dimensiondata.com"

# Initialize text coloring
init(autoreset=True)


def mission_control():
    """Mission control module for this application"""
    import_manager(import_type="bulk")


if __name__ == "__main__":
    mission_control()
