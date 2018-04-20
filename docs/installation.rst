Installation
------------

Use `pipenv <https://docs.pipenv.org>`_ (the recommended wrapper for virtualenvs and pip) to install this package.
It depends on Python 3.5+ and various packages as described in ``Pipfile``.


.. code:: bash

    pipenv install smartva-dhis2

Run
----

.. code:: bash

    pipenv run python -m smartvadhis2


Optional arguments (can't use both at the same time)::

    --briefcase           Skip download of briefcase file, provide local file path instead
    --all                 Pull ALL briefcases instead of relative time window (e.g. yesterday's)

Test
-----

It is advised to run test before running on your server.

To run tests:

.. code:: bash

    pipenv run python setup.py test