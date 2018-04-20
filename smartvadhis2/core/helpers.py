import argparse
import csv
import datetime
import hashlib
import os
import re

from logzero import logger

from .config import SmartVAConfig
from .exceptions import FileException
from .mapping import Mapping

"""
Module that provides various helper methods cross all other modules
"""

class Color:
    """Color class to be used for Terminal print formatting"""
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


def parse_args(args):
    """Parse arguments"""
    parser = argparse.ArgumentParser(usage='%(prog)s', description="Run SmartVA and import to DHIS2")

    group = parser.add_mutually_exclusive_group()

    group.add_argument('--briefcase',
                       dest='briefcase_file',
                       action='store',
                       required=False,
                       help="Skip download of briefcase file, provide local file path instead"
                       )

    group.add_argument('--all',
                       dest='all',
                       action='store_true',
                       default=False,
                       required=False,
                       help="Pull all briefcases instead of relative time window (e.g. yesterday's)"
                       )

    arguments = parser.parse_args(args)
    if arguments.briefcase_file and not os.path.exists(arguments.briefcase_file):
        raise FileNotFoundError("Briefcase file does not exist: {}".format(arguments.briefcase_file))
    return arguments


def log_subprocess_output(process):
    """Log output from subprocess (e.g. smartva, Briefcase)"""
    [
        logger.info(str(line).replace('\n', ''))
        for line in process.stdout
        if not any(stop in line for stop in {'ETA: ', 'Time: '})  # don't log progress bars (smartva messages)
    ]


def read_csv(path):
    """Generator to read a smartva CSV file"""
    allowed_fields = [m.csv_name for m in Mapping.properties() if m.csv_name is not None]
    with open(path, 'r') as f:
        reader = csv.DictReader(f, delimiter=',')

        for field in reader.fieldnames:
            if field not in allowed_fields and field not in SmartVAConfig.ignore_columns:
                raise FileException("Column '{}' could not be parsed - check Mapping and SmartVA CSV. "
                                    "Ignored columns per config: {}".format(field,
                                                                            ','.join(SmartVAConfig.ignore_columns)))
        for row in reader:
            yield row


def sha256_checksum(filename, block_size=65536):
    """Calculate checksum on file"""
    sha256 = hashlib.sha256()
    with open(filename, 'rb') as f:
        for block in iter(lambda: f.read(block_size), b''):
            sha256.update(block)
    return sha256.hexdigest()


def is_non_zero_file(fpath):
    """Return true if file is existing AND file has content, false otherwise"""
    logger.debug(fpath)
    if fpath:
        exists = os.path.exists(fpath)
        logger.debug("File exists: {}".format(fpath))
        if exists:
            return os.stat(fpath).st_size > 0
    return False


def sanitize(data, some_property):
    """Strip whitespace from a dict value"""
    value = data.get(some_property, '')
    return value.strip() if value else None


def is_uid(string):
    """Return true if string is a valid DHIS2 Unique Identifier (UID)"""
    return re.compile('^[A-Za-z][A-Za-z0-9]{10}$').match(string)


def get_timewindow(weeks=-1, days=1, fmt='%Y/%m/%d'):
    """Return tuple of datetime strings
    start = today minus 1 week
    end = start + 1 day
    e.g. if today is Tuesday, 2018-04-08, return
    (2018-04-01, 2018-04-02)
    """
    now = datetime.datetime.now()
    start = (now + datetime.timedelta(weeks=weeks))
    end = (start + datetime.timedelta(days=days))
    return start.strftime(fmt), end.strftime(fmt)


# Gregorian - see e.g. https://pumas.gsfc.nasa.gov/files/04_21_97_1.pdf
DAYS_IN_YEAR = 365.2425


def days_to_years(days):
    """Convert days to years"""
    return int(round((days / DAYS_IN_YEAR)))


def years_to_days(years):
    """Convert years to days"""
    return int(round((years * DAYS_IN_YEAR)))
