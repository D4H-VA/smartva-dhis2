import json

import requests
from logzero import logger

from .config import DhisConfig, SMARTVADHIS2_VERSION
from .mapping import Sid

from .exceptions.base import (
    FileException,
    DhisApiException
)
from .exceptions.errors import (
    OrgunitNotValidImportError,
    ProgramNotValidError,
    GenericImportError,
    DuplicateEventImportError,
    OrgUnitNotAssignedError
)


class ImportStatus(object):

    def __init__(self, response):

        try:
            self.status_code = int(response['httpStatusCode'])
            self.imported = int(response['response']['imported'])
            self.updated = int(response['response']['updated'])
            self.ignored = int(response['response']['ignored'])
            self.deleted = int(response['response']['deleted'])
        except (ValueError, KeyError) as e:
            logger.debug(response)
            raise GenericImportError("Error parsing response: {}".format(response))

        else:
            if self.status_code not in {200, 201} or self.imported == 0:
                try:
                    self.description = set([
                        r['description'] for r in response['response']['importSummaries']
                        if r['status'] != 'SUCCESS'])
                except KeyError:
                    try:
                        self.description = set([c[0]['value'] for c in
                                                [r['conflicts'] for r in response['response']['importSummaries'] if
                                                 r['status'] != 'SUCCESS']])
                    except KeyError:
                        logger.debug(response)
                        raise GenericImportError(response)

                if [d for d in self.description if "Event.orgUnit does not point to a valid organisation unit" in d]:
                    raise OrgunitNotValidImportError(self.description)
                elif [d for d in self.description if "Event.program does not point to a valid program" in d]:
                    raise ProgramNotValidError(self.description)
                elif [d for d in self.description if "Program is not assigned to this organisation unit" in d]:
                    raise OrgUnitNotAssignedError(self.description)
                else:
                    logger.debug(response)
                    raise GenericImportError(response)


class RaiseIfDuplicate(object):

    def __init__(self, response, sid):
        event_count = int(response.get('height', 0))
        if event_count > 0:
            event_uids = ','.join([e[1] for e in response['rows']])
            message = '{} events already exist for SID {} in events {}'.format(event_count, sid, event_uids)
            raise DuplicateEventImportError(message)


class Dhis(object):
    def __init__(self):

        url = DhisConfig.baseurl
        api_version = DhisConfig.api_version

        if '/api' in url:
            raise FileException('Do not specify /api in the URL')
        if url.startswith('localhost') or url.startswith('127.0.0.1'):
            url = 'http://{}'.format(url)
        elif url.startswith('http://'):
            url = url
        elif not url.startswith('https://'):
            url = 'https://{}'.format(url)

        self.api_url = '{}/api/{}'.format(url, api_version)
        self.api = requests.Session()
        self.auth = (DhisConfig.username, DhisConfig.password)
        self.headers = {'User-Agent': 'smartvadhis2_v.{}'.format(SMARTVADHIS2_VERSION)}

    def get(self, endpoint, params=None):
        url = '{}/{}.json'.format(self.api_url, endpoint)
        logger.debug('GET: {} - Params: {}'.format(url, params))
        return self.api.get(url, params=params, auth=self.auth, headers=self.headers)

    def post(self, endpoint, data, params=None):
        url = '{}/{}'.format(self.api_url, endpoint)
        logger.debug('POST: {} - Params: {} - Data: {}'.format(url, params, json.dumps(data)))
        return self.api.post(url, params=params, auth=self.auth, headers=self.headers, json=data)

    def delete(self, endpoint):
        url = '{}/{}'.format(self.api_url, endpoint)
        return self.api.delete(url, auth=self.auth, headers=self.headers)

    def post_event(self, data):

        r = self.post(endpoint='events', data=data)
        try:
            logger.debug(r.text)
            ImportStatus(r.json())
            r.raise_for_status()
        except OrgUnitNotAssignedError:
            self.assign_orgunit_to_program(data)
            self.post(endpoint='events', data=data)
        except requests.RequestException:
            raise DhisApiException("POST failed - {} {}".format(r.url, r.text))

    def is_duplicate(self, sid):
        params = {
            'programStage': DhisConfig.programstage_uid,
            'orgUnit': DhisConfig.root_orgunit,
            'ouMode': 'DESCENDANTS',
            'filter': '{}:EQ:{}'.format(Sid.dhis_uid, sid)
        }
        r = self.get(endpoint='events/query', params=params)
        RaiseIfDuplicate(r.json(), sid)

    def assign_orgunit_to_program(self, data):
        params = {
            'fields': ':owner'
        }
        existing = self.get('programs/{}'.format(DhisConfig.program_uid), params=params).json()
        org_unit = data['orgUnit']

        if org_unit not in [ou['id'] for ou in existing['organisationUnits']]:
            existing['organisationUnits'].append({"id": org_unit})
            self.post('metadata', data={'programs': [existing]})
            logger.info("Assigned orgUnit {}".format(org_unit))
