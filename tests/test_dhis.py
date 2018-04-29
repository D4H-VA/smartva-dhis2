import pytest

from smartvadhis2.core.dhis import RaiseImportFailure, raise_if_duplicate, Dhis
from smartvadhis2.core.exceptions.errors import *
from smartvadhis2.core.exceptions.base import DhisApiException


def test_import_orgunit_invalid():
    response = {
        "httpStatus": "Conflict",
        "httpStatusCode": 409,
        "status": "ERROR",
        "message": "An error occurred, please check import summary.",
        "response": {
            "responseType": "ImportSummaries",
            "status": "ERROR",
            "imported": 0,
            "updated": 0,
            "deleted": 0,
            "ignored": 1,
            "importOptions": {
                "idSchemes": {},
                "dryRun": False,
                "async": False,
                "importStrategy": "CREATE",
                "mergeMode": "REPLACE",
                "reportMode": "FULL",
                "skipExistingCheck": False,
                "sharing": False,
                "skipNotifications": False,
                "datasetAllowsPeriods": False,
                "strictPeriods": False,
                "strictCategoryOptionCombos": False,
                "strictAttributeOptionCombos": False,
                "strictOrganisationUnits": False,
                "requireCategoryOptionCombo": False,
                "requireAttributeOptionCombo": False
            },
            "importSummaries": [
                {
                    "responseType": "ImportSummary",
                    "status": "ERROR",
                    "importOptions": {
                        "idSchemes": {},
                        "dryRun": False,
                        "async": False,
                        "importStrategy": "CREATE",
                        "mergeMode": "REPLACE",
                        "reportMode": "FULL",
                        "skipExistingCheck": False,
                        "sharing": False,
                        "skipNotifications": False,
                        "datasetAllowsPeriods": False,
                        "strictPeriods": False,
                        "strictCategoryOptionCombos": False,
                        "strictAttributeOptionCombos": False,
                        "strictOrganisationUnits": False,
                        "requireCategoryOptionCombo": False,
                        "requireAttributeOptionCombo": False
                    },
                    "description": "Event.orgUnit does not point to a valid organisation unit: tbd",
                    "importCount": {
                        "imported": 0,
                        "updated": 0,
                        "ignored": 1,
                        "deleted": 0
                    }
                }
            ]
        }
    }

    with pytest.raises(OrgunitNotValidImportError):
        RaiseImportFailure(response)


def test_import_program_invalid():
    response = {
        "httpStatus": "Conflict",
        "httpStatusCode": 409,
        "status": "ERROR",
        "message": "An error occurred, please check import summary.",
        "response": {
            "responseType": "ImportSummaries",
            "status": "ERROR",
            "imported": 0,
            "updated": 0,
            "deleted": 0,
            "ignored": 1,
            "importOptions": {
                "idSchemes": {},
                "dryRun": False,
                "async": False,
                "importStrategy": "CREATE",
                "mergeMode": "REPLACE",
                "reportMode": "FULL",
                "skipExistingCheck": False,
                "sharing": False,
                "skipNotifications": False,
                "datasetAllowsPeriods": False,
                "strictPeriods": False,
                "strictCategoryOptionCombos": False,
                "strictAttributeOptionCombos": False,
                "strictOrganisationUnits": False,
                "requireCategoryOptionCombo": False,
                "requireAttributeOptionCombo": False
            },
            "importSummaries": [
                {
                    "responseType": "ImportSummary",
                    "status": "ERROR",
                    "importOptions": {
                        "idSchemes": {},
                        "dryRun": False,
                        "async": False,
                        "importStrategy": "CREATE",
                        "mergeMode": "REPLACE",
                        "reportMode": "FULL",
                        "skipExistingCheck": False,
                        "sharing": False,
                        "skipNotifications": False,
                        "datasetAllowsPeriods": False,
                        "strictPeriods": False,
                        "strictCategoryOptionCombos": False,
                        "strictAttributeOptionCombos": False,
                        "strictOrganisationUnits": False,
                        "requireCategoryOptionCombo": False,
                        "requireAttributeOptionCombo": False
                    },
                    "description": "Event.program does not point to a valid program: abc",
                    "importCount": {
                        "imported": 0,
                        "updated": 0,
                        "ignored": 1,
                        "deleted": 0
                    }
                }
            ]
        }
    }

    with pytest.raises(ProgramNotValidError):
        RaiseImportFailure(response)


