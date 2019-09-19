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

   CISCO DNA Center PnP automation control panel

   Options:
     --debug    Turns on DEBUG mode.  [default: False]
     --version  Show the version and exit.
     --help     Show this message and exit.

   Commands:
     acclaim-devices    Add and claim single or multiple devices.
     add-sites          Add one or more sites.
     delete-devices     Delete single or multiple devices.
     pkg-info           Shows package information.
     show               Shows DNA center component information.

To checkout individual options for any command use ``--help`` flag.

.. code-block:: batch

   dnac_pnp info --help

This command should show all the available ``arguments`` for ``info``
sub-command.

.. code-block:: batch

   Usage: dnac_pnp pkg-info [OPTIONS]

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

Acclaim (add + claim) one device [Test Purpose Only]
----------------------------------------------------

.. warning::

   Does not support ``day0 template`` configurations

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

Acclaim (add+claim) in bulk
---------------------------

Adding and claiming one single device at a time is not very efficient while there are
couple hundred or thousand devices to add. ``acclaim-in-bulk`` is there to do just
that. It does what the command says, adds and claims one or multiple devices.

let's look at the options for this sub-command with ``--help`` flag.

.. code-block:: batch

   dnac_pnp acclaim-in-bulk --help

This should present all possible options on screen. Something similar as below -

.. code-block:: batch

   Usage: dnac_pnp acclaim-in-bulk [OPTIONS]

   Add and claim multiple devices

   Options:
     -f, --catalog-file FILE  Device catalog full file path
     --debug                  Turns on DEBUG mode.  [default: False]
     --help                   Show this message and exit.

From this output, we can see that there are no required options, all of them are
``optional``.

.. note::

   All the options are ``optional``.

So how does this work? Remember while installing, we talked about
``bulk import dependency``? If ``-f`` or ``--catalog-file`` is not provided,
the program will look for a file called ``DeviceImport.csv`` in following directories -

.. note::

   Directories are listed from highest to lowest priority order.

1. <user_home_directory>/.<package_name>/catalog/config.yaml (``Window/Linux/MacOS``)
2. <current_working_directory>/.<package_name>/catalog/config.yaml (``Windows/Linux/MacOS``)
3. /etc/<package_name>/catalog/config.yaml (``Linux/MacOS``)

If there is no file named ``DeviceImport.csv`` in any of these locations and ``-f`` flag
is not provided, the program will stop and exit.

.. warning::

   Program will only take into account the first file that it finds.

So, what if you don't want to put the file into one of these directories and certainly
you don't want to name your file ``DeviceImport.csv`` ?

Here comes the ``-f`` or ``--catalog-file`` in rescue, you can point to a properly
formatted csv file form anywhere in the file system with this flag and the program will
look only to that file and carry on.

.. note::

   The argument to ``-f`` flag must be a valid file path. The program pre-checks for
   validity and read permission of the file and also the extension. Only valid extension
   is ``.csv``

Example csv file content
^^^^^^^^^^^^^^^^^^^^^^^^

A well formatted CSV should look something like below -

.. code-block:: shell

   serial_number, pid, site_name, name, template_name, host_name, vtp_domain, vtp_version
   FOC2246T582, WS-C3560CX-8PC-S, Global/DD Germany/DD MUC, pnp-test-sw01, Onboarding Configuration/Test-Day0-Template, switch001, vtp001, 1
   FOC1849Z2JL, WSC2960C, Global/Demo_DE/B1/F3, MainRouter, Onboarding Configuration/Test-Day0-Template, switch001, vtp001, 1
   AAA1111K3MX, C891FK9, Global/Demo_DE/B1/F35, HallwaySwitch, Onboarding Configuration/Test-Day0-Template, switch001, vtp001, 1
   FOC1849Z2KK, WSC2960C, Global/Demo_DE/B1/F3, MainRouter2, Onboarding Configuration/Test-Day0-Template, switch001, vtp001, 1

.. danger::

   DO NOT USE ``camelCased`` headers or ``unicode`` characters in the headers

Add Sites
---------

Adding site designs are handled by the sub-command ``add-sites``. With the help of
this sub command we can add one or multiple sites (area/building/floor).

.. code-block:: shell

   dnac_pnp add-sites -l ..\..\sites-config.yaml

This should check the input and create the sites listed in the ``sies-config.yaml``
file.

