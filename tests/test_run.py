import os
import pytest

from smartvadhis2.run import _parse_args
from smartvadhis2.core.helpers import csv_with_content
from smartvadhis2.core.config import Config


def file_testdata(filename):
    return os.path.join(Config.ROOT_DIR, 'tests', 'testdata', filename)


def test_parse_args_briefcase():
    briefcase_file = file_testdata('briefcase_valid.csv')
    parser = _parse_args(['--manual', briefcase_file])
    assert parser.manual == briefcase_file
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


def test_csv_with_content_exists():
    briefcase_file = file_testdata('briefcase_valid.csv')
    assert csv_with_content(briefcase_file)
