import datetime
import os

import pytest

from smartvadhis2.core.helpers import (
    sanitize,
    is_uid,
    get_timewindow,
    is_non_zero_file,
    days_to_years,
    years_to_days,
    read_csv
)


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
    assert end == '2018/04/10'


def test_is_non_zero_file_not_exists():
    assert is_non_zero_file('notexisting.csv') is False


@pytest.fixture
def briefcase_empty():
    tmp_briefcase = 'briefcase_test.csv'
    with open(tmp_briefcase, 'w'):
        pass
    yield tmp_briefcase
    os.remove(tmp_briefcase)


def test_is_non_zero_file_exists_but_empty(briefcase_empty):
    assert is_non_zero_file(briefcase_empty) is False


@pytest.mark.parametrize("years, expected", [
    (1, 365),
    (10, 3652),
    (15, 5479)
])
def test_years_to_days(years, expected):
    assert years_to_days(years) == expected


@pytest.mark.parametrize("days, expected", [
    (365, 1),
    (3652, 10),
    (5479, 15)
])
def test_years_to_days(days, expected):
    assert days_to_years(days) == expected


@pytest.fixture
def test_data():
    s = '''sid,national_id,name,name2,surname,surname2,geography1,geography2,geography3,geography4,geography5,cause34,cause list #,icd10,age,sex,birth_date,death_date,interview_date
VA_12342215225123456,54,A amin,Darth Vader,Skywalker,,u7T5N81y4aU,bb3Zld3B8z0,MJ0S8In5PIQ,VVS7SuCWYRI,GSGNlW5McFb,Homicide,16,Y09,48 years,1,,,"Mar 26, 2018"
VA_12342212222123456,20202020,Joan,Of,Ark,,PHa5gf2nadH,TdsPHReXCYD,wrGMB1SnYGR,V1UEigOLUev,HO5HagDSmnY,Diabetes,9,E14,82 years,2,1933-01-01,2016-01-01,"Mar 26, 2018"
VA_19752212222123456,101010,Han,,Solo,,cKuLAesQuzV,drvOPxQmmSO,UatIDzyz41i,gJ5eerA6za7,PSoRVLwvNbB,Congenital malformation,2,Q89,10 days,1,,,"Mar 26, 2018"'''
    tmp_file = 'test_smartva_csv'
    with open(tmp_file, 'w') as f:
        f.write(s)
    yield tmp_file
    os.remove(tmp_file)


def test_read_csv(test_data):
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
    for i, row in enumerate(read_csv('test_smartva_csv')):
        for key in row.keys():
            assert row.get(key, None) == expected[i][key]