.. warning::

   While creating sites, ``parent site`` (referred by ``parentName``) **MUST** be
   present.

A sample ``sites-config.yaml`` -

.. code-block:: yaml

   ---
   sites:
     - EU-WEST:
         type: area
         name: EU-WEST
         parentName: Global
     - FRA:
         type: area
         name: FRA
         parentName: Global/EU-WEST
     - DH:
         type: area
         name: DH
         parentName: Global/EU-WEST/FRA
     - HQ:
         type: building
         parentName: Global/EU-WEST/FRA/DH
         name: HQ
         latitude: 50.219202
         longitude: 8.622795
         address: Horexstr 7
     - F1:
         type: floor
         name: F1
         parentName: Global/EU-WEST/FRA/DH/HQ
         rfModel: Cubes And Walled Offices
         length: 20
         width: 15
         height: 8

.. note::

   If the site (area/building/floor) already exists then it will NOT be over written

Delete from PnP
---------------

Once we have added some devices, it might be necessary that we need to delete
some of the devices from the PnP (Plug and Play) of DNA center.

The program can delete one or more devices from PnP with ``delete``
sub-command.

As usual, let's take a look at the ``--help`` section of this sub-command.

.. code-block:: batch

   Usage: dnac_pnp delete [OPTIONS]

   Delete one or multiple devices

   Options:
     -d, --delete-from [pnp|inv]  Delete device from PnP or Inventory.
                               [required]
     -s, --serial-numbers TEXT    Comma separated serial numbers.
     -f, --delete-file FILE       Device delete full file path.
     --dry-run                    Dry runs the process.  [default: False]
     --debug                      Turns on DEBUG mode.  [default: False]
     --help                       Show this message and exit.

Options explained
^^^^^^^^^^^^^^^^^

- ``-d`` or ``--delete-from`` is a ``required`` option, this determines
  from where the devices associated with the provided serial numbers will
  be deleted. Only to valid choices for this option ``pnp`` which stands
  for ``plug and play`` and ``inv`` which elaborates to ``inventory``.

- ``-s`` or ``--serial-number`` is a list of comma separated serial numbers.
  The idea behind this option is to have the flexibility to delete one or
  more devices from the commandline.

  .. note::

     Serial numbers must be in comma separated format. e.g. xxxxx, yyyy etc.
     and all the serial number should be valid serial with 11 character or
     less in length

- ``-f`` or ``--delete-file`` is a full file path to a (preferably ``.txt``)
  file with serial numbers that needs to be deleted. One serial number per
  line. A sample ``delete_device.txt`` looks like below

  .. code-block:: ini

     FOC1849Z2JL
     AAA1111K3MX
     FOC1849Z2KK

  .. warning::

     Please do not put any header in ``delete`` file

- ``--dry-run`` does exactly what it says. It will only show what will be
  deleted and from where.

- ``--debug`` turns on the debug mode.

- ``--help`` shows the help options and saves the day.


Displaying DNA Center Components
--------------------------------

To display components like ``pnp`` devices or ``templates`` this software package
provides an option named ``show``. Use ``--help`` to see all the available options.

.. code-block:: shell

   dnac_pnp show --help

This should output something like below -

.. code-block:: shell

   Usage: dnac_pnp show [OPTIONS]

   Shows DNA Center component information

   Options:
     --all-locations    Shows all available site locations.  [default: False]
     --all-pnp-devices  Shows all devices in PnP.  [default: False]
     --pnp-device TEXT  Shows [pnp] device information by serial number.
     --all-templates    Lists all available templates.  [default: False]
     --template TEXT    Shows template information by full template name
     --export-pnp FILE  Exports PnP device information to CSV
     --debug            Turns on DEBUG mode.  [default: False]
     --help             Show this message and exit.

Options explained
^^^^^^^^^^^^^^^^^

- ``--all-locations`` lists all available sites/building/floors from DNA
  center
- ``--all-pnp-devices`` Lists and shows all the devices listed under pnp tab in DNA
  center. Display limit is set to ``100`` devices.
- ``--pnp-device`` shows details about a particular device based on serial number
  provided as an argument
- ``--all-templates`` shows all available templates with their project names.
- ``--template`` requires an argument of ``full template name``
  [project_name/template_name] and shows the body of the template and variables
- ``--export-pnp`` allows user to export all the listed devices under PnP tab in DNA
  center. Export limit is also bound to display limit, which is currently set to ``100``
