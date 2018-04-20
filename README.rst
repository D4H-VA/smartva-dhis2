smartvadhis2
=============

A Python package that downloads ODK Briefcases, runs the SmartVA / Tariff 2.0 algorithm to find the most probable Cause of Death, transforms it to a DHIS2-compatible Program Event and posts it to DHIS2.
Any data validation errors or DHIS2 import errors are written to a local SQLite database.

Documentation: `smartva-dhis2.readthedocs.io <https://smartva-dhis2.readthedocs.io>`_

Licence
--------

MIT

The library that creates the most probable Cause of Death based from Briefcase records (``smartvadhis2/lib/smartva``) i
s a closed-source binary packaged by *The Institute for Health Metrics and Evaluation (IHME)* and is **excluded** from above licence.
See `here <http://www.healthdata.org/verbal-autopsy/tools>`_ for more details.