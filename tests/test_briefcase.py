import datetime
import os

from smartvadhis2.core.briefcase import ODKBriefcase
from smartvadhis2.core.config import ODKConfig


def test_briefcase_jar_exists():
    briefcase = ODKBriefcase()
    assert os.path.exists(briefcase.jar_path)


def test_briefcase_args_timewindows():
    briefcase = ODKBriefcase()
    actual = briefcase._get_arguments(all_briefcases=False)
    assert actual[18] == '--export_start_date'
    assert actual[20] == '--export_end_date'
    assert len(actual) == 22


def test_briefcase_args_all():
    now = datetime.datetime.now()
    briefcase = ODKBriefcase()
    actual = briefcase._get_arguments(all_briefcases=True)
    expected = [
        'java', '-jar', briefcase.jar_path,
        '--storage_directory', ODKConfig.briefcases_dir,
        '--export_directory', ODKConfig.briefcases_dir,
        '--form_id', ODKConfig.form_id,
        '--aggregate_url', ODKConfig.baseurl,
        '--odk_username', ODKConfig.username,
        '--odk_password', ODKConfig.password,
        #'--export_filename', 'briefcase_{}.csv'.format(now.strftime('%Y%m%d_%H%M%S')),
        '--exclude_media_export'
    ]
    for o in expected:
        assert o in actual

    assert '--export_start_date' not in actual
    assert '--export_end_date' not in actual
