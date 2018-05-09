DHIS2 configuration
====================

All metadata in DHIS2 is required to be configured before running this application.

This process will set up the VA module in the DHIS2 server. This module is required to be set up before VA data can be pushed to DHIS2.

.. note:: The Organisation Unit hierarchy in DHIS2 should be aligned with the VA Questionnaire.
          This application assumes it is set up correctly (however it auto-assigns the Organisation Unit to the program if not already assigned).

In order to install metadata, import the the following metadata files with DHIS2's Import/Export app.
Always do a "Dry run" first.

1. Import ``metadata/optionset_age_category.csv``
2. Import ``metadata/optionset_cause_of_death.csv``
3. Import ``metadata/optionset_ICD10.csv``
4. Import ``metadata/optionset_sex.csv``
5. Import ``metadata/dataelements.csv``
6. Import ``metadata/program.json``
7. (Import ``metadata/dashboard.json``)

Probably it is a good idea to create a dedicated ``verbal-autopsy-bot`` user account with at least the following access:

- the whole Organisation Unit hierarchy for both data capture and data analysis
- the User Role authority to send Events
- the User Role authority to access the program (read and write)
- the User Role *read* authority for all imported metadata

This has the advantage that the dedicated username shows up in DHIS 2 log files.