def test_import_success():
    response = {
        "httpStatus": "OK",
        "httpStatusCode": 200,
        "status": "OK",
        "message": "Import was successful.",
        "response": {
            "responseType": "ImportSummaries",
            "status": "SUCCESS",
            "imported": 2,
            "updated": 4,
            "deleted": 0,
            "ignored": 0,
            "importOptions": {
                "idSchemes": {},
                "dryRun": False,
                "async": False,
                "importStrategy": "CREATE",
                "mergeMode": "REPLACE",
                "reportMode": "FULL",
                "skipExistingCheck": False,
                "sharing": False,
                "skipNotifications": False,
                "datasetAllowsPeriods": False,
                "strictPeriods": False,
                "strictCategoryOptionCombos": False,
                "strictAttributeOptionCombos": False,
                "strictOrganisationUnits": False,
                "requireCategoryOptionCombo": False,
                "requireAttributeOptionCombo": False
            },
            "importSummaries": [
                {
                    "responseType": "ImportSummary",
                    "status": "SUCCESS",
                    "importCount": {
                        "imported": 2,
                        "updated": 0,
                        "ignored": 0,
                        "deleted": 0
                    },
                    "reference": "IgEemKlf33z",
                    "href": "https://play.dhis2.org/2.28/api/events/IgEemKlf33z"
                },
                {
                    "responseType": "ImportSummary",
                    "status": "SUCCESS",
                    "importCount": {
                        "imported": 0,
                        "updated": 2,
                        "ignored": 0,
                        "deleted": 0
                    },
                    "reference": "onXW2DQHRGS",
                    "href": "https://play.dhis2.org/2.28/api/events/onXW2DQHRGS"
                },
                {
                    "responseType": "ImportSummary",
                    "status": "SUCCESS",
                    "importCount": {
                        "imported": 0,
                        "updated": 2,
                        "ignored": 0,
                        "deleted": 0
                    },
                    "reference": "A7vnB73x5Xw",
                    "href": "https://play.dhis2.org/2.28/api/events/A7vnB73x5Xw"
                }
            ]
        }
    }
    import_status = RaiseImportFailure(response)
    assert import_status.status_code == 200
    assert import_status.imported == 2
    assert import_status.deleted == 0
    assert import_status.updated == 4
    assert import_status.ignored == 0
    assert import_status.deleted == 0


def test_import_conflict_dataelement_invalid():
    response = {
        "httpStatus": "Conflict",
        "httpStatusCode": 409,
        "status": "WARNING",
        "message": "One more conflicts encountered, please check import summary.",
        "response": {
            "responseType": "ImportSummaries",
            "status": "WARNING",
            "imported": 2,
            "updated": 3,
            "deleted": 0,
            "ignored": 1,
            "importOptions": {
                "idSchemes": {},
                "dryRun": False,
                "async": False,
                "importStrategy": "CREATE",
                "mergeMode": "REPLACE",
                "reportMode": "FULL",
                "skipExistingCheck": False,
                "sharing": False,
                "skipNotifications": False,
                "datasetAllowsPeriods": False,
                "strictPeriods": False,
                "strictCategoryOptionCombos": False,
                "strictAttributeOptionCombos": False,
                "strictOrganisationUnits": False,
                "requireCategoryOptionCombo": False,
                "requireAttributeOptionCombo": False
            },
            "importSummaries": [
                {
                    "responseType": "ImportSummary",
                    "status": "SUCCESS",
                    "importCount": {
                        "imported": 2,
                        "updated": 0,
                        "ignored": 0,
                        "deleted": 0
                    },
                    "reference": "iG9fBAyM71U",
                    "href": "https://play.dhis2.org/2.28/api/events/iG9fBAyM71U"
                },
                {
                    "responseType": "ImportSummary",
                    "status": "WARNING",
                    "importCount": {
                        "imported": 0,
                        "updated": 1,
                        "ignored": 1,
                        "deleted": 0
                    },
                    "conflicts": [
                        {
                            "object": "dataElement",
                            "value": "sWoqcoByYmE is not a valid data element"
                        }
                    ],
                    "reference": "onXW2DQHRGS",
                    "href": "https://play.dhis2.org/2.28/api/events/onXW2DQHRGS"
                },
                {
                    "responseType": "ImportSummary",
                    "status": "SUCCESS",
                    "importCount": {
                        "imported": 0,
                        "updated": 2,
                        "ignored": 0,
                        "deleted": 0
                    },
                    "reference": "A7vnB73x5Xw",
                    "href": "https://play.dhis2.org/2.28/api/events/A7vnB73x5Xw"
                }
            ]
        }
    }

    with pytest.raises(GenericImportError):
        RaiseImportFailure(response)


