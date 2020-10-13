#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""The setup script"""

from setuptools import setup, find_packages

with open("README.rst", "r", encoding="utf-8") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst", "r", encoding="utf-8") as history_file:
    history = history_file.read()

requirements = [
    "click>=7.0",
    "requests>=2.22.0",
    "colorama>=0.4.1",
    "pyyaml>=5.1.1",
    "tabulate>=0.8.3",
    "netmiko>=2.4.1",
    "tqdm>=4.36.1"
]

setup_requirements = []

test_requirements = []

setup(
    author="Dalwar Hossain",
    author_email="dalwar.hossain@global.ntt",
    maintainer="NTT Germany Network Automation Development Team",
    maintainer_email="DE.PS.DI.Automation@global.ntt",
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3 :: Only",
    ],
    description="Cisco DNA center PnP device add, claim and delete automation",
    entry_points={
        "console_scripts": [
            "dnac_pnp=dnac_pnp.app:mission_control",
            "ios_reset=ios_reset.ios:mission_control",
        ]
    },
    install_requires=requirements,
    license="BSD-3-Clause License",
    long_description=readme + "\n\n" + history,
    include_package_data=True,
    keywords=["dnac", "pnp", "cisco", "NTT"],
    name="dnac_pnp",
    packages=find_packages(include=["dnac_pnp"]),
    setup_requires=setup_requirements,
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/nttde/dnac_pnp.git",
    version="1.0.2b1",
    zip_safe=False,
)
