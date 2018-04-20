import os
import shutil
import subprocess

from logzero import logger

from .config import SmartVAConfig, ODKConfig
from .helpers import log_subprocess_output, is_non_zero_file


class SmartVA(object):

    def __init__(self):
        self.briefcase_dir = ODKConfig.briefcases_dir

    def run(self, input_file, manual=False):
        if is_non_zero_file(input_file):
            input_path = input_file if manual else os.path.join(self.briefcase_dir, input_file)
            logger.debug(input_path)

            logger.info("Running SmartVA ...")
            self._execute([SmartVAConfig.smartva_executable, '--version'])
            self._execute([SmartVAConfig.smartva_executable, input_path, SmartVAConfig.smartva_dir])

            return self._cleanup(input_file)
        else:
            logger.debug("Empty input file for smartva: {}".format(input_file))

    @staticmethod
    def _execute(arguments):
        with subprocess.Popen(arguments,
                              bufsize=1,
                              universal_newlines=True,
                              stdout=subprocess.PIPE,
                              stderr=subprocess.STDOUT) as print_info:
            log_subprocess_output(print_info)

    @staticmethod
    def _cleanup(filename):
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
