Installation
------------

.. note:: It is *highly recommended* to test the whole configuration part including running over a period of time
 on a development/test server before implementing it in production.

Use `pipenv <https://docs.pipenv.org>`_ (the recommended wrapper for virtualenvs and pip) to install this package.
It depends on Python 3.5+ and various packages as described in ``Pipfile`` and DHIS2 2.28 as for now.

Libraries included:

- Briefcase version: 1.10.1 Production (see `ODK Github <https://github.com/opendatakit/briefcase/releases>`_)
- smartva: SmartVA-Analyze, version 2.0.0

System requirements:

- Min. 2GB RAM
- Min. 2 CPUs

Ubuntu installation (tested with 16.04 LTS)


.. code:: bash

    sudo apt update
    sudo apt install python3

.. code:: bash

    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    sudo python3 get-pip.py

See here for further details
https://pip.pypa.io/en/stable/installing/

.. code:: bash

    (As a non-root user)
    pip3 install pipenv --user
    git clone --depth=1 https://github.com/D4H-VA/smartva-dhis2
    cd smartva-dhis2
    pipenv install --ignore-pipfile --deploy

Run
^^^^

Refer to the configuration pages first before running it:

1. :doc:`/config_dhis2`
2. :doc:`/config_application`

.. code:: bash

    cd ~/smartva-dhis2   (adjust to path where you cloned the repository)
    pipenv run smartva-dhis2 [--options]

Options are:

::

    --manual              Skip download of ODK aggregate file, provide local file path instead
    --all                 Pull ALL briefcases instead of relative time window


**If you do not provide any argument**, it will attempt to import ODK Aggregate records from last week (today minus 7 days).
e.g. if today is ``2018-04-08`` it attempts to download records for ``2018-04-01:00:00:00`` to ``2018-04-01:23:59:59``.

This is scheduled to run every three hours (leading to messages that the record is already in DHIS2)
but then it's expected.

.. note:: This application builds on the fact that *Study ID numbers* (SID) are **always unique** and **not modified
 in DHIS2 after the import**.


Tests
^^^^^^

To run tests:

.. code:: bash

    pipenv install --dev
    pipenv run python setup.py test

Deployment
^^^^^^^^^^^

Make sure the script is running even after server reboots - how this is achieved depends on the Operating System.
For systemd-based Operating Systems, you can install the following service.

::

    [Unit]
    Description=smartva-dhis2
    After=multi-user.target

    [Service]
    Type=simple
    Restart=always
    User=ubuntu
    WorkingDirectory=~/smartva-dhis2
    ExecStart=~/.local/bin/pipenv run smartva-dhis2

    [Install]
    WantedBy=multi-user.target


- Adjust ``~/smartva-dhis2`` to where you've installed the repository
- Adjust the path to ``pipenv`` - you can find out the path by calling ``which pipenv``.
- Adjust the ``ubuntu`` user to the user that runs the script
- ``~`` means *expanding to the home folder of the user as specified in* ``User=``.

Systemd service installation on Ubuntu:

.. code:: bash

    sudo nano /etc/systemd/system/smartva-dhis2.service
    (adjust and paste above config)
    sudo systemctl enable smartva-dhis2.service
    sudo systemctl start smartva-dhis2.service

    (to see the status of the service:)
    sudo systemctl start smartva-dhis2.service

    (check log files:)
    tail -f smartva_dhis2.log
