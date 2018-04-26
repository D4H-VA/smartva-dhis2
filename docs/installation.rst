Installation
------------

It is *highly recommended* to install this on a development/test server before running it in production.

Use `pipenv <https://docs.pipenv.org>`_ (the recommended wrapper for virtualenvs and pip) to install this package.
It depends on Python 3.5+ and various packages as described in ``Pipfile``.

- Briefcase version: 1.10.1 Production (see `ODK Github <https://github.com/opendatakit/briefcase/releases>`_)
- smartva: SmartVA-Analyze, version 2.0.0-a8

.. code:: bash

    pipenv install smartva-dhis2

Then, to run the application, invoke:

.. code:: bash

    smartva-dhis2

Optional but exclusive arguments:

::

    --manual              Skip download of ODK aggregate file, provide local file path instead
    --all                 Pull ALL briefcases instead of relative time window


If you do not provide any argument, it will attempt to import ODK aggregate records from last week (today minus 7 days).
e.g. if today is ``2018-04-08`` it attempts to download records for ``2018-04-01:00:00:00`` to ``2018-04-01:23:59:59``.

This is scheduled to run every three hours (leading to messages that the record is already in DHIS2)
but then it's expected.

Deployment
^^^^^^^^^^^

Make sure the script is running even after server reboots. This depends on the Operating System.

For systemd-based Operating Systems, you can install this service (adjust ``/path/to/repo``)

::

    [Unit]
    Description=smartva-dhis2
    After=multi-user.target

    [Service]
    Type=simple
    Restart=always
    WorkingDirectory=/path/to/repo
    ExecStart=/usr/local/bin/pipenv run python -m smartvadhis2

    [Install]
    WantedBy=multi-user.target


To run tests:

.. code:: bash

    pipenv run python setup.py test