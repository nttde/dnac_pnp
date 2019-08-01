#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Main module for dnac-pnp"""

# Import builtin python libraries
import sys

# Import external python libraries
from colorama import init, Fore
from wasabi import Printer

# Source code meta data
__author__ = "Dalwar Hossain"
__email__ = "dalwar.hossain@dimensiondata.com"

# Initialize
init(autoreset=True)
msg = Printer()


# Single device import
def import_single_device(api_headers=None, **kwargs):
    """This module imports single device into dnac"""
    pass


# Bulk device import
def import_bulk_device(api_headers=None, **kwargs):
    """This module imports devices in bulk"""
    pass
