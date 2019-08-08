#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Validation module for dnac_pnp"""

# Import builtin python libraries
import collections
import sys
import os
import logging
import re
import json

# Import external python libraries
import click

# Import custom (local) python packages
from dnac_pnp import (
    __package_name__ as package_name,
    __author__ as maintainer,
    __email__ as contact_email,
    __version__ as version,
    __license__ as package_license,
    __coffee__ as coffee,
)

# Source code meta data
__author__ = "Dalwar Hossain"
__email__ = "dalwar.hossain@dimensiondata.com"


# Accepted values
accepted_status_codes = [200]
accepted_csv_headers = ["serialNumber", "pid", "siteName", "name"]


# Show only package info
def _show_pkg_info():
    """This private function shows package information"""

    divider("Package Information")
    pkg_info = {
        "Package Name": package_name,
        "Version": version,
        "Maintainer": maintainer,
        "Contact": contact_email,
        "License": package_license,
    }
    for key, value in pkg_info.items():
        click.secho(f"{key}: ", fg="cyan", nl=False)
        click.secho(f"{value}", fg="yellow")


# Show DNAC Dependency list
def _show_dnac_dependencies():
    """This private method shows DNA center dependencies for this package"""

    try:
        pkg_file = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "compatible_dnac_packages.json"
        )
        with open(pkg_file) as pkg_info:
            data = json.load(pkg_info)
            divider("DNA Center Dependency Information")
        for key, value in data.items():
            click.secho(f"{key}: ", fg="cyan", nl=False)
            click.secho(f"{value}", fg="yellow")
    except Exception as err:
        click.secho(f"[x] Can not obtain compatible package information.", fg="red")
        click.secho(f"[x] ERROR: {err}", fg="red")
        sys.exit(1)


# Show information about the package
def show_info(view_type=None):
    """
    This module prints information about the package on screen

    :param view_type: (boolean) To show more or less info
    :returns: (stdout) output to the screen
    """

    if view_type == "more":
        _show_pkg_info()
        _show_dnac_dependencies()

    if view_type == "less":
        _show_pkg_info()
    divider(coffee)


# Validate input serial number
def validate_serial(ctx, param, value):
    """This function validates serial number"""

    if not value.isalnum():
        click.secho(
            f"[x] Serial Number must be alphanumeric and must be 11 characters in length or less.",
            fg="red",
        )
        ctx.abort()
    else:
        if len(value) > 11:
            click.secho(
                f"[x] Serial Number must be alphanumeric and must be 11 characters in length or less."
            )
            ctx.abort()
        else:
            return value


# Validate rest of the inputs
def validate_input(ctx, param, value):
    """This function validates other inputs. [alphanumeric and - and _]"""
    if not re.match("^[A-Za-z0-9_-]*$", value):
        click.secho(
            f"[x] Invalid input! No special character is accepted except [- and _]",
            fg="red",
        )
        ctx.abort()
    else:
        return value


# Validate file extension
def validate_file_extension(ctx, param, value):
    """This function validates file extensions"""

    allowed_extensions = ["csv"]
    if value:
        try:
            ext = value.rsplit(".", 1)[1]
        except AttributeError:
            return False
        if ext not in allowed_extensions:
            click.secho(
                f"[x] Provided file extension [{ext}] is not allowed!", fg="red"
            )
            ctx.abort()
        else:
            return value


# Initial message
def initial_message():
    """This function shows the initialization message"""

    click.clear()
    divider(f"Initializing [{package_name}]")
    click.secho(f"[*] Initializing.....", fg="cyan")
    click.secho(
        f"[*] Please use 'dnac_pnp info' command to see supported version of Cisco DNA Center",
        fg="cyan",
    )


# Turn on/off debugging
def debug_manager():
    """This function acts accordingly with --debug switch"""

    try:
        from http.client import HTTPConnection
    except ImportError:
        click.secho(f"[x] Can't import http client", fg="red")
        sys.exit(1)
    click.secho(f"[+] ", nl=False, fg="yellow")
    click.secho(f"DEBUG mode is ON", fg="black", bg="yellow")
    debug_format = click.style(
        "[+] %(levelname)s %(asctime)-15s %(message)s", fg="yellow"
    )
    HTTPConnection.debuglevel = 4
    logging.basicConfig(format=debug_format)
    logging.getLogger().setLevel(logging.DEBUG)
    requests_log = logging.getLogger("urllib3")
    requests_log.setLevel(logging.DEBUG)
    requests_log.propagate = True


# Validate delete input
def validate_delete_input(ctx, param, value):
    """This function validates the device delete input"""

    if not value.isalnum():
        click.secho(f"[x] Provided input is not supported!", fg="red")
        click.secho(f"[*] Use comma separated values", fg="cyan")
        ctx.abort()
    else:
        return value


# Divider function
def divider(text="", char="="):
    """
    Print a divider with a headline:

    :param text: (unicode) Headline text. If empty, only the line is printed.
    :param char: (unicode) Line character to repeat, e.g. =.
    :returns: (stdout) on screen
    """

    pretty = True
    line_max = 88
    if len(char) != 1:
        raise ValueError(
            "Divider chars need to be one character long. " "Received: {}".format(char)
        )
    if pretty:
        deco = char * (int(round((line_max - len(text))) / 2) - 2)
        text = " {} ".format(text) if text else ""
        text = f"{deco}{text}{deco}"
    if len(text) < line_max:
        text = text + char * (line_max - len(text))
    click.secho(text, fg="magenta")


# Create camelCase strings
def do_camel_case(input_string=None):
    """
    This function creates camelCased strings

    .. warning::

       Can't handle already camelCased string and unicode strings

    :param input_string: (str) string to be camel cased
    :returns: (str) Camel cased string
    """

    word_regex_pattern = re.compile("[^A-Za-z]+")
    words = word_regex_pattern.split(input_string)
    camel_cased_string = "".join(w.lower() if i is 0 else w.title() for i, w in enumerate(words))
    return camel_cased_string


# Check cell name
def check_csv_cell_name(cell_name=None):
    """
    This function checks validity of single CSV cell name

    :param cell_name: (str) Cell name form file
    :return: (str) Valid cell name
    """

    invalid_entry = re.match("^[pP]roduct.*$", cell_name)
    if invalid_entry:
        logging.debug(f"Found invalid header [{cell_name}] in CSV, converting.....")
        valid_cell_name = "pid"
    else:
        valid_cell_name = do_camel_case(cell_name)
    return  valid_cell_name


# Check CSV headers
def check_csv_header(file_headers=None):
    """
    This function checks the csv headers against accepted headers

    :param file_headers: (list) A list of headers retrieved from CSV file
    :return: (list) A list (subset or equal) of headers that has been checked
    """

    ret_headers = []
    for cell in file_headers:
        valid_cell_name = check_csv_cell_name(cell_name=cell)
        ret_headers.append(valid_cell_name)
    logging.debug(f"camelCased headers: {ret_headers}")
    if collections.Counter(accepted_csv_headers) == collections.Counter(ret_headers):
        click.secho(f"[#] The list of headers is accepted!", fg="green")
        return ret_headers
    else:
        click.secho(f"[x] The list of headers does not match with accepted headers!", fg="red")
        click.secho(f"[*] Retrieved headers from file: {file_headers}", fg="cyan")
        click.secho(f"[*] Accepted headers: {accepted_csv_headers}", fg="cyan")
        sys.exit(1)
