#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This module handles the headers for API call"""

# Import builtin python libraries
import sys

# import external python libraries
from colorama import init, Fore

# Initialize
init(autoreset=True)

# Source code meta data
__author__ = "Dalwar Hossain"
__email__ = "dalwar.hossain@dimensiondata.com"


# Define get headers function
def get_headers():
    """
    This function returns appropriate headers

    :return: (dict) A python dictionary of headers
    """
    print(Fore.BLUE + "Setting API headers.....")
    headers = {"Content-Type": "application/json"}
    return headers
