Installation
============

Getting the package
-------------------
The current version of the release in (.tar.gz/.zip/.tar.bz2) format can always be found in
the release section of this project in SCM.

Here is the direct link to the releases section - 
`Releases <https://scm.dimensiondata.com/de-ps/digital-infrastructure/automation/carnival/dnac-pnp/-/releases>`_

Download preffered format and extract. Once that is done, move forward witht the dependency
management.

Dependencies
------------

This package requires a configuration file in either ``.yaml`` or ``yml`` format. The
look up priority for the configuration file is as following-

1. <user_home_directory>/.<package_name>/configs/config.yaml (``Window/Linux/MacOS``)
2. <current_working_directory>/.<package_name>/configs/config.yaml (``Windows/Linux/MacOS``)
3. /etc/<package_name>/configs/config.yaml (``Linux/MacOS``)

If ``config.yaml`` doesn't exists in one of these locations, the program will NOT run.
So, to create the configuration file, please use -

**Windows**

Windows system by default doesn't allow creation of ``.`` prefixed directory from GUI,
so use the following -

- Open `cmd` and change the directory to the ``home`` folder of the user
- Run ``mkdir .dnac_pnp``
- Run ``cd .dnac_pnp``
- Run ``mkdir configs``
- Run ``mkdir catalog``
- Run ``cd configs``

Now that the ``.`` prefixed directory is created, use the GUI to add a file in
``configs`` directory named ``config.yaml``. Once the file is created, open the file
and add the following lines according to your preference -

.. code-block:: yaml

   ---
   dnac:
     host: sandboxdnac.cisco.com
     username: <username>
     password: <secret_password>

**Linux/MacOS**

- Open a terminal and ``cd`` into the home directory or any other directory form the
  above dependency list.
- Run ``mkdir -p .dnac_pnp/{catalog, configs}``
- Run ``cd .dnac_pnp/configs/``
- Run ``nano config.yaml``
- Add the above lines into the file and save it

Bulk Import Dependency
----------------------

While importing in bulk, a device catalog file can be put inside the ``catalog``
folder under ``.dnac_pnp`` with ``DeviceImport.csv`` name at the program will
automatically read this file.

**Windows**

.. code-block:: batch

   .dnac_pnp\catalog\DeviceImport.csv

**Linux/MacOS**

.. code-block:: shell

   .dnac_pnp/catalog/DeviceImport.csv

.. note::

   Samples files are available, in the ``data`` directory of this repo.
   The location of the catalog file can be provided with ``-f`` flag also

Installation
------------

Installing Virtual Environment
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

It is highly recommended to use ``virtual environment`` for this package. To know how
to setup the virtual environment
please visit`this page <https://virtualenv.pypa.io/en/stable/installation/>`_.

Installing the package
^^^^^^^^^^^^^^^^^^^^^^

Once you have virtual environment installed, clone this repository and move into
the ``root`` directory of the project.

Now, crate a virtual environment.

.. code-block:: shell

   ~/dnac-pnp/$ virtualenv --always-copy -p python3 venv

.. code-block:: batch

   C:\Users\user.name\folder\dnac-pnp> virtualenv --always-copy -p python3 venv

activate virtual environment -

**Linux/MacOS**

.. code-block:: shell

   ~/dnac-pnp/$ source venv/bin/activate

**Windows**

.. code-block:: batch

   C:\Users\user.name\folder\dnac-pnp> venv\Scripts\activate.bat

Once the ``virtual environment`` is active, run the following command -

.. code-block:: shell

   pip install .

Once the installation is finished, check out all the available options with -

.. code-block:: shell

   dnac_pnp --version

This should give an output like below -

.. code-block:: batch

   (venv) C:\Users\user.name\folder\dnac-pnp>dnac_pnp --version
   dnac_pnp, version 0.2.5

**To use this package without any errors/bugs please always activate the virtual environment first**

To deactivate virtual environment use -

.. code-block:: shell

   deactivate
