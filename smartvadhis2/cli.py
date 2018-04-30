import argparse
import json
import sys
import time

import requests

try:
    from core.config import DhisConfig
    from core.dhis import Dhis
    from core.helpers import Color
    from core.exceptions.__init__ import db_exceptions
    from core.exceptions.warnings import ValidationWarning
    from core.exceptions.errors import ValidationError, ImportException
except ImportError:
    from smartvadhis2.core.config import DhisConfig
    from smartvadhis2.core.dhis import Dhis
    from smartvadhis2.core.helpers import Color
    from smartvadhis2.core.exceptions.__init__ import db_exceptions
    from smartvadhis2.core.exceptions.warnings import ValidationWarning
    from smartvadhis2.core.exceptions.errors import ValidationError, ImportException

"""
Module to provide various ad-hoc commands not to be run regularly
"""


def parse_args():
    parser = argparse.ArgumentParser(usage='%(prog)s', description="CLI helpers for smartvadhis2")

    group = parser.add_mutually_exclusive_group()

    group.add_argument('--delete_events',
                       dest='delete_events',
                       action='store_true',
                       required=False,
                       help="Delete all events"
                       )

    group.add_argument('--download_program_metadata',
                       dest='program_metadata',
                       action='store_true',
                       required=False,
                       help="Download DHIS2 program metadata"
                       )

    group.add_argument('--print_error_categories',
                       dest='error_categories',
                       action='store_true',
                       required=False,
                       help="Print error categories inserted into the database"
                       )

    arguments = parser.parse_args()
    if not any([arguments.delete_events, arguments.program_metadata, arguments.error_categories]):
        parser.error('Must provide an argument. see --help')
    return arguments


def remove_keys(obj, rubbish):
    """Recursively remove keys whose are in `rubbish` and return cleaned object"""
    if isinstance(obj, dict):
        obj = {
            key: remove_keys(value, rubbish)
            for key, value in obj.items()
            if key not in rubbish}
    elif isinstance(obj, list):
        obj = [remove_keys(item, rubbish)
               for item in obj
               if item not in rubbish]
    return obj


def delete_events():
    """Delete ALL Verbal Autopsy Program Events from DHIS2"""
    confirm = input('You are about to {}delete{} ALL Verbal Autopsy DHIS2 Program Events from {}{}. '
                    'Are you really sure? Type yes / no\n'.format(Color.RED, Color.BOLD, DhisConfig.baseurl, Color.END))
    if confirm.lower() == 'yes':
        api = Dhis()

        program_name = api.get(endpoint='programs/{}'.format(DhisConfig.program_uid)).json().get('name')

        params = {
            'program': DhisConfig.program_uid,
            'skipPaging': True,
            'fields': 'event'
        }
        events = api.get(endpoint='events', params=params).json()

        no_of_events = len(events.get('events', 0))
        print("Deleting {}{} events{} for the '{}' program ({})...".format(Color.BOLD, no_of_events, Color.END,
                                                                      program_name, DhisConfig.program_uid))
        if no_of_events > 0:
            time.sleep(5)
            for i, event in enumerate(events['events'], 1):
                r = api.delete('events/{}'.format(event['event']))
                try:
                    r.raise_for_status()
                except requests.HTTPError:
                    print(r.text)
                else:
                    print("[{}/{}] Deleted {}".format(i, no_of_events, event['event']))
    else:
        print("Aborted.")
        sys.exit(0)


def download_program_metadata(skip_csv_metadata=True):
    """
    Download metadata from server and clean up some properties that might create problems in another DHIS2 instance
    If skip_csv_metadata is false, additional properties are returned that are already provided
    in the metadata folder
    """
    api = Dhis()

    metadata = api.get(endpoint='programs/{}/metadata.json'.format(DhisConfig.program_uid)).json()

    if skip_csv_metadata:
        remove_obj = ['dataElements', 'optionSets', 'options']
        descriptor = 'partial (no {}) program metadata'.format('/'.join(remove_obj))
        for obj in remove_obj:
            metadata.pop(obj, None)
    else:
        descriptor = 'full program metadata'

    metadata.pop('categoryCombos', None)
    metadata.pop('categoryOptions', None)
    metadata.pop('categoryOptionCombos', None)
    metadata.pop('categories', None)
    metadata['programs'][0]['version'] = 0
    metadata['programs'][0]['organisationUnits'] = []
    metadata = remove_keys(metadata, ['lastUpdatedBy', 'user'])

    filename = 'program_metadata.json'
    with open(filename, 'w') as f:
        json.dump(metadata, f, sort_keys=True, indent=4)
    print("Exported {} to {}{}{}".format(descriptor, Color.BOLD, filename, Color.END))


def print_error_categories():
    """
    Print exception categories that are inserted into the local database
    """

    def print_tuple(data, msg):
        """Sort by code and print"""
        print(msg)
        [print('- ID:{} - {}'.format(tup[0], tup[1])) for tup in sorted(data, key=lambda tup: tup[0])]

    val_err = [(e.code, e.message) for e in db_exceptions if e.code in range(600, 700)]
    print_tuple(val_err, 'Validation Errors (600-699)')

    import_err = [(e.code, e.message) for e in db_exceptions if e.code in range(700, 800)]
    print_tuple(import_err, 'Import Errors (700-799)')

    var_warn = [(w.code, w.message) for w in db_exceptions if w.code in range(800, 900)]
    print_tuple(var_warn, 'Validation Warnings (800-899)')


def main():
    args = parse_args()
    if args.delete_events:
        delete_events()
    if args.program_metadata:
        download_program_metadata()
    if args.error_categories:
        print_error_categories()


if __name__ == '__main__':
    main()
