import os
import logging

import pytest

from smartvadhis2.core.config import (
    DataDirConfig,
    ODKConfig,
    SmartVAConfig,
    DatabaseConfig,
    DhisConfig,
    LoggingConfig,
    check_python_version,
    load_auth,
    setup as setup_with_config
)

from smartvadhis2.core.helpers import is_uid

setup_with_config()


def test_create_file(tmpdir):
    p = tmpdir.mkdir("pytest").join("hello.txt")
    p.write("content")
    assert p.read() == "content"
    assert len(tmpdir.listdir()) == 1


def test_load_auth():
    dish = load_auth(alt_path='dish.json')
    assert dish['dhis']['baseurl'] is not None
    assert dish['dhis']['username'] is not None
    assert dish['dhis']['password'] is not None
    assert dish['odk']['baseurl'] is not None
    assert dish['odk']['username'] is not None
    assert dish['odk']['password'] is not None


def test_load_auth_fails():
    with pytest.raises(FileNotFoundError):
        load_auth(alt_path='notexistent.json')


def test_file_config():
    cfg = DataDirConfig()
    assert os.path.exists(cfg.data_dir)


def test_odk_config():
    cfg = ODKConfig()
    assert os.path.exists(cfg.briefcase_executable)
    assert os.path.exists(cfg.briefcases_dir)
    assert cfg.form_id is not None
    assert cfg.sid_regex is not None
    assert cfg.baseurl is not None
    assert cfg.username is not None
    assert cfg.password is not None


def test_smartva_config():
    cfg = SmartVAConfig()
    assert os.path.exists(cfg.smartva_dir)
    assert os.path.exists(cfg.smartva_executable)
    assert cfg.ignore_columns is not None
    assert cfg.algorithm_version is not None
    assert cfg.country is not None
    assert isinstance(cfg.hiv, bool)
    assert isinstance(cfg.malaria, bool)
    assert isinstance(cfg.hce, bool)


def test_database_config():
    cfg = DatabaseConfig()
    assert os.path.exists(cfg.database_dir)
    assert cfg.db_name is not None
    assert isinstance(cfg.db_queries_log, bool)


def test_dhis_config():
    cfg = DhisConfig()
    assert cfg.baseurl is not None
    assert cfg.username is not None
    assert cfg.password is not None
    assert is_uid(cfg.programstage_uid)
    assert is_uid(cfg.program_uid)
    assert cfg.api_version >= 28


def test_logging_config():
    cfg = LoggingConfig()
    assert cfg.log_file is not None
    assert cfg.log_level in {logging.INFO, logging.WARNING, logging.DEBUG}


def test_python_version():
    check_python_version()
