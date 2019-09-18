#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Parameters module for dnac_pnp"""

# Source code meta data
__author__ = "Dalwar Hossain"
__email__ = "dalwar.hossain@dimensiondata.com"

# Accepted http response codes
accepted_status_codes = [200, 202]
# Accepted (MUST have) CSV headers
accepted_csv_headers = ["serialNumber", "pid", "siteName", "name", "template_name"]
# PnP device limit
pnp_device_limit = 100
# Device Information extra parameters
device_extra_param = [
    "serialNumber",
    "name",
    "agentType",
    "pid",
    "state",
    "onbState",
    "imageFile",
    "imageVersion",
    "hostname",
    "source",
    "siteClaimType",
]
device_extra_param_less = ["serialNumber", "name", "pid", "state", "source"]
