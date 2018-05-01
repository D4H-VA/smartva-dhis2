#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import time

from setuptools import find_packages, setup, Command
from smartvadhis2.core.config import DataDirConfig

here = os.path.abspath(os.path.dirname(__file__))

__version__ = ''
with open(os.path.join('smartvadhis2', '__version__.py')) as f:
    exec(f.read())


def status(s):
    """Prints things in bold."""
    print('\033[1m{0}\033[0m'.format(s))
    time.sleep(2)


class TestCommand(Command):
    description = 'Run Unit tests.'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    @staticmethod
    def run():
        status('Testing with pytest...')
        os.system('python -m pytest --cov=smartvadhis2 --cov-report term-missing tests -vv')


class ProfileCommand(Command):
    description = 'Profile application'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    @staticmethod
    def run():
        status('Profiling with cProfile: running with ~50.000 briefcase records (this may take a while)')
        test_file = os.path.join('tests', 'testdata', 'load_test_51800_odk_records.csv')
        cprofile_output = os.path.join(DataDirConfig.data_dir, 'smartva_dhis2_profile_output')
        os.system('python -m cProfile -o {} smartvadhis2/__main__.py --manual {}'.format(cprofile_output, test_file))

        status('Profiling with /usr/bin/time: running with ~10.000 briefcase records')
        test_file = os.path.join('tests', 'testdata', 'load_test_1000_odk_records.csv')
        os.system('time -v python -m smartvadhis2 --manual {}'.format(test_file))

        status('Profiling file written to {}. Open http://localhost:4000'.format(cprofile_output))
        os.system('cprofilev -f smartva_dhis2_profile_output')


with open('README.rst', 'r') as f:
    readme = f.read()

setup(
    name='smartva-dhis2',
    version=__version__,
    description='Integration of Verbal Autopsy data into DHIS2.',
    long_description=readme,
    author='Data For Health Initiative - Verbal Autopsy',
    url='https://github.com/D4H-VA/smartva-dhis2',
    keywords='smartva verbal autopsy dhis2 tariff odk',
    license='MIT',
    install_requires=[
        'requests',
        'records',
        'logzero',
        'alembic',
        'apscheduler'
    ],
    packages=find_packages(),
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'License :: OSI Approved :: MIT License',
        'License :: Other/Proprietary License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
    ],
    cmdclass={
        'test': TestCommand,
        'profile': ProfileCommand
    },
)
