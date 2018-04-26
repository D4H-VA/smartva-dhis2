import json
import os
import platform
import subprocess
import logging  # keep for LoggingConfig.setup()
import stat
import sys
from configparser import ConfigParser

import logzero
from logzero import logger

from .exceptions import SmartVADHIS2Exception, FileException

try:
    from __version__ import __version__
except ImportError:
    from ..__version__ import __version__

"""
Module to configure the application, load the ConfigParser file (config.ini) and set up necessary folders
"""

SMARTVADHIS2_VERSION = __version__


def load_auth(alt_path, parser=None):
    """Load the authentication file as specified in config.ini and return a Python object
    alt_path is used for testing purposes to load a different file
    """
    path = alt_path if alt_path else parser.get('auth', 'auth_file')

    try:
        with open(path, 'r') as f:
            return json.load(f)
    except (IOError, AttributeError):
        raise FileNotFoundError("Could not read authentication file at {}".format(path))


class Config(object):
    """Base class for all configuration classes"""
    ROOT_DIR = os.path.abspath('.')
    _parser = ConfigParser()
    _parser.read(os.path.join(ROOT_DIR, 'config.ini'))

    dish = load_auth(alt_path=None, parser=_parser)

    @staticmethod
    def create_dir(path, created_message=False):
        """Create folders and optionally log a info message"""
        if not os.path.exists(path):
            os.mkdir(path)
            if created_message:
                logger.info("Created folder {}".format(created_message))


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


class DataDirConfig(Config):
    """Class to set up the `data` directory containing both Briefcases and SmartVA files"""
    data_dir = os.path.join(Config.ROOT_DIR, 'data')

    def setup(self):
        self.create_dir(self.data_dir)


class ODKConfig(Config):
    """Class to set up ODK Briefcase"""
    __section__ = 'odk'
    briefcases_dir = os.path.join(Config.ROOT_DIR, 'data', 'briefcases')
    briefcase_executable = os.path.join(Config.ROOT_DIR, 'smartvadhis2', 'lib')  # download JAR first
    briefcase_version = "v1.9.0"

    jar_url = "https://s3.amazonaws.com/opendatakit.downloads/ODK Briefcase {} Production.jar".format(briefcase_version)
    # https://opendatakit.org/wp-content/uploads/sha256_signatures.txt
    jar_sig = "b9c2259b63ae87ef4cfbb16c752b806fc95acf49ff2cb96171f93a2f39fd5995"

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
    """Class to set up SmartVA"""
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
        """Make the smartva binary executable (for Linux systems)"""
        st = os.stat(self.smartva_executable)
        os.chmod(self.smartva_executable, st.st_mode | stat.S_IEXEC)


class DatabaseConfig(Config):
    """Class to set up the local database"""
    __section__ = 'database'
    database_dir = os.path.join(Config.ROOT_DIR, 'db')
    db_name = Config._parser.get(__section__, 'db_name')
    db_queries_log = Config._parser.getboolean(__section__, 'db_queries_log')

    def setup(self):
        self.create_dir(self.database_dir, created_message=True)


class DhisConfig(Config):
    """Class to set up DHIS2"""
    __section__ = 'dhis'
    program_uid = Config._parser.get(__section__, 'program')
    programstage_uid = Config._parser.get(__section__, 'program_stage')

    baseurl = Config.dish[__section__]['baseurl']
    username = Config.dish[__section__]['username']
    password = Config.dish[__section__]['password']

    api_version = Config._parser.getint(__section__, 'api_version')

    if not all([baseurl, username, password]):
        raise FileException(
            "[{}] Empty baseurl, username or password. Check docs for proper format.".format(__section__))


def check_python_version():
    """Verify that we're on Python 3.5+"""
    required_major = 3
    required_minor = 5
    if sys.version_info < (required_major, required_minor):
        raise SmartVADHIS2Exception("Python {}.{}+ required - installed is {}.{}".format(
            required_major,
            required_minor,
            sys.version_info.major,
            sys.version_info.minor
        ))


def check_java_installed():
    """Verify java is installed for running ODK Briefcase"""
    try:
        subprocess.Popen(['java', '--version'],
                         bufsize=1,
                         universal_newlines=True,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)
    except FileNotFoundError:
        logger.exception("Java installation not found")


def check_operating_system():
    """Get the operating system the application is running on"""
    opsys = platform.system()
    logger.debug("Running on {}".format(opsys))
    if opsys in {'Linux', 'Windows'}:
        return opsys
    else:
        raise SmartVADHIS2Exception("Must run on Linux or Windows")


def setup():
    """Method to set everything up and return instances of the respective module classes"""
    LoggingConfig().setup()

    check_operating_system()
    check_java_installed()
    check_python_version()

    DatabaseConfig().setup()
    DataDirConfig().setup()
    ODKConfig().setup()
    SmartVAConfig().setup()
    DhisConfig()


def access():
    # import here to avoid circular dependencies
    from .briefcase import ODKBriefcase
    from .smartva import SmartVA
    from .dhis import Dhis
    from . import database

    dhis = Dhis()
    briefcase = ODKBriefcase()
    smartva = SmartVA()
    db = database.get_db()

    return dhis, briefcase, smartva, db
