smartva-dhis2
=============

|Build| |BuildWin| |Coverage|

A Python package for the integration of Verbal Autopsy data into DHIS2.

Documentation: `smartva-dhis2.readthedocs.io <https://smartva-dhis2.readthedocs.io>`_

Virtual Machine Demo: `Ubuntu 16.04 LTS image <https://drive.google.com/file/d/1fuYLobncdWuGyG29DX1w_htRLiiuL7To/view>`_

It downloads `ODK <https://opendatakit.org>`_ Aggregate records via ODK Briefcase,
runs the `SmartVA / Tariff 2.0 <http://www.healthdata.org/verbal-autopsy/tools>`_ algorithm to determine the most probable Cause of Death,
transforms it to a DHIS2-compatible Program Event and posts it to DHIS2.
Any data validation errors or DHIS2 import errors are written to a local SQLite database
which can be queried via the command line and exported to various formats.

It also checks DHIS2 for duplicate events (by Study ID Number) before posting
and auto-assigns organisation units to the program.

SmartVA Source Code: https://github.com/ihmeuw/SmartVA-Analyze

Licence: MIT

.. |Build| image:: https://travis-ci.org/D4H-VA/smartva-dhis2.svg?branch=master
   :target: https://travis-ci.org/D4H-VA/smartva-dhis2

.. |BuildWin| image:: https://ci.appveyor.com/api/projects/status/jn7ydwsd7ndq4e57/branch/master?svg=true
   :target: https://ci.appveyor.com/project/d4h-va/smartva-dhis2

.. |Coverage| image:: https://coveralls.io/repos/github/D4H-VA/smartva-dhis2/badge.svg?branch=master
   :target: https://coveralls.io/github/D4H-VA/smartva-dhis2?branch=master
