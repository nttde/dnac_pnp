#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This module handles the headers for API call"""

# import external python libraries
import click

# Source code meta data
__author__ = "Dalwar Hossain"
__email__ = "dalwar.hossain@dimensiondata.com"


# Define get headers function
def get_headers():
    """
    This function returns appropriate headers

    :return: (dict) A python dictionary of headers
    """
    click.secho(f"[$] Setting API headers.....", fg="blue")
    headers = {"Content-Type": "application/json"}
    return headers
