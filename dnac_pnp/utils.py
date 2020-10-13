#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Utility module for dnac_pnp"""

# Import builtin python libraries
import csv
import collections
import json
import logging
import os
import re
import sys

# Import external python libraries
import click

# Import custom (local) python packages
from . import __maintainer__ as maintainer
from . import __maintainer_email__ as contact_email
from . import __license__ as package_license
from . import __package_name__ as package_name
from . import __version__ as version
from . import __author__ as author
from . import __author_email as author_email
from . import __copyright__ as copy_right
from .dnac_params import accepted_csv_headers, max_col_length

# Source code meta data
__author__ = "Dalwar Hossain"
__email__ = "dalwar.hossain@global.ntt"


# Show only package info
def _show_author_info():
    """This private function shows author information"""

    divider("Author Information")
    author_info = {
        "Package Name": package_name,
        "Version": version,
        "Author": author,
        "Contact": author_email,
        "Copyright": copy_right,
    }
    for key, value in author_info.items():
        click.secho(f"[*] {key}: ", fg="cyan", nl=False)
        click.secho(f"{value}", fg="yellow")


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
        click.secho(f"[*] {key}: ", fg="cyan", nl=False)
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
            click.secho(f"[*] {key}: ", fg="cyan", nl=False)
            click.secho(f"{value}", fg="yellow")
    except Exception as err:
        click.secho(f"[x] Can not obtain compatible package information.", fg="red")
        click.secho(f"[x] ERROR: {err}", fg="red")
        sys.exit(1)


# Show information about the package
def show_info(view_type=None):
    """
    This function prints information about the package on screen

    :param view_type: (boolean) To show more or less info
    :returns: (stdout) output to the screen
    """

    click.clear()
    if view_type == "more":
        _show_pkg_info()
        _show_dnac_dependencies()

    if view_type == "less":
        _show_pkg_info()
    if view_type == "author":
        _show_author_info()
    goodbye()


# Validate input serial number
def validate_serial(ctx, param, value):
    """This function validates serial number"""

    if value:
        if not value.isalnum():
            click.secho(
                f"[x] Serial Number must be alphanumeric and less than 11 characters",
                fg="red",
            )
            ctx.abort()
        else:
            if len(value) > 11:
                click.secho(
                    f"[x] Serial Number must be less than 11 characters", fg="red"
                )
                ctx.abort()
            else:
                return value
    else:
        return False


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

    allowed_extensions = ["csv", "txt"]
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
        f"[*] Please use 'dnac_pnp --help' to see all available options", fg="cyan"
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
        "[+] %(levelname)s %(asctime)-15s [%(filename)s:%(lineno)s - %(funcName)20s() ]"
        " %(message)s",
        fg="yellow",
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
    :return: (stdout) on screen
    """

    pretty = True
    line_max = max_col_length
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
    camel_cased_string = "".join(
        w.lower() if i is 0 else w.title() for i, w in enumerate(words)
    )
    return camel_cased_string


# Check cell name
def check_csv_cell_name(cell_name=None):
    """
    This function checks validity of single CSV cell name

    :param cell_name: (str) Cell name form file
    :return: (str) Valid cell name
    """

    product_id = re.match("^[pP]roduct.*$", cell_name)
    device_name = re.match("^[dD]evice.*$", cell_name)
    if product_id:
        logging.debug(f"Product ID header [{cell_name}] in CSV, converting.....")
        valid_cell_name = "pid"
    elif device_name:
        logging.debug(f"Device name header [{cell_name}] in CSV, converting.....")
        valid_cell_name = "hostname"
    else:
        valid_cell_name = do_camel_case(cell_name)
    return valid_cell_name


# Check CSV headers
def check_csv_header(file_headers=None):
    """
    This function checks the csv headers against accepted headers

    :param file_headers: (list) A list of headers retrieved from CSV file
    :return: (list) A list (subset or equal) of headers that has been checked
    """

    template_flag = False
    ret_headers = []
    for cell in file_headers:
        if "template" in cell:
            template_flag = True
        if template_flag:
            ret_headers.append(cell)
        else:
            valid_cell_name = check_csv_cell_name(cell_name=cell)
            ret_headers.append(valid_cell_name)
    logging.debug(f"camelCased headers: {ret_headers}")
    logging.debug(f"Type of input headers: {type(file_headers)}")
    logging.debug(f"Type of converted headers: {type(ret_headers)}")
    if all(item in ret_headers for item in accepted_csv_headers):
        return ret_headers
    else:
        click.secho(
            f"[x] The list of headers does not match with accepted headers!", fg="red"
        )
        click.secho(f"[*] Retrieved headers from file: {file_headers}", fg="cyan")
        click.secho(
            f"[!] Warning! camelCased and unicode headers are not accepted!",
            fg="yellow",
        )
        click.secho(
            f"[!] Warning! Underscore(_), Dash/Hyphen(-), Single Space ( ) "
            f"are accepted between words",
            fg="yellow",
        )
        click.secho(
            f"[*] Accepted header syntax: Some_Thing, Other-Thing, Another Thing",
            fg="cyan",
        )
        sys.exit(1)


# Parse CSV input
def parse_csv(file_to_parse=None):
    """
    This function parses CSV for device import

    :param file_to_parse: (str) Full path of CSV file
    :returns: (list) of dictionaries with each row as an item
    """

    logging.debug(f"Reading csv from [{file_to_parse}]")
    csv_rows = []
    with open(file_to_parse) as csv_import_file:
        reader = csv.DictReader(csv_import_file)
        r_title = [item.strip() for item in reader.fieldnames]
        logging.debug(f"CSV file headers: {r_title}")
        title = check_csv_header(file_headers=r_title)
        for r_row in reader:
            logging.debug(f"Raw input row from file: {r_row}")
            try:
                l_row = []
                template_flag = False
                for key, value in r_row.items():
                    if "template" in key.strip():
                        template_flag = True
                    if template_flag:
                        l_row.append((key.strip(), value.strip()))
                    else:
                        l_row.append((check_csv_cell_name(key.strip()), value.strip()))
                row = collections.OrderedDict(l_row)
            except AttributeError or KeyError:
                logging.debug(f"AttributeError: An attribute error has occurred!")
                logging.debug(f"Skipping row: {r_row}")
                continue
            logging.debug(f"Stripped row: {row}")
            csv_rows.extend([{title[i]: row[title[i]] for i in range(len(title))}])
    return csv_rows


# Parse txt file to delete serials
def parse_txt(serials_file_path=None):
    """
    This function parses a text file line by line and returns a list of serials

    :param serials_file_path: (str) Full path to serials to delete file
    :return: (list) A list of serials
    """

    with open(serials_file_path) as serials_file:
        serials_to_delete_crlf = serials_file.readlines()
        serials_to_delete = [
            serial.strip() for serial in serials_to_delete_crlf if serial.strip()
        ]
    return serials_to_delete


# Goodbye
def goodbye(before=False, data=None):
    """
    Shows goodbye message

    :param before: (boolean) Whether to show a message before goodbye
    :param data: (dict) skipped information
    :return: (stdout) On screen output
    """

    if before:
        if data:
            divider("Before we leave, Please note ")
            click.secho(f"[*] Total serial skipped: {len(data)}", fg="cyan")
            click.secho(f"[*] Skipped Serials: ", fg="cyan", nl=False)
            click.secho(f"{data}", fg="yellow")
        divider("Goodbye!")
    else:
        divider("Goodbye!")
