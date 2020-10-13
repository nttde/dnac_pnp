#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Main module for dnac-pnp"""

# Import builtin python libraries
import logging
import sys

# Import external python libraries
import click

# Import custom (local) python libraries
from .ios_utils import (
    debug_manager,
    initial_message,
    validate_file_extension,
    show_info,
)
from .device_reset_handler import device_reset

# Source code meta data
__author__ = "Dalwar Hossain"
__email__ = "dalwar.hossain@global.ntt"


# Alias group class
class AliasedGroup(click.Group):
    def get_command(self, ctx, cmd_name):
        rv = click.Group.get_command(self, ctx, cmd_name)
        if rv is not None:
            return rv
        matches = [x for x in self.list_commands(ctx) if x.startswith(cmd_name)]
        if not matches:
            return None
        elif len(matches) == 1:
            return click.Group.get_command(self, ctx, matches[0])
        matched_commands = ", ".join(sorted(matches))
        print(matched_commands)
        ctx.fail(f"Too many matches: {matched_commands}")


# Click context manager class
class Context(object):
    """Click context manager class"""

    def __init__(self):
        """Constructor method for click context manager class"""

        self.debug = False
        self.initial_msg = False


pass_context = click.make_pass_decorator(Context, ensure=True)


@click.group(cls=AliasedGroup)
@click.option(
    "--debug",
    "debug",
    is_flag=True,
    default=False,
    show_default=True,
    help="Turns on DEBUG mode.",
    type=str,
)
@click.version_option()
@pass_context
def mission_control(context, debug):
    """Mission control module"""

    context.debug = debug
    context.initial_msg = True
    context.dry_run = True
    context.show_help = False


@mission_control.command(short_help="Resets one or more IOS devices.")
@click.option(
    "-c",
    "--config-file",
    "config_file",
    help="Device access config file full file path.",
    required=False,
    type=click.Path(exists=True, dir_okay=False),
)
@click.option(
    "-r",
    "--reset-file",
    "reset_file",
    help="Device reset file full file path.",
    required=True,
    type=click.Path(exists=True, dir_okay=False),
    callback=validate_file_extension,
)
@click.option(
    "--debug",
    "sub_debug",
    is_flag=True,
    default=False,
    show_default=True,
    help="Turns on DEBUG mode.",
    type=str,
)
@pass_context
def reset(context, config_file, reset_file, sub_debug):
    """Add and claim single or multiple devices"""

    if context.initial_msg:
        initial_message()
    if context.debug or sub_debug:
        debug_manager()
    if reset_file:
        logging.debug(f"Reset file: {reset_file}")
        click.secho(f"[!] warning: Device reset file detected at input!", fg="yellow")
        click.secho(f"[*] Device reset file location: [{reset_file}]", fg="cyan")
        device_reset(config_path=config_file, reset_file_path=reset_file)
    else:
        click.secho(f"Reset file with IP address not provided!")
        sys.exit(1)


@mission_control.command(short_help="Shows package information.")
@click.option(
    "--author",
    "author",
    is_flag=True,
    default=False,
    show_default=True,
    help="Shows author information.",
    type=str,
    hidden=True,
)
@pass_context
# Information about this package
def pkg_info(context, author):
    """This module prints information about the package"""
    if author:
        show_info(view_type="author")
    else:
        show_info(view_type="more")
