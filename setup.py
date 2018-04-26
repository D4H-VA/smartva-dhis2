#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from setuptools import find_packages, setup, Command

here = os.path.abspath(os.path.dirname(__file__))

__version__ = ''
with open(os.path.join('smartvadhis2', '__version__.py')) as f:
    exec(f.read())


class TestCommand(Command):
    description = 'Run Unit tests.'
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print('\033[1m{0}\033[0m'.format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        self.status('Testing with pytest...')
        os.system('python -m pytest --cov=smartvadhis2 --cov-report term-missing tests -vv')


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
        'test': TestCommand
    },
)