def test_empty_post_throws():
    response = {
        "httpStatus": "OK",
        "httpStatusCode": 200,
        "status": "OK",
        "message": "Import was successful.",
        "response": {
            "responseType": "ImportSummaries",
            "status": "SUCCESS",
            "imported": 0,
            "updated": 0,
            "deleted": 0,
            "ignored": 0,
            "importOptions": {
                "idSchemes": {},
                "dryRun": False,
                "async": False,
                "importStrategy": "CREATE",
                "mergeMode": "REPLACE",
                "reportMode": "FULL",
                "skipExistingCheck": False,
                "sharing": False,
                "skipNotifications": False,
                "datasetAllowsPeriods": False,
                "strictPeriods": False,
                "strictCategoryOptionCombos": False,
                "strictAttributeOptionCombos": False,
                "strictOrganisationUnits": False,
                "requireCategoryOptionCombo": False,
                "requireAttributeOptionCombo": False
            }
        }
    }

    with pytest.raises(GenericImportError):
        RaiseImportFailure(response)


def test_event_duplicate_found():
    sid = "VA_12345678912345"
    response = {
        "headers": [
            {
                "name": "event",
                "column": "event",
                "type": "java.lang.String",
                "hidden": False,
                "meta": False
            },
            {
                "name": "created",
                "column": "created",
                "type": "java.lang.String",
                "hidden": False,
                "meta": False
            },
            {
                "name": "lastUpdated",
                "column": "lastUpdated",
                "type": "java.lang.String",
                "hidden": False,
                "meta": False
            },
            {
                "name": "storedBy",
                "column": "storedBy",
                "type": "java.lang.String",
                "hidden": False,
                "meta": False
            },
            {
                "name": "completedBy",
                "column": "completedBy",
                "type": "java.lang.String",
                "hidden": False,
                "meta": False
            },
            {
                "name": "completedDate",
                "column": "completedDate",
                "type": "java.lang.String",
                "hidden": False,
                "meta": False
            },
            {
                "name": "eventDate",
                "column": "eventDate",
                "type": "java.lang.String",
                "hidden": False,
                "meta": False
            },
            {
                "name": "dueDate",
                "column": "dueDate",
                "type": "java.lang.String",
                "hidden": False,
                "meta": False
            },
            {
                "name": "orgUnit",
                "column": "orgUnit",
                "type": "java.lang.String",
                "hidden": False,
                "meta": False
            },
            {
                "name": "orgUnitName",
                "column": "orgUnitName",
                "type": "java.lang.String",
                "hidden": False,
                "meta": False
            },
            {
                "name": "status",
                "column": "status",
                "type": "java.lang.String",
                "hidden": False,
                "meta": False
            },
            {
                "name": "longitude",
                "column": "longitude",
                "type": "java.lang.String",
                "hidden": False,
                "meta": False
            },
            {
                "name": "latitude",
                "column": "latitude",
                "type": "java.lang.String",
                "hidden": False,
                "meta": False
            },
            {
                "name": "programStage",
                "column": "programStage",
                "type": "java.lang.String",
                "hidden": False,
                "meta": False
            },
            {
                "name": "program",
                "column": "program",
                "type": "java.lang.String",
                "hidden": False,
                "meta": False
            },
            {
                "name": "attributeOptionCombo",
                "column": "attributeOptionCombo",
                "type": "java.lang.String",
                "hidden": False,
                "meta": False
            },
            {
                "name": "deleted",
                "column": "deleted",
                "type": "java.lang.String",
                "hidden": False,
                "meta": False
            }
        ],
        "rows": [
            [
                "zLPwmHJVr09",
                "2018-04-19 07:43:30.068",
                "2018-04-19 07:43:30.078",
                "smartvadhis2_v0.0.1",
                "bao-admin",
                "2018-04-19 00:00:00.0",
                "2018-03-26 00:00:00.0",
                "2018-04-19 07:43:30.068",
                "MJ0S8In5PIQ",
                "Gournadi Upazila",
                "COMPLETED",
                "",
                "",
                "pQ8gaWKD3pi",
                "HPrJOsYuM1K",
                "HllvX50cXC0",
                "False"
            ]
        ],
        "width": 17,
        "height": 1
    }

    with pytest.raises(DuplicateEventImportError):
        raise_if_duplicate(response, sid)


