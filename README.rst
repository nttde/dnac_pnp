========
dnac-pnp
========

Cisco DNA center device claim and delete automation

.. image:: https://img.shields.io/badge/license-bsd--3--clause-blue.svg?style=for-the-badge
    :alt: License
    :target: https://opensource.org/licenses/BSD-3-Clause

.. image:: https://img.shields.io/pypi/v/dnac_pnp.svg?logo=python&style=for-the-badge
    :alt: Pypi Version
    :target: https://pypi.org/project/dnac_pnp/

.. image:: https://img.shields.io/pypi/wheel/dnac_pnp?color=blue&logo=python&style=for-the-badge
   :alt: PyPI - Wheel
   :target: https://dnc-pnp.readthedocs.io/

.. image:: https://img.shields.io/pypi/pyversions/dnac_pnp?logo=python&style=for-the-badge
   :alt: PyPI - Python Version
   :target: https://dnc-pnp.readthedocs.io/

.. image:: https://img.shields.io/badge/platform-windows%2Flinux%2Fmacos-blue.svg?style=for-the-badge
   :alt: Supported platforms
   :target: https://dnc-pnp.readthedocs.io/

.. image:: https://readthedocs.org/projects/dnac-pnp/badge/?version=latest&style=for-the-badge
   :target: https://dnac-pnp.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status

.. image:: https://img.shields.io/badge/code%20style-black-black.svg?style=for-the-badge
    :target: https://github.com/python/black
    :alt: Code Style

Features
--------

Behaviour
^^^^^^^^^
* ``Git`` alike commandline user interface
* Define user credentials and host for DNAC
* Read configurations from file
* Configurations file lookup in 3 default locations

Checks
^^^^^^
* Pre-checks user inputs
* Pre-checks csv file for bulk import (add+claim)
* Pre-checks txt file for bulk delete
* Pre-check templates
* Pre-check and warning messages for template variables
* Pre-checks for valid sites
* Pre-checks for device status

Import
^^^^^^
* Single import of device
* Bulk import devices from csv
* Single site creation
* Bulk site creation

Delete
^^^^^^
* Single device deletion, more than one device deletion
* Bulk device delete from txt file
* Single/Multiple Device delete even after provision

Decision
^^^^^^^^
* Decision based on site status and device status
* Read day0 template
* Decide on day0 template parameters are provided properly or not
* Shows day0 template parameters
* Day0 configuration

View
^^^^
* Shows all pnp devices
* Shows details about a single device by serial number
* Shows all available templates
* Shows specific template body and variables by full template name
* Shows all available locations

Export
^^^^^^
* Export all PnP devices to csv

Dependencies
------------

This package requires a configuration file in either ``.yaml`` or ``yml`` format. The look up priority for
the configuration file is as following-

1. <user_home_directory>/.<package_name>/configs/config.yaml (``Window/Linux/MacOS``)
2. <current_working_directory>/.<package_name>/configs/config.yaml (``Windows/Linux/MacOS``)
3. /etc/<package_name>/configs/config.yaml (``Linux/MacOS``)

If ``config.yaml`` doesn't exists in one of these locations, the program will NOT run. So, to create the configuration
file, please use -

**Windows**

Windows system by default doesn't allow creation of ``.`` prefixed directory from GUI, so use the following -

- Open `cmd` and change the directory to the ``home`` folder of the user
- Run ``mkdir .dnac_pnp``
- Run ``cd .dnac_pnp``
- Run ``mkdir configs``

Now that the ``.`` prefixed directory is created, use the GUI to add a file in ``configs`` directory named
``config.yaml``. Once the file is created, open the file and add the following lines according to your preference -

.. code-block:: yaml

   ---
   dnac:
     host: sandboxdnac.cisco.com
     username: <username>
     password: <secret_password>

**Linux/MacOS**

- Open a terminal and ``cd`` into the home directory or any other directory form the above dependency list.
- Run ``mkdir -p .dnac_pnp/{catalog, configs}``
- Run ``cd .dnac_pnp/configs/``
- Run ``nano config.yaml``
- Add the above lines into the file and save it

Bulk Import Dependency
----------------------

While importing in bulk, a device catalog file can be put inside the ``catalog`` folder under ``.dnac_pnp`` with
``DeviceImport.csv`` name at the program will automatically read this file.

**Windows**

.. code-block:: batch

   .dnac_pnp\catalog\DeviceImport.csv

**Linux/MacOS**

.. code-block:: shell

   .dnac_pnp/catalog/DeviceImport.csv

**Note**

Samples files are available, in the ``data`` directory of this repo.
The location of the catalog file can be provided with ``-f`` flag also

Usage
-----

Installing Virtual Environment
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

It is highly recommended to use ``virtual environment`` for this package. To know how to setup
the virtual environment please visit `this page <https://virtualenv.pypa.io/en/stable/installation/>`_.

Installing the package
^^^^^^^^^^^^^^^^^^^^^^

Once you have virtual environment installed, clone this repository and move into the ``root``
directory of the project.

Now, crate a virtual environment.

.. code-block:: shell

   virtualenv --always-copy -p python3 venv

activate virtual environment -

**Linux/MacOS**

.. code-block:: shell

   source venv/bin/activate

**Windows**

.. code-block:: batch

   venv\Scripts\activate.bat

Once the ``virtual environment`` is active, run the following command -

.. code-block:: shell

   pip install .

Once the installation is finished, check out all the available options with -

.. code-block:: shell

   dnac_pnp --help

This should give an output like below -

.. code-block:: batch

   (venv) C:\Users\user.name\folder\dnac-pnp>dnac_pnp --help
   Usage: dnac_pnp [OPTIONS] COMMAND [ARGS]...

   Mission control module

   Options:
     --debug    Turns on DEBUG mode.  [default: False]
     --version  Show the version and exit.
     --help     Show this message and exit.

   Commands:
     acclaim-devices  Add and claim single or multiple devices.
     add-sites        Add one or more sites.
     delete-devices   Delete single or multiple devices.
     pkg-info         Shows package information.
     show             Shows DNA center component information.

To see the individual options for any of the ``commands`` use ``--help``
flag after the command.

.. code-block:: batch

   (venv) C:\Users\user.name\folder\dnac-pnp>dnac_pnp acclaim-in-bulk --help


**To use this package without any errors/bugs please always activate the virtual environment first**

To deactivate virtual environment use -

.. code-block:: shell

   deactivate


Credits
-------

See `AUTHORS.rst <AUTHORS.rst>`_

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
