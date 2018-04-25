import os
import re
import shutil
import subprocess

from logzero import logger

from .config import SmartVAConfig, ODKConfig
from .helpers import is_non_zero_file
from .exceptions import NoODKDataException

"""
Module for wrapping smartva
"""


class SmartVA(object):

    def __init__(self):
        self.briefcase_dir = ODKConfig.briefcases_dir

    def run(self, input_file, manual=False):
        """Entry method to run smartva"""
        if is_non_zero_file(input_file):
            input_path = input_file if manual else os.path.join(self.briefcase_dir, input_file)

            logger.info("Running SmartVA ...")
            self._execute([SmartVAConfig.smartva_executable, '--version'])
            self._execute([SmartVAConfig.smartva_executable, input_path, SmartVAConfig.smartva_dir])
            return self._cleanup(input_file)
        else:
            logger.debug("Empty input file for smartva: {}".format(input_file))

    def _execute(self, arguments):
        """Call the smartva binary with provided arguments and log output messages"""
        with subprocess.Popen(arguments,
                              bufsize=1,
                              universal_newlines=True,
                              stdout=subprocess.PIPE,
                              stderr=subprocess.STDOUT) as print_info:
            self._log_subprocess_output(print_info)

    @staticmethod
    def _cleanup(filename):
        """smartva creates lots of files that we don't need
        move the one we need to `output` folder and remove the rest
        """
        output_file = os.path.join(SmartVAConfig.smartva_dir, '1-individual-cause-of-death', 'individual-cause-of-death.csv')
        target_file = os.path.join(SmartVAConfig.smartva_dir, 'output', 'smartva_{}'.format(os.path.basename(filename).replace('_briefcase', '')))
        try:
            shutil.move(output_file, target_file)
            shutil.rmtree(os.path.join(SmartVAConfig.smartva_dir, '1-individual-cause-of-death'))
            shutil.rmtree(os.path.join(SmartVAConfig.smartva_dir, '2-csmf'))
            shutil.rmtree(os.path.join(SmartVAConfig.smartva_dir, '3-graphs-and-tables'))
            shutil.rmtree(os.path.join(SmartVAConfig.smartva_dir, '4-monitoring-and-quality'))
        except FileNotFoundError:
            raise FileNotFoundError("Could not clean up created files in {}".format(SmartVAConfig.smartva_dir))
        else:
            logger.info("Moved output file to {}".format(target_file))
            return target_file

    @staticmethod
    def _log_subprocess_output(process):
        """
        Log output from subprocess, does not log progress bars of smartva
        """
        for line in process.stdout:
            if re.compile('^Source file \".*\" does not contain data').match(line):
                raise NoODKDataException
            if not any(stop in line for stop in {'ETA: ', 'Time: '}):
                logger.info(str(line).replace('\n', ''))
