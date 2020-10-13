#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This module handles the headers for API call"""

# Import builtin python libraries
import logging

# Import external python libraries
import click

# Source code meta data
__author__ = "Dalwar Hossain"
__email__ = "dalwar.hossain@global.ntt"


# Define get headers function
def get_headers(auth_token=None):
    """
    This function returns appropriate headers

    :param auth_token: (str) Authentication token
    :return: (dict) A python dictionary of headers
    """

    headers = {"Content-Type": "application/json"}
    if auth_token is None:
        return headers
    else:
        logging.debug(f"Token in header:{auth_token}")
        headers["X-Auth-Token"] = auth_token
        logging.debug(f"Headers: {headers}")
        return headers
