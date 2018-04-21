Development
===========

- Install Python 3.5+
- Install ``pip``
- Install ``pipenv``
- Clone repository
- ``pipenv install --dev``

Testing
--------
``pytest`` is used for Unit testing.

.. code:: bash

    pipenv run python setup.py test

Releasing
----------
- To release a new pip installable package, run ``pipenv run python setup.py publish``.
- Use `Semantic Versioning <https://semver.org/spec/v2.0.0.html>`_:


        "Consider a version format of X.Y.Z (Major.Minor.Patch). Bug fixes not affecting the API increment the patch version,
        backwards compatible API additions/changes increment the minor version,
        and backwards incompatible API changes increment the major version."

        -- https://semver.org

Commandline interface
----------------------

- delete ALL events (asks first)
- export program metadata w/ dependencies


::

    pipenv run python smartvadhis2/cli.py --help
    usage:

    arguments:
      --delete_events               Delete all events
      --download_program_metadata   Download DHIS2 program metadata


Updating Documentation
-----------------------

- add RestructuredText files (like this one) to ``docs`` and link them in ``index.rst``
- ``pipenv shell``, then ``cd docs`` and finally ``make html``