"""
import os

import pytest

from smartvadhis2.core.config import DatabaseConfig, Config
from smartvadhis2.core.database import Database
from smartvadhis2.core.exceptions import SmartVADHIS2Exception

db_url = os.path.join(Config.ROOT_DIR, 'tests', DatabaseConfig.db_name.replace('.db', '') + '_test.db')


@pytest.yield_fixture
def db():
    yield Database(db_url='sqlite:///{}'.format(db_url))
    os.remove(db_url)


def test_to_sql_rows(db):
    data = {
        'age': '22 years',
        'birth_date': None,
        'cause_code': None,
        'death_date': 'Unknown',
        'first_name': None,
        'first_name_2nd': None,
        'interview_date': '2018-02-01',
        'orgunit': None,
        'surname': None,
        'surname_2nd': None,
        'icd10': None,
        'sex': None,
        'sid': None,
        'national_id': None
    }
    assert db._to_sql_rows(data) == data


def test_to_sql_rows_not_aligned(db):
    data = {
        'age': '22 years'
    }
    with pytest.raises(SmartVADHIS2Exception):
        db._to_sql_rows(data)


def test_init_database(db):
    assert db.db_url == 'sqlite:///{}'.format(db_url)
    assert os.path.exists(db_url)
"""