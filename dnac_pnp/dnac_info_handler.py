#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Information handler functions"""

# Import builtin python libraries
import json
import logging
import sys

# Import external python libraries
import click

# Import custom (local) python packages
from .dnac_info_butler import get_template_id, get_template_parameters
from .dnac_token_generator import generate_token
from .header_handler import get_headers
from .utils import divider, goodbye

# Source code meta data
__author__ = "Dalwar Hossain"
__email__ = "dalwar.hossain@dimensiondata.com"


# Show template body and the parameters
def show_template_info(dnac_configs=None, template_name=None, show_all=False):
    """
    This function shows details about a single template

    :param dnac_configs: (dict) DNA Center username/password configurations
    :param template_name: (str) Name of the template
    :param show_all: (boolean) List all or show details of one
    :return: (stdOut) On screen output
    """

    token = generate_token(configs=dnac_configs)
    headers = get_headers(auth_token=token)

    divider("Template(s)")
    template_id = get_template_id(
        api_headers=headers, show_all=show_all, template=template_name
    )
    if not show_all:
        if template_id is not None:
            template_content, template_parameters = get_template_parameters(
                api_headers=headers, config_id=template_id
            )
            if template_content and template_parameters:
                click.secho(f"[$] Template Body:", fg="blue")
                print(template_content)
                click.secho(f"[$] Template Parameters:", fg="blue")
                print(template_parameters)
            else:
                click.secho(f"[x] Could not retrieve parameters! Use --debug to get "
                            f"more information", fg="red")
        else:
            click.secho("[x] No template found!", fg="red")
            click.secho(f"[*] Make sure that the spelling is correct and has "
                        f"[project_name/template_name] syntax", fg="blue")
    else:
        if template_id:
            pass
    goodbye()
