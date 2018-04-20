import os
import json
import sys
import platform
import logging  # keep for LoggingConfig.setup()
import stat
from configparser import ConfigParser

import logzero
from logzero import logger

from .exceptions import SmartVADHIS2Exception, FileException
try:
    from __version__ import __version__
except ImportError:
    from ..__version__ import __version__

SMARTVADHIS2_VERSION = __version__


def load_auth(alt_path, parser=None):

    path = alt_path if alt_path else parser.get('auth', 'auth_file')

    try:
        with open(path, 'r') as f:
            return json.load(f)
    except (IOError, AttributeError):
        raise FileNotFoundError("Could not read authentication file at {}".format(path))


class Config(object):

    ROOT_DIR = os.path.abspath('.')
    _parser = ConfigParser()
    _parser.read(os.path.join(ROOT_DIR, 'config.ini'))

    dish = load_auth(alt_path=None, parser=_parser)

    @staticmethod
    def create_dir(path, created_message=False):
        if not os.path.exists(path):
            os.mkdir(path)
            if created_message:
                logger.info("Created folder {}".format(created_message))


class DataDirConfig(Config):
    data_dir = os.path.join(Config.ROOT_DIR, 'data')

    def setup(self):
        self.create_dir(self.data_dir)


class ODKConfig(Config):
    __section__ = 'odk'
    briefcases_dir = os.path.join(Config.ROOT_DIR, 'data', 'briefcases')
    briefcase_executable = os.path.join(Config.ROOT_DIR, 'smartvadhis2', 'lib')  # download JAR first
    jar_url = Config._parser.get(__section__, 'dl_url')
    jar_sig = Config._parser.get(__section__, 'dl_sig')
    form_id = Config._parser.get(__section__, 'form_id')
    sid_regex = Config._parser.get(__section__, 'sid_regex')

    baseurl = Config.dish[__section__]['baseurl']
    username = Config.dish[__section__]['username']
    password = Config.dish[__section__]['password']

    if not all([baseurl, username, password]):
        raise FileNotFoundError("[{}] Empty baseurl, username or password."
                                "Check docs for proper format.".format(__section__))

    def setup(self):
        self.create_dir(self.briefcases_dir)


class SmartVAConfig(Config):
    __section__ = 'smartva'
    smartva_dir = os.path.join(Config.ROOT_DIR, 'data', 'smartvas')
    smartva_executable = os.path.join(Config.ROOT_DIR, 'smartvadhis2', 'lib', 'smartva')
    ignore_columns = Config._parser.get(__section__, 'ignore_columns').split(',')
    algorithm_version = Config._parser.get(__section__, 'algorithm_version')

    def setup(self):
        self.create_dir(self.smartva_dir)
        self.create_dir(os.path.join(self.smartva_dir, 'output'))
        self.make_executable()

    def make_executable(self):
        st = os.stat(self.smartva_executable)
        os.chmod(self.smartva_executable, st.st_mode | stat.S_IEXEC)


class DatabaseConfig(Config):
    __section__ = 'database'
    database_dir = os.path.join(Config.ROOT_DIR, 'db')
    db_name = Config._parser.get(__section__, 'db_name')
    db_queries_log = Config._parser.getboolean(__section__, 'db_queries_log')

    def setup(self):
        self.create_dir(self.database_dir, created_message=True)


class DhisConfig(Config):
    __section__ = 'dhis'
    program_uid = Config._parser.get(__section__, 'program')
    programstage_uid = Config._parser.get(__section__, 'program_stage')
    root_orgunit = Config._parser.get(__section__, 'root_orgunit')

    baseurl = Config.dish[__section__]['baseurl']
    username = Config.dish[__section__]['username']
    password = Config.dish[__section__]['password']

    api_version = Config._parser.getint(__section__, 'api_version')

    if not all([baseurl, username, password]):
        raise FileException("[{}] Empty baseurl, username or password. Check docs for proper format.".format(__section__))


class LoggingConfig(Config):
    __section__ = 'logging'
    log_file = Config._parser.get('logging', 'logfile')
    __log_level_from_config = Config._parser.get('logging', 'level')
    log_level = eval('logging.{}'.format(__log_level_from_config.upper()))

    def setup(self):
        log_format = '%(color)s[%(asctime)s %(levelname)s]%(end_color)s %(message)s'
        formatter = logzero.LogFormatter(fmt=log_format)
        logzero.setup_default_logger(formatter=formatter)

        # Log rotation of 10 files for 10MB each
        logzero.logfile(self.log_file, loglevel=self.log_level, maxBytes=int(1e7), backupCount=20)
        logger.info("smartvadhis2 v.{} - logging to {} with min level {}".format(
            SMARTVADHIS2_VERSION,
            self.log_file,
            self.__log_level_from_config)
        )


def check_python_version():
    required_major = 3
    required_minor = 5
    if sys.version_info < (required_major, required_minor):
        raise SmartVADHIS2Exception("Python {}.{}+ required - installed is {}.{}".format(
            required_major,
            required_minor,
            sys.version_info.major,
            sys.version_info.minor
        ))


def check_operating_system():
    """
    Get the operating system the application is running on
    :rtype: Operating System string (Linux, Windows)
    """
    opsys = platform.system()
    logger.debug("Running on {}".format(opsys))
    if opsys in {'Linux', 'Windows'}:
        return opsys
    else:
        raise SmartVADHIS2Exception("Must run on Linux or Windows")


def setup():
    LoggingConfig().setup()

    check_python_version()
    check_operating_system()

    DatabaseConfig().setup()
    DataDirConfig().setup()
    ODKConfig().setup()
    SmartVAConfig().setup()
    DhisConfig()

    from .briefcase import ODKBriefcase
    from .smartva import SmartVA
    from .dhis import Dhis
    from . import database

    dhis = Dhis()
    briefcase = ODKBriefcase()
    smartva = SmartVA()
    db = database.get_db()

    return dhis, briefcase, smartva, db
