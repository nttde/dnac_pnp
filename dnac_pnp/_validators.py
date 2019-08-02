#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Validation module for dnac_pnp"""

# Import builtin python libraries
import sys

# Import external python libraries
from colorama import init, Fore

# Source code meta data
__author__ = "Dalwar Hossain"
__email__ = "dalwar.hossain@dimensiondata.com"

# Initialize text coloring
init(autoreset=True)


# Show information about the package
def show_info():
    """This module prints information about the package on screen"""

    try:
        from dnac_pnp import __package_name__ as package_name
        from dnac_pnp import __version__ as version
        from dnac_pnp import __license__ as package_license
        from dnac_pnp import __author__ as author
        from dnac_pnp import __email__ as email
    except ImportError:
        print(Fore.RED + f"[x] Can't import information")
        sys.exit(1)
    print(Fore.CYAN + f"Package Name: " + Fore.GREEN + f"{package_name}")
    print(Fore.CYAN + f"Version: " + Fore.GREEN + f"{version}")
    print(Fore.CYAN + f"License: " + Fore.GREEN + f"{package_license}")
    print(Fore.CYAN + f"Author: " + Fore.GREEN + f"{author}")
    print(Fore.CYAN + f"Contact: " + Fore.GREEN + f"{email}")


# Validate input serial number
def validate_alphanumeric(ctx, param, value):
    """This function validates and allows only letters and numbers"""

    if not value.isalnum():
        print(Fore.RED + "[x] Invalid input!")
        ctx.abort()
    else:
        return value


# Validate file extension
def validate_file_extension(ctx, param, value):
    """This function validates file extensions"""

    allowed_extensions = ["csv"]
    if value.rsplit(".", 1)[1] not in allowed_extensions:
        print(Fore.RED + "[x] Provided file extension not allowed!")
        ctx.abort()
    else:
        return value
