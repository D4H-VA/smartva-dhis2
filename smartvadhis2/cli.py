import argparse
import json
import sys
import time

import requests

try:
    from core.config import DhisConfig
    from core.dhis import Dhis
    from core.helpers import Color
except ImportError:
    from smartvadhis2.core.config import DhisConfig
    from smartvadhis2.core.dhis import Dhis
    from smartvadhis2.core.helpers import Color


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

    arguments = parser.parse_args()
    print(arguments)
    if not any([arguments.delete_events, arguments.program_metadata]):
        parser.error('Must provide an argument. see --help')
    return arguments


def remove_keys(obj, rubbish):
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
    confirm = input('You are about to {}delete{} ALL Verbal Autopsy DHIS2 Program Events from {}{}. '
                    'Are you really sure? Type yes / no'.format(Color.RED, Color.BOLD, DhisConfig.baseurl, Color.END))
    if confirm.lower() == 'yes':
        api = Dhis()

        program_name = api.get(endpoint='programs/{}'.format(DhisConfig.program_uid)).json().get('name')

        params = {
            'program': DhisConfig.program_uid,
            'skipPaging': True,
            'fields': 'event'
        }
        events = api.get(endpoint='events', params=params).json()

        no_of_events = len(events['events'])
        print("Deleting {}{} events{} for the '{}' program ({})...".format(Color.BOLD, no_of_events, Color.END,
                                                                           program_name, DhisConfig.program_uid))
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


def main():
    args = parse_args()
    if args.delete_events:
        delete_events()
    if args.program_metadata:
        download_program_metadata()


if __name__ == '__main__':
    main()
