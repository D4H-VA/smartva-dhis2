import os
import pytest

from smartvadhis2.run import _parse_args
from smartvadhis2.core.helpers import is_non_zero_file

@pytest.fixture
def briefcase():
    tmp_briefcase = 'briefcase_test.csv'
    with open(tmp_briefcase, 'w') as f:
        f.write("blub")
    yield tmp_briefcase
    os.remove(tmp_briefcase)


def test_parse_args_briefcase(briefcase):
    parser = _parse_args(['--manual', briefcase])
    assert parser.manual == briefcase
    assert parser.all is False


def test_parse_args_briefcase_does_not_exist():
    with pytest.raises(FileNotFoundError):
        _parse_args(['--manual', 'not_here.csv'])


def test_parse_args_all_windows():
    parser = _parse_args(['--all'])
    assert parser.manual is None
    assert parser.all is True


def test_parse_args_no_args():
    parser = _parse_args([])
    assert parser.manual is None


def test_is_non_zero_file_exists(briefcase):
    assert is_non_zero_file(briefcase)
