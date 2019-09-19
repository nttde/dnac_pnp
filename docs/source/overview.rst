========
Overview
========

Cisco DNA center device claim and delete automation

Features
********

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
