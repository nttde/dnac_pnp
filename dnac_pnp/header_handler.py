#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This module handles the headers for API call"""

# Import builtin python libraries
import sys

# Source code meta data
__author__ = "Dalwar Hossain"
__email__ = "dalwar.hossain@dimensiondata.com"


# Define get headers function
def get_headers():
    """
    This function returns appropriate headers

    :param header_type: (str) API call header type (xml/json)
    :return: (dict) A python dictionary of headers
    """
    msg.info("Setting API headers.....")
    headers = {
        "Content-Type": "application/json"
    }
    return headers
