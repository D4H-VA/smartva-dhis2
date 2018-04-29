import os
import re
import subprocess
from datetime import datetime

from logzero import logger

from .config import ODKConfig
from .exceptions import BriefcaseException
from .helpers import get_timewindow

"""
Module to connect to ODK by wrapping ODK Briefcase (JAR)
"""


class ODKBriefcase(object):

    def __init__(self):

        self._log_version()
        self.timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

    def _get_arguments(self, all_briefcases):
        """Create the argument list to provide to the Briefcase JAR
        see: https://docs.opendatakit.org/briefcase-using/#working-with-the-command-line
        """
        arguments = [
            'java', '-jar', ODKConfig.briefcase_executable,
            '--storage_directory', ODKConfig.briefcases_dir,
            '--export_directory', ODKConfig.briefcases_dir,
            '--form_id', ODKConfig.form_id,
            '--aggregate_url', ODKConfig.baseurl,
            '--odk_username', ODKConfig.username,
            '--odk_password', ODKConfig.password,
            '--exclude_media_export'
        ]
        logger.info("Connecting to ODK Briefcase on {} ...".format(ODKConfig.baseurl))

        if not all_briefcases:
            start, end = get_timewindow()
            export_filename = "briefcases_from_{}_at_{}.csv".format(start.replace('/', ''), self.timestamp)
            time_window = [
                '--export_start_date', start,
                '--export_end_date', end
            ]
            arguments.extend(time_window)
            logger.info("Fetching briefcases from {} to {} ...".format(start, end))
        else:
            logger.info("Fetching ALL briefcases...")
            export_filename = "briefcases_all_{}.csv".format(self.timestamp)

        arguments.extend(['--export_filename', export_filename])
        return arguments, export_filename

    def _log_version(self):
        with subprocess.Popen(['java', '-jar', ODKConfig.briefcase_executable, '-v'],
                              bufsize=1,
                              universal_newlines=True,
                              stdout=subprocess.PIPE,
                              stderr=subprocess.STDOUT) as process:
            self._log_subprocess_output(process)

    @staticmethod
    def _log_subprocess_output(process):
        """Log output from subprocess"""
        for line in process.stdout:
            if re.compile(r'.*INFO.*$').match(line) and not re.compile(
                    r'.*Submission date is before specified, skipping.*').match(line):
                logger.debug(line)
            elif re.compile(r'^\[main]\sWARN\s.*$').match(line):
                logger.warn(line)
            elif re.compile(r'^Error: Server connection test failure.*').match(line):
                raise BriefcaseException("Could not connect to ODK server. Check config.ini / dish.json")
            elif re.compile(r'^\[main]\sERROR\s.*$').match(line):
                logger.error(line)
                raise BriefcaseException(line)

            else:
                # remove timestamp for better readability
                line = re.sub(r'^\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2},\d{3}\s', '', line)
                line = re.sub(r'Processing instance', 'Downloading instance', line)
                logger.info(str(line).replace('\n', ''))

    def download_briefcases(self, all_briefcases):
        """Do the actual call to the JAR file and return generated filename path"""
        args, filename = self._get_arguments(all_briefcases)
        with subprocess.Popen(args,
                              bufsize=1,
                              universal_newlines=True,
                              stdout=subprocess.PIPE,
                              stderr=subprocess.STDOUT) as process:
            self._log_subprocess_output(process)

        export = os.path.join(ODKConfig.briefcases_dir, filename)
        return export
