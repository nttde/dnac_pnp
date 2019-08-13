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


**To use this package without any errors/bugs please alway activate the virtual environment first**

To deactivate virtual environment use -

.. code-block:: shell

   deactivate


Credits
-------

See `AUTHORS.rst <AUTHORS.rst>`_

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
