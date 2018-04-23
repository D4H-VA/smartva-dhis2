Installation
------------

It is *highly recommended* to install this on a development/test server before running it in production.

Use `pipenv <https://docs.pipenv.org>`_ (the recommended wrapper for virtualenvs and pip) to install this package.
It depends on Python 3.5+ and various packages as described in ``Pipfile``.

- Briefcase version: 1.9.0 Production
- smartva: SmartVA-Analyze, version 2.0.0-a6

.. code:: bash

    pipenv install smartva-dhis2

Then, to run the application, invoke:

.. code:: bash

    pipenv run python -m smartvadhis2

Optional arguments (can't use both at the same time)

::

    --briefcase           Skip download of ODK aggregate file, provide local file path instead
    --all                 Pull ALL briefcases instead of relative time window


If you do not provide any argument, it will attempt to import ODK aggregate records in a sliding time window, where

::

    start_date = today minus 1 week
    end_date = start_date + 1 day

e.g. if today is 2018-04-08 it will pass 2018-04-01 -> 2018-04-02 as arguments to ODK Briefcase.

**Deployment & scheduling**
TODO


To run tests:

.. code:: bash

    pipenv run python setup.py test