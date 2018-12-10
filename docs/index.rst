.. smartva-dhis2 documentation master file, created by
   sphinx-quickstart on Fri Apr 20 12:15:30 2018.

smartva-dhis2
==============

|Build| |BuildWin| |Coverage|

A Python package for the integration of Verbal Autopsy data into DHIS2.

It downloads `ODK <https://opendatakit.org>`_ Aggregate records via ODK Briefcase,
runs the `SmartVA / Tariff 2.0 <http://www.healthdata.org/verbal-autopsy/tools>`_ algorithm to determine the most probable Cause of Death,
transforms it to a DHIS2-compatible Program Event and posts it to DHIS2.
Any data validation errors or DHIS2 import errors are written to a local SQLite database
which can be queried via the command line and exported to various formats.

It also checks DHIS2 for duplicate events (by Study ID Number) before posting
and auto-assigns organisation units to the program.

- Documentation: `smartva-dhis2.readthedocs.io <https://smartva-dhis2.readthedocs.io>`_
- Github: `github.com/D4H-VA/smartva-dhis2 <https://github.com/D4H-VA/smartva-dhis2>`_
- Virtual Machine Demo: `Ubuntu 16.04 LTS image <https://drive.google.com/file/d/1fuYLobncdWuGyG29DX1w_htRLiiuL7To/view>`_


To transfer events to a target DHIS2 (e.g. a Ministry of Health DHIS2), see :doc:`/data_transfer`.

.. toctree::
   :maxdepth: 2
   :caption: Contents

   DHIS2 configuration <config_dhis2>
   Installation <installation>
   App configuration <config_application>
   Local database <local_database>
   DHIS2 to DHIS2 transfer <data_transfer>
   Components <components>
   Development <development>
   Changelog <changelog>


Links
------

- `CRVS Knowledge Gateway <https://crvsgateway.info>`_
- `DHIS 2 <https://www.dhis2.org>`_
- `IHME / SmartVA <http://www.healthdata.org/verbal-autopsy/tools>`_
- `SmartVA-Analyze <https://github.com/ihmeuw/SmartVA-Analyze>`_



.. |Build| image:: https://travis-ci.org/D4H-VA/smartva-dhis2.svg?branch=master
   :target: https://travis-ci.org/D4H-VA/smartva-dhis2

.. |BuildWin| image:: https://ci.appveyor.com/api/projects/status/jn7ydwsd7ndq4e57/branch/master?svg=true
   :target: https://ci.appveyor.com/project/d4h-va/smartva-dhis2

.. |Coverage| image:: https://coveralls.io/repos/github/D4H-VA/smartva-dhis2/badge.svg?branch=master
   :target: https://coveralls.io/github/D4H-VA/smartva-dhis2?branch=master


