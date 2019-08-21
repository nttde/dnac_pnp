Tutorials
=========

.. tip::

   Always remember, when in doubt use ``--help``.

Getting help
------------
To see the options use ``--help`` flag after the command.

.. code-block:: batch

   (venv) C:\Users\user.name\folder\dnac-pnp>dnac_pnp --help

This should output the help information on screen and it
looks something similar as below -

.. code-block:: batch

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

To checkout individual options for any command use ``--help`` flag.

.. code-block:: batch

   dnac_pnp info --help

This command should show all the available ``arguments`` for ``info``
sub-command.

.. code-block:: batch

   Usage: dnac_pnp info [OPTIONS]

   This module prints information about the package

   Options:
     --all   Shows full information.  [default: False]
     --help  Show this message and exit.

Turning on debug
----------------

Sometimes program runs into ERROR and there are not enough data shown
on screen to determine the cause of the ERROR. For getting ``verbose`` output
of all the actions done by the program simply ``turn on`` the ``debug`` mode
with ``--debug`` flag. By default it's turned off.

To turn on ``debug`` mode -

.. code-block:: batch

   dnac_pnp --debug acclaim-one [here goes other arguments]

Also you can turn on the ``debug`` mode at sub-command level by using ``--debug``
flag after the sub-command

.. code-block:: batch

   dnac_pnp acclaim-one [here goes other arguments] --debug

OR like this -

.. code-block:: batch

    dnac_pnp acclaim-one --debug [here goes other arguments]

Acclaim (add + claim) one device
--------------------------------

To add and claim one single device use the ``acclaim-one`` sub-command. ``--help``
will guide through the required arguments.

At the time of writing this documentation, version 0.3.1 looked something similar
like below -

.. code-block:: batch

   Usage: dnac_pnp acclaim-one [OPTIONS]

   This module is the entry-point for single device add and claim

   Options:
     -s, --serial-number TEXT  Serial number of the device.  [required]
     -p, --product-id TEXT     Product ID of the device. (e.g. Cisco2690)
                            [required]
     -b, --site-name TEXT      Site name with full hierarchy.  [required]
     -h, --host-name TEXT      hostname of the device [if not provided, serial
                            number will be used].
     --debug                   Turns on DEBUG mode.  [default: False]
     --help                    Show this message and exit.

So from the above output we can see that a few fields are required and some are
not. So the required fields must be provided in order to start the execution
of the program.

.. warning::

   Please take note that all the input's are validated at a primary level before
   execution starts.

Options explained
^^^^^^^^^^^^^^^^^

- ``-s`` or ``--serial-number`` should be a valid serial number. Serial number
must be 11 character (alphanumeric - letters and digits) in length or less.

- ``-p`` or ``--product-id`` should be the correct product ID according to the
device. Take a look into DNA Center itself to know the proper Product ID. Product
ID must also be alphanumeric and must not contain any special characters. Only
allowed special characters are ``dash/hyphen(-)`` and  ``underscore(_)``

- ``-b`` or ``--site-name`` should mention a valid site that is available in DNA
center. ``-b`` elaborates to ``building`` in general, if you are wondering why
it's ``-b``

- ``-h`` or ``--host-name`` represents the name of the device shown on DNA Center.
If not provide, ``serial number`` is used to create an unique hostname. if
provided, must be unique.

- ``--debug`` turns on the debug mode

- ``--help`` rescues you from wasting time using inappropriate options.