def test_event_no_duplicate():
    sid = "VA_12345678912345"
    response = {
        "headers": [
            {
                "name": "event",
                "column": "event",
                "type": "java.lang.String",
                "hidden": False,
                "meta": False
            },
            {
                "name": "created",
                "column": "created",
                "type": "java.lang.String",
                "hidden": False,
                "meta": False
            },
            {
                "name": "lastUpdated",
                "column": "lastUpdated",
                "type": "java.lang.String",
                "hidden": False,
                "meta": False
            },
            {
                "name": "storedBy",
                "column": "storedBy",
                "type": "java.lang.String",
                "hidden": False,
                "meta": False
            },
            {
                "name": "completedBy",
                "column": "completedBy",
                "type": "java.lang.String",
                "hidden": False,
                "meta": False
            },
            {
                "name": "completedDate",
                "column": "completedDate",
                "type": "java.lang.String",
                "hidden": False,
                "meta": False
            },
            {
                "name": "eventDate",
                "column": "eventDate",
                "type": "java.lang.String",
                "hidden": False,
                "meta": False
            },
            {
                "name": "dueDate",
                "column": "dueDate",
                "type": "java.lang.String",
                "hidden": False,
                "meta": False
            },
            {
                "name": "orgUnit",
                "column": "orgUnit",
                "type": "java.lang.String",
                "hidden": False,
                "meta": False
            },
            {
                "name": "orgUnitName",
                "column": "orgUnitName",
                "type": "java.lang.String",
                "hidden": False,
                "meta": False
            },
            {
                "name": "status",
                "column": "status",
                "type": "java.lang.String",
                "hidden": False,
                "meta": False
            },
            {
                "name": "longitude",
                "column": "longitude",
                "type": "java.lang.String",
                "hidden": False,
                "meta": False
            },
            {
                "name": "latitude",
                "column": "latitude",
                "type": "java.lang.String",
                "hidden": False,
                "meta": False
            },
            {
                "name": "programStage",
                "column": "programStage",
                "type": "java.lang.String",
                "hidden": False,
                "meta": False
            },
            {
                "name": "program",
                "column": "program",
                "type": "java.lang.String",
                "hidden": False,
                "meta": False
            },
            {
                "name": "attributeOptionCombo",
                "column": "attributeOptionCombo",
                "type": "java.lang.String",
                "hidden": False,
                "meta": False
            },
            {
                "name": "deleted",
                "column": "deleted",
                "type": "java.lang.String",
                "hidden": False,
                "meta": False
            }
        ],
        "rows": [],
        "width": 17,
        "height": 0
    }

    raise_if_duplicate(response, sid)


def test_orgunit_not_assigned():
    response = {
        "httpStatus": "Conflict",
        "httpStatusCode": 409,
        "status": "ERROR",
        "message": "An error occurred, please check import summary.",
        "response": {
            "responseType": "ImportSummaries",
            "status": "ERROR",
            "imported": 0,
            "updated": 0,
            "deleted": 0,
            "ignored": 1,
            "importOptions": {
                "idSchemes": {},
                "dryRun": False,
                "async": False,
                "importStrategy": "CREATE",
                "mergeMode": "REPLACE",
                "reportMode": "FULL",
                "skipExistingCheck": False,
                "sharing": False,
                "skipNotifications": False,
                "datasetAllowsPeriods": False,
                "strictPeriods": False,
                "strictCategoryOptionCombos": False,
                "strictAttributeOptionCombos": False,
                "strictOrganisationUnits": False,
                "requireCategoryOptionCombo": False,
                "requireAttributeOptionCombo": False
            },
            "importSummaries": [
                {
                    "responseType": "ImportSummary",
                    "status": "ERROR",
                    "importOptions": {
                        "idSchemes": {},
                        "dryRun": False,
                        "async": False,
                        "importStrategy": "CREATE",
                        "mergeMode": "REPLACE",
                        "reportMode": "FULL",
                        "skipExistingCheck": False,
                        "sharing": False,
                        "skipNotifications": False,
                        "datasetAllowsPeriods": False,
                        "strictPeriods": False,
                        "strictCategoryOptionCombos": False,
                        "strictAttributeOptionCombos": False,
                        "strictOrganisationUnits": False,
                        "requireCategoryOptionCombo": False,
                        "requireAttributeOptionCombo": False
                    },
                    "description": "Program is not assigned to this organisation unit: MJ0S8In5PIQ",
                    "importCount": {
                        "imported": 0,
                        "updated": 0,
                        "ignored": 1,
                        "deleted": 0
                    }
                }
            ]
        }
    }

    with pytest.raises(OrgUnitNotAssignedError):
        RaiseImportFailure(response)


def test_generic_import_error():
    response = {
        "Unknown response"
    }

    with pytest.raises(GenericImportError):
        RaiseImportFailure(response)


def test_get_root_orgunit():
    response = {
        "organisationUnits": [
            {
                "id": "ImspTQPwCqd"
            }
        ]
    }

    assert 'ImspTQPwCqd' == Dhis._get_root_id(response)


def test_get_root_orgunit_multiple():
    response = {
        "organisationUnits": [
            {
                "id": "ImspTQPwCqd"
            },
            {
                "id": "lc3eMKXaEfw"
            }
        ]
    }
    with pytest.raises(DhisApiException):
        Dhis._get_root_id(response)


def test_get_root_orgunit_none():
    response = {
        "pager": {
            "page": 1,
            "pageCount": 1,
            "total": 1,
            "pageSize": 50
        },
        "organisationUnits": []
    }
    with pytest.raises(DhisApiException):
        Dhis._get_root_id(response)
