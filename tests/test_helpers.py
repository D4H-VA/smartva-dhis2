import datetime
import os

import pytest

from smartvadhis2.core.helpers import (
    sanitize,
    is_uid,
    parse_args,
    get_timewindow,
    is_non_zero_file,
    days_to_years,
    years_to_days
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


@pytest.fixture
def briefcase():
    tmp_briefcase = 'briefcase_test.csv'
    with open(tmp_briefcase, 'w') as f:
        f.write("blub")
    yield tmp_briefcase
    os.remove(tmp_briefcase)


def test_parse_args_briefcase(briefcase):

    parser = parse_args(['--briefcase', briefcase])
    assert parser.briefcase_file == briefcase
    assert parser.all is False


def test_parse_args_briefcase_does_not_exist():

    with pytest.raises(FileNotFoundError):
        parse_args(['--briefcase', 'not_here.csv'])


def test_parse_args_all_windows():
    parser = parse_args(['--all'])
    assert parser.briefcase_file is None
    assert parser.all is True


def test_parse_args_no_args():
    parser = parse_args([])
    assert parser.briefcase_file is None


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


def test_is_non_zero_file_exists(briefcase):
    assert is_non_zero_file(briefcase)


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