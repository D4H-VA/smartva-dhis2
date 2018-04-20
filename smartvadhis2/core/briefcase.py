import math
import os
import subprocess
from datetime import datetime

import requests
from logzero import logger
from tqdm import tqdm

from .config import ODKConfig
from .exceptions.base import FileException
from .helpers import sha256_checksum, log_subprocess_output, get_timewindow, is_non_zero_file


class ODKBriefcase(object):

    def __init__(self):

        self.jar_filename = ODKConfig.jar_url.split('/')[-1]
        self.jar_path = os.path.join(ODKConfig.briefcase_executable, self.jar_filename)
        if not os.path.exists(self.jar_path):
            self._download_jar()
        self._verify_jar()

        self.timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.filename = "briefcase_{}.csv".format(self.timestamp)

    def _download_jar(self):
        logger.info("Downloading {} ...".format(self.jar_filename))
        r = requests.get(ODKConfig.jar_url, stream=True)
        total_size = int(r.headers.get('content-length', 0))
        block_size = 1024
        wrote = 0
        with open(self.jar_path, 'wb') as f:
            for chunk in tqdm(r.iter_content(chunk_size=1024),
                              total=math.ceil(total_size // block_size),
                              unit='KB',
                              unit_scale=True):
                if chunk:
                    wrote = wrote + len(chunk)
                    f.write(chunk)

    def _verify_jar(self):
        if sha256_checksum(self.jar_path) != ODKConfig.jar_sig:
            raise FileException("Verification failed for {} and hash set in config.ini".format(self.jar_filename))

    def _get_arguments(self, all_briefcases):
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

    def download_briefcases(self, all_briefcases):

        args = self._get_arguments(all_briefcases)

        try:
            with subprocess.Popen(args,
                                  bufsize=1,
                                  universal_newlines=True,
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.STDOUT) as process:
                log_subprocess_output(process)
            return os.path.join(ODKConfig.briefcases_dir, self.filename)

        except subprocess.CalledProcessError as e:
            logger.exception(e)
