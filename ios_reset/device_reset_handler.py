#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Main module for dnac-pnp"""

# Import builtin python libraries
import ipaddress
import json
import logging
import os
import sys

# Import external python libraries
import click
from netmiko import ConnectHandler

# Import custom (local) python packages
from .config_handler import load_config
from .ios_utils import divider, goodbye

# Source code meta data
__author__ = "Dalwar Hossain"
__email__ = "dalwar.hossain@dimensiondata.com"


def _file_parser(file_path=None):
    """
    This private function parses a file into a list

    :param file_path: (str) Full path to the file
    :return: (list) Each line as an element of python list
    """

    if os.path.isfile(file_path):
        try:
            logging.debug(f"Parsing file path: {file_path}")
            with open(file_path, "r") as f:
                lines = f.readlines()
                lines_as_list = [line.strip() for line in lines]
                if lines_as_list:
                    return lines_as_list
        except IOError:
            click.secho(f"[x] IO Error! ERROR: {IOError}", fg="red")
            sys.exit(1)
    else:
        click.secho(f"[x] File [{file_path}] does not exists!", fg="red")
        sys.exit(1)


def _check_ip_address(ip=None):
    """
    This function validates ip address

    :param ip: (str) IP address
    :return: (str) Valid IP or False otherwise
    """

    try:
        valid_ip = ipaddress.ip_address(f"{ip}")
        logging.debug(f"Valid IP: {valid_ip}")
        click.secho(f"[#] IP address validated!", fg="green")
        return str(ipaddress.ip_address(valid_ip))
    except ValueError:
        logging.debug(f"Invalid IP: {ip}")
        click.secho(f"[x] IP address [{ip}] is invalid", fg="red")
        return False


def _reset_device(config=None, commands=None):
    """
    This private method resets the device with ssh connection

    :param config: (dict) Device login configurations
    :param commands: (list) commands to be executed to reset the device
    :return: (str) Output of the commands
    """

    try:
        ssh_client = ConnectHandler(**config)
    except Exception as err:
        click.secho(f"[x] Connection Error: {err}", fg="red")
        return False
    if ssh_client:
        try:
            ssh_client.enable()
        except NameError:
            click.secho(f"[x] Connection to device [{config['host']}] was "
                        f"not successful", fg="red")
            return False
        try:
            output = ssh_client.send_config_set(commands)
            return output
        except EOFError:
            print(f"Connection to device terminated!")
            print(f"Device [{config['host']}] might be reloading.....")
        except NameError:
            print(f"Connection to device [{config['host']}] was not successful")


def device_reset(config_path=None, reset_file_path=None):
    """
    This function resets one or more devices

    :param config_path: (str) Device login configurations full file path
    :param reset_file_path: (str) Full path to reset file with IP address
    :return: (stdOut) Std output on screen
    """

    if config_path is None:
        logging.debug(f"No configuration provided")
        click.secho(
            f"Configuration file not provided! Looking into default " f"locations!"
        )
        configs = load_config(config_file_paths=None)
    else:
        configs = load_config(config_file_paths=[config_path])

    login_config = configs["device_login"]
    logging.debug(f"Login details: {json.dumps(login_config, indent=4)}")
    try:
        reset_command_file = configs["reset_commands"]["file"]
        logging.debug(f"Rest command file: {json.dumps(reset_command_file, indent=4)}")
    except KeyError:
        click.secho(f"[x] Key Error! Error: {KeyError}", fg="red")
        click.secho(f"[x] Malformed configuration file!", fg="red")
        sys.exit(1)
    divider("Device reset")
    if reset_file_path:
        reset_commands = _file_parser(file_path=reset_command_file)
        ip_addresses = _file_parser(file_path=reset_file_path)
        for ip_address in ip_addresses:
            logging.debug(f"IP address: {ip_address}")
            divider(f"Resetting [{ip_address}]", char="-")
            click.secho(f"[$] Validating IP: {ip_address}", fg="blue")
            host_ip = _check_ip_address(ip=ip_address)
            if host_ip:
                login_config["host"] = host_ip
                reset_output = _reset_device(
                    config=login_config, commands=reset_commands
                )
                click.secho(f"[#] Output:", fg="green")
                click.secho(f"{reset_output}")
            else:
                click.secho(f"[!] Invalid IP address! "
                            f"Skipping [{ip_address}].....", fg="yellow")
                continue
        goodbye()
