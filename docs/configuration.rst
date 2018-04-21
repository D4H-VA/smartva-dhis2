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

[auth]
^^^^^^

**auth_file**: A file path to where authentication details for DHIS2 and ODK Aggregate are stored - see ``dish.json`` for structure of the file.
Keep it on a secure place with correct access rights (e.g. ``chmod 0600 dish.json``).

[logging]
^^^^^^^^^^

**logfile**: Where the application should log to.
If there is no path (e.g. ``smartvadhis2.log``) it logs within the code repository.

**level**: Minimum Log level - e.g. ``INFO`` logs all info messages, warnings, errors.
Must be uppercase and one of: ``DEBUG``, ``INFO``, ``WARNINGS``

[database]
^^^^^^^^^^

**db_queries_log**: Whether to log all local database queries as well. Either ``true`` or ``false``.

**db_name**: Name of the local database file, e.g. ``smartvadhis2.db``

[odk]
^^^^^^

**dl_url**: ODK Briefcase JAR download URL, e.g. ``https://s3.amazonaws.com/opendatakit.downloads/ODK Briefcase v1.9.0 Production.jar``

**dl_sig**: Signature of the Briefcase JAR download (to verify the integrity of the JAR). If the Briefcase version changes, get the new signature from `opendatakit.org <https://opendatakit.org/wp-content/uploads/sha256_signatures.txt>`_.

**form_id**: Verbal Autopsy ODK Form ID, e.g. ``SmartVA_Bangla_v7``

**sid_regex**: Regular Expression that matches a to Verbal Autopsy Study ID number, e.g. ``^VA_[0-9]{17}$``.
Check regex with online tools, e.g. `regex101.com <https://regex101.com>`_.

[smartva]
^^^^^^^^^

**ignore_columns**: Which CSV columns in the SmartVA CSV output to ignore for further processing.
Must be delimited by commas ``,`` and without space, e.g. ``geography1,geography2,geography4,geography5,cause34``

**algorithm_version**: With which version the CoD was obtained, e.g. ``Tariff 2.0``. This is sent as a text attached to the DHIS2 Event.


[dhis]
^^^^^^
**program**: The Unique Identifier (UID) of the Verbal Autopsy DHIS2 program.

**program_stage**: The Unique Identifier (UID) of the Verbal Autopsy DHIS2 program *stage*.

**root_orgunit**: The Unique Identifier (UID) of the Top-Level Root Organisation Unit.
This is used to determine if there is a duplicate.


For further mapping details see also the ``smartva/core/mapping.py`` module.