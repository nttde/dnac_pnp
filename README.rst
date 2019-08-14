========
dnac-pnp
========

Cisco DNA center device claim and delete functionalities


Features
--------

* ``Git`` alike commandline user interface
* Define user credentials and host for DNAC
* Read configurations from file
* Configurations file lookup in 3 default locations
* Pre-checks user inputs
* Pre-checks csv file for bulk import (add+claim)
* Pre-checks txt file for bulk delete
* Single import of device
* Bulk import from csv
* Single device deletion
* Bulk delete from txt file
* Pre-checks for valid sites
* Pre-checks for device status
* Decision based on site status and device status

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

Windows system by default doesn't let you create ``.`` prefixed directory, so use the following -

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

.. note::

   Samples files are available, in the ``data`` directory of this repo.


the location of the catalog file can be provided with ``-f`` flag also

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
     acclaim-in-bulk  Add and claim multiple devices.
     acclaim-one      Add and claim a single device.
     delete           Delete [un-claim + remove] or more devices.
     info             Shows package information.

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
