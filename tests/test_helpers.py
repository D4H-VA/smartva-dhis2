import datetime
import os

import pytest

from smartvadhis2.core.helpers import (
    sanitize,
    is_uid,
    get_timewindow,
    csv_with_content,
    years_to_days,
    read_csv
)

from smartvadhis2.core.config import Config


def test_sanitize():
    data = {
        'one': 'data1',
        'two': 'data2 ',
        'three': ' data3',
        'four': 4
    }

    assert sanitize(data, 'one') == 'data1'
    assert sanitize(data, 'two') == 'data2'
    assert sanitize(data, 'three') == 'data3'
    with pytest.raises(AttributeError):
        sanitize(data, 'four')


def test_is_uid():
    uid = 'ZkJMgwNtihH'
    assert is_uid(uid)

    uid = 'ZkJMgwNtihH '
    assert not is_uid(uid)

    uid = 'not a uid'
    assert not is_uid(uid)

    uid = 'ZkJMgwNtihHZkJMgwNtihH'
    assert not is_uid(uid)

    uid = 'ZkJMgwNtih'
    assert not is_uid(uid)


FAKE_NOW = datetime.datetime(2018, 4, 16)


@pytest.fixture
def faked_now(monkeypatch):
    class MyDatetime:
        @classmethod
        def now(cls):
            return FAKE_NOW

    monkeypatch.setattr(datetime, 'datetime', MyDatetime)


def test_get_timewindow(faked_now):
    now = datetime.datetime.now()
    assert now == FAKE_NOW
    start, end = get_timewindow()
    assert start == '2018/04/09'
    assert end == '2018/04/09'


def file_testdata(filename):
    return os.path.join(Config.ROOT_DIR, 'tests', 'testdata', filename)


def test_csv_with_content_not_found():
    assert csv_with_content('notexisting.csv') is False


def test_csv_with_content_valid():
    data = file_testdata('briefcase_valid.csv')
    assert os.path.exists(data)
    assert csv_with_content(data) is True


def test_csv_with_content_exists_but_empty():
    data = file_testdata('briefcase_empty.csv')
    assert os.path.exists(data)
    assert csv_with_content(data) is False


def test_csv_with_content_headers_only():
    data = file_testdata('briefcase_headers_only.csv')
    assert os.path.exists(data)
    assert csv_with_content(data) is False


@pytest.mark.parametrize("years, expected", [
    (0.01, 3.652425),
    (1, 365.2425),
    (10, 3652.425)
])
def test_years_to_days(years, expected):
    assert years_to_days(years) == expected


def test_read_csv():
    data = file_testdata('smartva_test.csv')
    assert os.path.exists(data)

    expected = [
        {
            "sid": "VA_12342215225123456",
            "national_id": "54",
            "name": "A amin",
            "name2": "Darth Vader",
            "surname": "Skywalker",
            "surname2": "",
            "geography1": "u7T5N81y4aU",
            "geography2": "bb3Zld3B8z0",
            "geography3": "MJ0S8In5PIQ",
            "geography4": "VVS7SuCWYRI",
            "geography5": "GSGNlW5McFb",
            "cause34": "Homicide",
            "cause list #": "16",
            "icd10": "Y09",
            "age": "48 years",
            "sex": "1",
            "birth_date": "",
            "death_date": "",
            "interview_date": "Mar 26, 2018"
        },
        {
            "sid": "VA_12342212222123456",
            "national_id": "20202020",
            "name": "Joan",
            "name2": "Of",
            "surname": "Ark",
            "surname2": "",
            "geography1": "PHa5gf2nadH",
            "geography2": "TdsPHReXCYD",
            "geography3": "wrGMB1SnYGR",
            "geography4": "V1UEigOLUev",
            "geography5": "HO5HagDSmnY",
            "cause34": "Diabetes",
            "cause list #": "9",
            "icd10": "E14",
            "age": "82 years",
            "sex": "2",
            "birth_date": "1933-01-01",
            "death_date": "2016-01-01",
            "interview_date": "Mar 26, 2018"
        },
        {
            "sid": "VA_19752212222123456",
            "national_id": "101010",
            "name": "Han",
            "name2": "",
            "surname": "Solo",
            "surname2": "",
            "geography1": "cKuLAesQuzV",
            "geography2": "drvOPxQmmSO",
            "geography3": "UatIDzyz41i",
            "geography4": "gJ5eerA6za7",
            "geography5": "PSoRVLwvNbB",
            "cause34": "Congenital malformation",
            "cause list #": "2",
            "icd10": "Q89",
            "age": "10 days",
            "sex": "1",
            "birth_date": "",
            "death_date": "",
            "interview_date": "Mar 26, 2018"
        }
    ]
    for i, row in enumerate(read_csv(data)):
        for key in row.keys():
            assert row.get(key, None) == expected[i][key]
