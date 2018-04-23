Configuration
==============


DHIS2 metadata
--------------

All metadata in DHIS2 is required to be configured before running this application.

*Note:* the Organisation Unit hierarchy in DHIS2 should be aligned with the VA Questionnaire.
This application assumes it is set up correctly (however it auto-assigns the Organisation Unit to the program if not already assigned).

In order to install metadata, import the the following metadata files with DHIS2's Import/Export app.
Always do a "Dry run" first.


1. Import ``metadata/optionset_age_category.csv``
2. Import ``metadata/optionset_cause_of_death.csv``
3. Import ``metadata/optionset_ICD10.csv``
4. Import ``metadata/optionset_sex.csv``
5. Import ``metadata/dataelements.csv``
6. Import ``metadata/program.json``
7. Import ``metadata/dashboard.json`` TODO

Application
------------

All configuration is defined in ``config.ini``. Note that there are no apostrophes (``"`` or ``'``) in this file.

yyy

For further mapping details see also the ``smartva/core/mapping.py`` module.