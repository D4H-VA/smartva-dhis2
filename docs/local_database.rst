Local SQLite database
======================

A single database file as specified in ``config.ini`` is used.
The database includes three tables which gets only populated when something went wrong.

- ``person``: All details regarding a person record
- ``failure``: Categorization of import errors. It is automatically sourced from the code (see ``exceptions`` folder) upon database creation.
- ``person_failure``: The linking table between a person and a failure category. 

Check ``models.py`` for the database schema.

If there is ever a need to move to a full-blown DBMS (e.g. Postgres, Redshift) it is easy to switch since it relies on an ORM (Object-relational mapping) - namely `SQLAlchemy <https://www.sqlalchemy.org>`_

Querying and exporting
-----------------------

A command-line tool to query and export from the local database is included, intended for report-style exports.

Use the ``records`` command (check `kennethreitz/records <https://github.com/kennethreitz/records#-command-line-tool>`_ for details)

.. code:: bash

    pipenv run records 'select first_name, surname, cause_of_death from person' --url=sqlite:///db/smartvadhis2.db

would for example yield:

::

    first_name|surname  |cause_of_death
    ----------|---------|-----------------------
    A amin    |Skywalker|Homicide
    Joan      |Ark      |Diabetes
    Han       |Solo     |Congenital malformation


To export it as a CSV file:

.. code:: bash

    pipenv run records 'select sid, surname, cause_of_death from person' csv --url=sqlite:///db/smartvadhis2.db > export.csv


Supported export formats
-------------------------

csv, tsv, json, yaml, html, xls, xlsx, dbf, latex, ods


Schema migrations
------------------

Database schema migrations - if necessary - are facilitated by `Alembic <http://alembic.zzzcomputing.com/en/latest/tutorial.html>`_. Just run
``pipenv alembic init alembic`` and follow the instructions in the link.