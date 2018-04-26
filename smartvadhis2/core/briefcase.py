# -*- coding: utf-8 -*-

import os
import re
import subprocess
from datetime import datetime

from logzero import logger

from .config import ODKConfig
from .helpers import get_timewindow
from .exceptions import BriefcaseException


"""
Module to connect to ODK by wrapping ODK Briefcase (JAR)
"""


class ODKBriefcase(object):

    def __init__(self):

        self.jar_filename = "ODK-Briefcase-v1.10.1.jar"
        self.jar_path = os.path.join(ODKConfig.briefcase_executable, self.jar_filename)

        self._log_version()
        self.timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.filename = "briefcases.csv"

    def _get_arguments(self, all_briefcases):
        """Create the argument list to provide to the Briefcase JAR
        see: https://docs.opendatakit.org/briefcase-using/#working-with-the-command-line
        """

        arguments = [
            'java', '-jar', self.jar_path,
            '--storage_directory', ODKConfig.briefcases_dir,
            '--export_directory', ODKConfig.briefcases_dir,
            '--form_id', ODKConfig.form_id,
            '--aggregate_url', ODKConfig.baseurl,
            '--odk_username', ODKConfig.username,
            '--odk_password', ODKConfig.password,
            '--export_filename', self.filename,
            '--exclude_media_export'
        ]
        logger.info("Connecting to ODK Briefcase on {} ...".format(ODKConfig.baseurl))

        if not all_briefcases:
            start, end = get_timewindow()
            time_window = [
                '--export_start_date', start,
                '--export_end_date', end
            ]
            arguments.extend(time_window)
            logger.info("Fetching briefcases from {} to {} ...".format(start, end))
        else:
            logger.info("Fetching ALL briefcases...")
        return arguments

    def _log_version(self):
        with subprocess.Popen(['java', '-jar', self.jar_path, '-v'],
                              bufsize=1,
                              universal_newlines=True,
                              stdout=subprocess.PIPE,
                              stderr=subprocess.STDOUT) as process:
            self._log_subprocess_output(process)

    @staticmethod
    def _log_subprocess_output(process):
        """Log output from subprocess"""
        for line in process.stdout:
            if re.compile(r'^Error: Server connection test failure.*').match(line):
                raise BriefcaseException("Could not connect to server. Check config.ini / dish.json")
            if re.compile(r'^\[main] WARN .*$').match(line):
                logger.warn(line)
            if re.compile(r'^\[main] ERROR .*$').match(line):
                logger.error(line)
                raise BriefcaseException(line)

            else:
                # remove timestamp for better readabilityf
                line = re.sub(r'^\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2},\d{3}\s', '', line)
                logger.info(str(line).replace('\n', ''))

    def download_briefcases(self, all_briefcases):
        """Do the actual call to the JAR file and log output messages"""
        args = self._get_arguments(all_briefcases)
        with subprocess.Popen(args,
                              bufsize=1,
                              universal_newlines=True,
                              stdout=subprocess.PIPE,
                              stderr=subprocess.STDOUT) as process:
            self._log_subprocess_output(process)
        return os.path.join(ODKConfig.briefcases_dir, self.filename)

