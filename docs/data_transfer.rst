DHIS2 to DHIS2 Event data transfer
===================================

To migrate DHIS2 events from one instance to another DHIS2 instance, use the script located at
`github.com/D4H-VA/smartva-dhis2-data-transfer <https://github.com/D4H-VA/smartva-dhis2-data-transfer>`_.

Same as with the main application, it auto-assigns Organisation Units and avoids importing duplicates
by assuring that no event exists already with the same Study ID number (see ``study_id`` below).

DHIS2 configuration
--------------------

Metadata must be aligned with the setup as described in :doc:`/config_dhis2` - you can import the same files.

Installation
-------------

.. code:: bash

    sudo apt update
    sudo apt install python3
    sudo apt install python3-venv python3-pip

    (As a non-root user)
    pip3 install pipenv --user
    git clone --depth=1 https://github.com/D4H-VA/smartva-dhis2-data-transfer
    cd smartva-dhis2-data-transfer
    pipenv install --ignore-pipfile --deploy

Script configuration
----------------------

A similar ``config.ini`` file can be found in this repository.

**[auth]**

auth_file
    A file path to where authentication details for source and target DHIS2 is stored -
    see ``dish.json`` for structure of the file.
    Keep it on a secure place and refer to its file path.

**[dhis]**

program
    The Unique Identifier (UID) of the Verbal Autopsy DHIS2 program.

program_stage
    The Unique Identifier (UID) of the Verbal Autopsy DHIS2 program *stage*.

study_id
    The Unique Identifier (UID) of the Data Element of the Study ID number.
    Should probably be ``L370gG5pb3P`` - the same as in :doc:`/config_application`

attribute_category_option
    The Unique Identifier (UID) of the Category Option to store the events for.
    If no special requirements are in place, it should be the ``default`` UID -
    get the UID via ``<target-dhis2.org>/api/categoryOptions?filter=name:eq:default``.

attribute_option_combo
    The Unique Identifier (UID) of the Category Option Combination that holds above Category Option -
    get the UID via ``<target-dhis2.org>/api/categoryOptionCombos?filter=name:eq:default``.


Run
----

.. code:: bash

    cd ~/smartva-dhis2-data-transfer   (adjust to path where you cloned the repository)
    pipenv run python -m datatransfer --log=/path/to/logfile.log [--options]

Options are:

::

  --all                 Import all events of a program
  --from_date           Import events of a certain date



**If you do not provide any optional argument**, it will attempt to import **yesterday's** events.

.. note:: This application builds on the fact that *Study ID numbers* (SID) are **always unique** and **not modified
 in DHIS2 after the import**.


