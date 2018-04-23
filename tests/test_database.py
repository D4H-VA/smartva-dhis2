import os

import pytest
from sqlalchemy.orm import Session

from smartvadhis2.core.config import DatabaseConfig, Config
from smartvadhis2.core.exceptions import db_exceptions
from smartvadhis2.core.models import *

db_url = os.path.join(Config.ROOT_DIR, 'tests', DatabaseConfig.db_name.replace('.db', '') + '_test.db')


@pytest.fixture(scope='session')
def engine():
    yield create_engine('sqlite:///' + db_url)
    os.remove(db_url)


@pytest.fixture(scope='session')
def tables(engine):
    Person.__table__.create(bind=engine, checkfirst=True)
    Failure.__table__.create(bind=engine, checkfirst=True)
    PersonFailure.__table__.create(bind=engine, checkfirst=True)
    yield


@pytest.fixture
def dbsession(engine, tables):
    connection = engine.connect()
    # begin the nested transaction
    transaction = connection.begin()
    # use the connection with the already started transaction
    session = Session(bind=connection)

    yield session

    session.close()
    # roll back the broader transaction
    transaction.rollback()
    # put back the connection to the connection pool
    connection.close()


def test_add_person(dbsession):
    person1 = Person(first_name="test")
    dbsession.add(person1)
    dbsession.commit()
    assert person1.personid == 1

    person2 = Person(first_name="test2")
    dbsession.add(person2)
    dbsession.commit()
    assert person2.personid == 2


def test_add_person_realdata(dbsession):
    person = Person(age='22 years',
                    birth_date='',
                    cause_code='',
                    cause_of_death='',
                    first_name='',
                    first_name_2nd='',
                    interview_date='2018-02-01',
                    orgunit='',
                    surname='',
                    surname_2nd='',
                    icd10='',
                    sex='',
                    sid='',
                    national_id='',
                    algorithm_version='',
                    questionnaire_version='')

    dbsession.add(person)
    dbsession.commit()
    assert person.age == '22 years'
    assert person.interview_date == '2018-02-01'
    assert isinstance(person.created, datetime)


def test_add_failure_categories(dbsession):
    failure_types = [
        {
            "failureid": err.code,
            "failuretype": err.err_type,
            "failuredescription": err.message
        }
        for err in db_exceptions
    ]

    f = [Failure(**failure) for failure in failure_types]
    dbsession.add_all(f)
    dbsession.commit()

    assert dbsession.query(Failure.failureid).count() == len(db_exceptions)