#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Validation module for dnac_pnp"""

# Import builtin python libraries
import sys
import logging
import re

# Import external python libraries
from wasabi import Printer
import click

# Source code meta data
__author__ = "Dalwar Hossain"
__email__ = "dalwar.hossain@dimensiondata.com"

# Initialize wasabi printer class
msg = Printer()

# Accepted status codes
accepted_status_codes = [200]


# Show information about the package
def show_info():
    """This module prints information about the package on screen"""

    try:
        from dnac_pnp import __package_name__ as package_name
        from dnac_pnp import __version__ as version
        from dnac_pnp import __license__ as package_license
        from dnac_pnp import __author__ as maintainer
        from dnac_pnp import __email__ as email
    except ImportError:
        click.secho(f"[x] Can't import information", fg="red")
        sys.exit(1)
    click.secho(f"Package Name: ", fg="cyan", nl=False)
    click.secho(f"{package_name}")
    click.secho(f"Version: ", fg="cyan", nl=False)
    click.secho(f"{version}")
    click.secho(f"License: ", fg="cyan", nl=False)
    click.secho(f"{package_license}")
    click.secho(f"Maintainer: ", fg="cyan", nl=False)
    click.secho(f"{maintainer}")
    click.secho(f"Contact : ", fg="cyan", nl=False)
    click.secho(f"{email}")


# Validate input serial number
def validate_serial(ctx, param, value):
    """This function validates serial number"""

    if not value.isalnum():
        click.secho(f"[x] Serial Number must be alphanumeric and must be 11 characters in length or less.", fg="red")
        ctx.abort()
    else:
        if len(value) > 11:
            click.secho(f"[x] Serial Number must be alphanumeric and must be 11 characters in length or less.")
        else:
            return value


# Validate rest of the inputs
def validate_input(ctx, param, value):
    """This function validates other inputs. [alphanumeric and - and _]"""
    if not re.match("^[A-Za-z0-9_-]*$", value):
        click.secho(f"[x] Invalid input! No special character is accepted except [- and _]", fg="red")
        ctx.abort()
    else:
        return value


# Validate file extension
def validate_file_extension(ctx, param, value):
    """This function validates file extensions"""

    allowed_extensions = ["csv"]
    if value.rsplit(".", 1)[1] not in allowed_extensions:
        click.secho(f"[x] Provided file extension not allowed!", fg="red")
        ctx.abort()
    else:
        return value


# Initial message
def initial_message():
    """This function shows the initialization message"""

    click.clear()
    msg.divider("Initializing")
    click.secho(f"[*] Initializing.....", fg="cyan")


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
    debug_format = click.style("[+] %(levelname)s %(asctime)-15s %(message)s", fg="yellow")
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
