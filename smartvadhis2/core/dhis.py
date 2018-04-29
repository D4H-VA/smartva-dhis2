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

"""
Module for DHIS2 access and Import Status
"""


class RaiseImportFailure(object):
    """Raise exception if import failed"""
    def __init__(self, response):

        try:
            self.status_code = int(response['httpStatusCode'])
            self.imported = int(response['response']['imported'])
            self.updated = int(response['response']['updated'])
            self.ignored = int(response['response']['ignored'])
            self.deleted = int(response['response']['deleted'])
        except (ValueError, KeyError, TypeError):
            logger.debug(response)
            raise GenericImportError("Error parsing response: {}".format(response))

        else:
            if self.status_code not in {200, 201} or self.imported == 0:
                try:
                    # check if all response state are SUCCESS
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


def raise_if_duplicate(response, sid):
    """Check response and raise if there is already an event"""
    event_count = int(response.get('height', 0))
    if event_count > 0:
        event_uids = ','.join([e[1] for e in response['rows']])
        message = '{} events already exist for SID {} in events {}'.format(event_count, sid, event_uids)
        raise DuplicateEventImportError(message)


class Dhis(object):
    """Class for accessing DHIS2"""
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

        logger.info("Connecting to DHIS2 on {} ...".format(url))
        self.api_url = '{}/api/{}'.format(url, api_version)
        self.api = requests.Session()
        self.auth = (DhisConfig.username, DhisConfig.password)
        self.headers = {'User-Agent': 'smartvadhis2_v.{}'.format(SMARTVADHIS2_VERSION)}

        self.root_orgunit = self.root_orgunit()

    def get(self, endpoint, params=None):
        """DHIS2 HTTP GET, returns requests.Response object"""
        url = '{}/{}.json'.format(self.api_url, endpoint)
        # logger.debug('GET: {} - Params: {}'.format(url, params))
        return self.api.get(url, params=params, auth=self.auth, headers=self.headers)

    def post(self, endpoint, data, params=None):
        """DHIS2 HTTP POST, returns requests.Response object"""
        url = '{}/{}'.format(self.api_url, endpoint)
        # logger.debug('POST: {} - Params: {} - Data: {}'.format(url, params, json.dumps(data)))
        return self.api.post(url, params=params, auth=self.auth, headers=self.headers, json=data)

    def delete(self, endpoint):
        """DHIS2 HTTP DELETE, returns requests.Response object"""
        url = '{}/{}'.format(self.api_url, endpoint)
        return self.api.delete(url, auth=self.auth, headers=self.headers)

    def post_event(self, data):
        """POST DHIS2 Event"""
        r = self.post(endpoint='events', data=data)
        try:
            # logger.debug(r.text)
            RaiseImportFailure(r.json())
            r.raise_for_status()
        except OrgUnitNotAssignedError:
            self.assign_orgunit_to_program(data)
            self.post(endpoint='events', data=data)
        except requests.RequestException:
            raise DhisApiException("POST failed - {} {}".format(r.url, r.text))

    def is_duplicate(self, sid):
        """Check DHIS2 for a duplicate event by SID across all OrgUnits"""
        params = {
            'programStage': DhisConfig.programstage_uid,
            'orgUnit': self.root_orgunit,
            'ouMode': 'DESCENDANTS',
            'filter': '{}:EQ:{}'.format(Sid.dhis_uid, sid)
        }
        r = self.get(endpoint='events/query', params=params)
        raise_if_duplicate(r.json(), sid)

    def root_orgunit(self):
        params = {
            'fields': 'id',
            'filter': 'level:eq:1'
        }
        req = self.get(endpoint='organisationUnits', params=params).json()
        return self._get_root_id(req)

    @staticmethod
    def _get_root_id(response):
        if len(response['organisationUnits']) > 1:
            raise DhisApiException("More than one Organisation Units found. Can not proceed.")
        if len(response['organisationUnits']) == 0:
            raise DhisApiException("No Organisation Unit found. Can not proceed.")
        return response['organisationUnits'][0]['id']

    def assign_orgunit_to_program(self, data):
        """Assign OrgUnit to program"""
        params = {
            'fields': ':owner'
        }
        existing = self.get('programs/{}'.format(DhisConfig.program_uid), params=params).json()
        org_unit = data['orgUnit']

        if org_unit not in [ou['id'] for ou in existing['organisationUnits']]:
            existing['organisationUnits'].append({"id": org_unit})
            self.post('metadata', data={'programs': [existing]})
            logger.info("Assigned orgUnit {}".format(org_unit))
