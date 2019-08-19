#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open("README.rst") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst") as history_file:
    history = history_file.read()

requirements = ["Click>=7.0"]

setup_requirements = []

test_requirements = []

setup(
    author="NTT Dimensiondata PS Automation Team",
    author_email="DE.PS.DI.Automation@dimensiondata.com",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3 :: Only",
    ],
    description="Cisco DNA center PnP device add, claim and delete functionalities",
    entry_points={"console_scripts": ["dnac_pnp=dnac_pnp.app:mission_control"]},
    install_requires=requirements,
    long_description=readme + "\n\n" + history,
    include_package_data=True,
    keywords="dnac_pnp",
    name="dnac_pnp",
    packages=find_packages(include=["dnac_pnp"]),
    setup_requires=setup_requirements,
    test_suite="tests",
    tests_require=test_requirements,
    url="https://scm.dimensiondata.com/de-ps/automation/carnival/dnac-pnp",
    version="0.2.4",
    zip_safe=False,
)
