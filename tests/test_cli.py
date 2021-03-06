from smartvadhis2.cli import remove_keys, print_error_categories


def test_remove_keys():
    metadata = {
        "programStages": [
            {
                "lastUpdated": "2018-04-19T13:38:20.185",
                "id": "pQ8gaWKD3pi",
                "created": "2018-03-07T19:31:51.060",
                "name": "Verbal Autopsy",
                "executionDateLabel": "Date of death",
                "allowGenerateNextVisit": False,
                "validCompleteOnly": False,
                "preGenerateUID": False,
                "openAfterEnrollment": False,
                "repeatable": False,
                "captureCoordinates": False,
                "remindCompleted": False,
                "displayGenerateEventBox": False,
                "generatedByEnrollmentDate": False,
                "autoGenerateEvent": True,
                "sortOrder": 1,
                "hideDueDate": False,
                "blockEntryForm": False,
                "minDaysFromStart": 0,
                "program": {
                    "id": "HPrJOsYuM1K"
                },
                "lastUpdatedBy": {
                    "id": "rJYzV7B0Md5"
                },
                "notificationTemplates": [],
                "programStageDataElements": [
                    {
                        "lastUpdated": "2018-04-19T13:38:20.042",
                        "id": "kI1px9KVtbz",
                        "created": "2018-03-07T19:31:51.060",
                        "displayInReports": False,
                        "externalAccess": False,
                        "renderOptionsAsRadio": False,
                        "allowFutureDate": False,
                        "compulsory": False,
                        "allowProvidedElsewhere": False,
                        "sortOrder": 0,
                        "lastUpdatedBy": {
                            "id": "rJYzV7B0Md5"
                        },
                        "programStage": {
                            "id": "pQ8gaWKD3pi"
                        },
                        "dataElement": {
                            "id": "C2OT4YktNGX"
                        },
                        "translations": [],
                        "userGroupAccesses": [],
                        "attributeValues": [],
                        "userAccesses": []
                    },
                    {
                        "lastUpdated": "2018-04-19T13:38:20.049",
                        "id": "mxZzEsvsdcF",
                        "created": "2018-03-07T19:31:51.061",
                        "displayInReports": False,
                        "externalAccess": False,
                        "renderOptionsAsRadio": False,
                        "allowFutureDate": False,
                        "compulsory": False,
                        "allowProvidedElsewhere": False,
                        "sortOrder": 1,
                        "lastUpdatedBy": {
                            "id": "rJYzV7B0Md5"
                        },
                        "programStage": {
                            "id": "pQ8gaWKD3pi"
                        },
                        "dataElement": {
                            "id": "t6O2A1gou0g"
                        },
                        "translations": [],
                        "userGroupAccesses": [],
                        "attributeValues": [],
                        "userAccesses": []
                    }
                ],
                "translations": [],
                "attributeValues": [],
                "programStageSections": []
            }
        ],
        "categoryOptionCombos": [],
        "programs": [
            {
                "lastUpdated": "2018-04-19T13:20:49.440",
                "id": "HPrJOsYuM1K",
                "created": "2018-03-07T19:31:51.129",
                "name": "Verbal Autopsy",
                "shortName": "VA",
                "publicAccess": "rw------",
                "completeEventsExpiryDays": 0,
                "description": "Data integration program from smartvadhis2",
                "ignoreOverdueEvents": False,
                "skipOffline": False,
                "captureCoordinates": False,
                "displayFrontPageList": False,
                "onlyEnrollOnce": False,
                "programType": "WITHOUT_REGISTRATION",
                "version": 4,
                "selectIncidentDatesInFuture": False,
                "displayIncidentDate": False,
                "selectEnrollmentDatesInFuture": False,
                "expiryDays": 0,
                "useFirstStageDuringRegistration": False,
                "lastUpdatedBy": {
                    "id": "rJYzV7B0Md5"
                },
                "user": {
                    "id": "rJYzV7B0Md5"
                },
                "programTrackedEntityAttributes": [],
                "notificationTemplates": [],
                "translations": [],
                "organisationUnits": [],
                "userGroupAccesses": [],
                "attributeValues": [],
                "validationCriterias": [],
                "programStages": [
                    {
                        "id": "pQ8gaWKD3pi"
                    }
                ],
                "userAccesses": []
            }
        ],
        "optionSets": [
            {
                "code": "VA-CoD",
                "created": "2018-04-19T13:07:32.552",
                "lastUpdated": "2018-04-19T13:07:32.724",
                "name": "VA- Cause of Death",
                "id": "tMkHCKkuxpD",
                "publicAccess": "rw------",
                "version": 0,
                "valueType": "TEXT",
                "lastUpdatedBy": {
                    "id": "rJYzV7B0Md5"
                },
                "user": {
                    "id": "rJYzV7B0Md5"
                },
                "userGroupAccesses": [],
                "attributeValues": [],
                "translations": [],
                "userAccesses": [],
                "options": [
                    {
                        "id": "cjrgMGLMwbu"
                    }
                ]
            },
            {
                "code": "VA-Sex",
                "created": "2018-04-19T06:55:22.425",
                "lastUpdated": "2018-04-19T06:55:22.442",
                "name": "VA- Sex",
                "id": "fXYBfOoLXgh",
                "publicAccess": "rw------",
                "version": 0,
                "valueType": "TEXT",
                "lastUpdatedBy": {
                    "id": "rJYzV7B0Md5"
                },
                "user": {
                    "id": "rJYzV7B0Md5"
                },
                "userGroupAccesses": [],
                "attributeValues": [],
                "translations": [],
                "userAccesses": [],
                "options": [
                    {
                        "id": "xwtfJn76te7"
                    },
                    {
                        "id": "QgHSjOft8v4"
                    },
                    {
                        "id": "LbjOq1YRCW2"
                    },
                    {
                        "id": "K7wBJlg8eRQ"
                    },
                    {
                        "id": "k8sIQ2bEaYT"
                    }
                ]
            }
        ],
        "categories": [],
        "programStageDataElements": [
            {
                "created": "2018-04-19T12:05:57.227",
                "lastUpdated": "2018-04-19T13:38:20.167",
                "id": "hGHimNEVl0B",
                "displayInReports": False,
                "renderOptionsAsRadio": False,
                "compulsory": False,
                "allowProvidedElsewhere": False,
                "sortOrder": 15,
                "allowFutureDate": False,
                "lastUpdatedBy": {
                    "id": "rJYzV7B0Md5"
                },
                "programStage": {
                    "id": "pQ8gaWKD3pi"
                },
                "dataElement": {
                    "id": "NsmhGfGhFRO"
                }
            },
            {
                "created": "2018-03-07T19:31:51.062",
                "lastUpdated": "2018-04-19T13:38:20.131",
                "id": "Z06nEMh81QI",
                "displayInReports": False,
                "renderOptionsAsRadio": False,
                "compulsory": False,
                "allowProvidedElsewhere": False,
                "sortOrder": 10,
                "allowFutureDate": False,
                "lastUpdatedBy": {
                    "id": "rJYzV7B0Md5"
                },
                "programStage": {
                    "id": "pQ8gaWKD3pi"
                },
                "dataElement": {
                    "id": "NM9CFZmYq9S"
                }
            }
        ],
        "dataElements": [
            {
                "code": "gen_5_0b",
                "lastUpdated": "2018-04-19T13:42:10.250",
                "id": "VEGzj76HCEN",
                "created": "2018-04-19T13:42:10.250",
                "name": "VA- Second Surname",
                "shortName": "Surname 2",
                "aggregationType": "NONE",
                "domainType": "TRACKER",
                "publicAccess": "rw------",
                "description": "Second surname",
                "valueType": "TEXT",
                "formName": "Second Surname",
                "zeroIsSignificant": False,
                "lastUpdatedBy": {
                    "id": "rJYzV7B0Md5"
                },
                "user": {
                    "id": "rJYzV7B0Md5"
                },
                "translations": [],
                "userGroupAccesses": [],
                "attributeValues": [],
                "userAccesses": [],
                "legendSets": [],
                "aggregationLevels": []
            },
            {
                "lastUpdated": "2018-04-19T13:42:10.256",
                "id": "lFKqfDj9Rhk",
                "created": "2018-04-19T13:42:10.256",
                "name": "VA- Age category",
                "shortName": "Age category",
                "aggregationType": "COUNT",
                "domainType": "TRACKER",
                "publicAccess": "rw------",
                "description": "Age category",
                "valueType": "INTEGER_POSITIVE",
                "formName": "Age category",
                "zeroIsSignificant": False,
                "optionSet": {
                    "id": "AXlVIlSE9zB"
                },
                "lastUpdatedBy": {
                    "id": "rJYzV7B0Md5"
                },
                "user": {
                    "id": "rJYzV7B0Md5"
                },
                "translations": [],
                "userGroupAccesses": [],
                "attributeValues": [],
                "userAccesses": [],
                "legendSets": [],
                "aggregationLevels": []
            }
        ],
        "options": [
            {
                "lastUpdated": "2018-04-19T13:07:32.584",
                "code": "107",
                "created": "2018-04-19T13:07:32.551",
                "name": "Adult - Colorectal Cancer (C18)",
                "id": "U3gJ2b6mW1k",
                "sortOrder": 6,
                "optionSet": {
                    "id": "tMkHCKkuxpD"
                },
                "translations": [],
                "attributeValues": []
            },
            {
                "lastUpdated": "2018-04-19T13:07:32.584",
                "code": "135",
                "created": "2018-04-19T13:07:32.552",
                "name": "Adult - Chronic Respiratory (J44)",
                "id": "UgfoWoGUBO5",
                "sortOrder": 32,
                "optionSet": {
                    "id": "tMkHCKkuxpD"
                },
                "translations": [],
                "attributeValues": []
            }
        ]
    }

    expected = {
        "programStages": [
            {
                "lastUpdated": "2018-04-19T13:38:20.185",
                "id": "pQ8gaWKD3pi",
                "created": "2018-03-07T19:31:51.060",
                "name": "Verbal Autopsy",
                "executionDateLabel": "Date of death",
                "allowGenerateNextVisit": False,
                "validCompleteOnly": False,
                "preGenerateUID": False,
                "openAfterEnrollment": False,
                "repeatable": False,
                "captureCoordinates": False,
                "remindCompleted": False,
                "displayGenerateEventBox": False,
                "generatedByEnrollmentDate": False,
                "autoGenerateEvent": True,
                "sortOrder": 1,
                "hideDueDate": False,
                "blockEntryForm": False,
                "minDaysFromStart": 0,
                "program": {
                    "id": "HPrJOsYuM1K"
                },
                "notificationTemplates": [],
                "programStageDataElements": [
                    {
                        "lastUpdated": "2018-04-19T13:38:20.042",
                        "id": "kI1px9KVtbz",
                        "created": "2018-03-07T19:31:51.060",
                        "displayInReports": False,
                        "externalAccess": False,
                        "renderOptionsAsRadio": False,
                        "allowFutureDate": False,
                        "compulsory": False,
                        "allowProvidedElsewhere": False,
                        "sortOrder": 0,
                        "programStage": {
                            "id": "pQ8gaWKD3pi"
                        },
                        "dataElement": {
                            "id": "C2OT4YktNGX"
                        },
                        "translations": [],
                        "userGroupAccesses": [],
                        "attributeValues": [],
                        "userAccesses": []
                    },
                    {
                        "lastUpdated": "2018-04-19T13:38:20.049",
                        "id": "mxZzEsvsdcF",
                        "created": "2018-03-07T19:31:51.061",
                        "displayInReports": False,
                        "externalAccess": False,
                        "renderOptionsAsRadio": False,
                        "allowFutureDate": False,
                        "compulsory": False,
                        "allowProvidedElsewhere": False,
                        "sortOrder": 1,
                        "programStage": {
                            "id": "pQ8gaWKD3pi"
                        },
                        "dataElement": {
                            "id": "t6O2A1gou0g"
                        },
                        "translations": [],
                        "userGroupAccesses": [],
                        "attributeValues": [],
                        "userAccesses": []
                    }
                ],
                "translations": [],
                "attributeValues": [],
                "programStageSections": []
            }
        ],
        "categoryOptionCombos": [],
        "programs": [
            {
                "lastUpdated": "2018-04-19T13:20:49.440",
                "id": "HPrJOsYuM1K",
                "created": "2018-03-07T19:31:51.129",
                "name": "Verbal Autopsy",
                "shortName": "VA",
                "publicAccess": "rw------",
                "completeEventsExpiryDays": 0,
                "description": "Data integration program from smartvadhis2",
                "ignoreOverdueEvents": False,
                "skipOffline": False,
                "captureCoordinates": False,
                "displayFrontPageList": False,
                "onlyEnrollOnce": False,
                "programType": "WITHOUT_REGISTRATION",
                "version": 4,
                "selectIncidentDatesInFuture": False,
                "displayIncidentDate": False,
                "selectEnrollmentDatesInFuture": False,
                "expiryDays": 0,
                "useFirstStageDuringRegistration": False,
                "programTrackedEntityAttributes": [],
                "notificationTemplates": [],
                "translations": [],
                "organisationUnits": [],
                "userGroupAccesses": [],
                "attributeValues": [],
                "validationCriterias": [],
                "programStages": [
                    {
                        "id": "pQ8gaWKD3pi"
                    }
                ],
                "userAccesses": []
            }
        ],
        "optionSets": [
            {
                "code": "VA-CoD",
                "created": "2018-04-19T13:07:32.552",
                "lastUpdated": "2018-04-19T13:07:32.724",
                "name": "VA- Cause of Death",
                "id": "tMkHCKkuxpD",
                "publicAccess": "rw------",
                "version": 0,
                "valueType": "TEXT",
                "userGroupAccesses": [],
                "attributeValues": [],
                "translations": [],
                "userAccesses": [],
                "options": [
                    {
                        "id": "cjrgMGLMwbu"
                    }
                ]
            },
            {
                "code": "VA-Sex",
                "created": "2018-04-19T06:55:22.425",
                "lastUpdated": "2018-04-19T06:55:22.442",
                "name": "VA- Sex",
                "id": "fXYBfOoLXgh",
                "publicAccess": "rw------",
                "version": 0,
                "valueType": "TEXT",
                "userGroupAccesses": [],
                "attributeValues": [],
                "translations": [],
                "userAccesses": [],
                "options": [
                    {
                        "id": "xwtfJn76te7"
                    },
                    {
                        "id": "QgHSjOft8v4"
                    },
                    {
                        "id": "LbjOq1YRCW2"
                    },
                    {
                        "id": "K7wBJlg8eRQ"
                    },
                    {
                        "id": "k8sIQ2bEaYT"
                    }
                ]
            }
        ],
        "categories": [],
        "programStageDataElements": [
            {
                "created": "2018-04-19T12:05:57.227",
                "lastUpdated": "2018-04-19T13:38:20.167",
                "id": "hGHimNEVl0B",
                "displayInReports": False,
                "renderOptionsAsRadio": False,
                "compulsory": False,
                "allowProvidedElsewhere": False,
                "sortOrder": 15,
                "allowFutureDate": False,
                "programStage": {
                    "id": "pQ8gaWKD3pi"
                },
                "dataElement": {
                    "id": "NsmhGfGhFRO"
                }
            },
            {
                "created": "2018-03-07T19:31:51.062",
                "lastUpdated": "2018-04-19T13:38:20.131",
                "id": "Z06nEMh81QI",
                "displayInReports": False,
                "renderOptionsAsRadio": False,
                "compulsory": False,
                "allowProvidedElsewhere": False,
                "sortOrder": 10,
                "allowFutureDate": False,
                "programStage": {
                    "id": "pQ8gaWKD3pi"
                },
                "dataElement": {
                    "id": "NM9CFZmYq9S"
                }
            }
        ],
        "dataElements": [
            {
                "code": "gen_5_0b",
                "lastUpdated": "2018-04-19T13:42:10.250",
                "id": "VEGzj76HCEN",
                "created": "2018-04-19T13:42:10.250",
                "name": "VA- Second Surname",
                "shortName": "Surname 2",
                "aggregationType": "NONE",
                "domainType": "TRACKER",
                "publicAccess": "rw------",
                "description": "Second surname",
                "valueType": "TEXT",
                "formName": "Second Surname",
                "zeroIsSignificant": False,
                "translations": [],
                "userGroupAccesses": [],
                "attributeValues": [],
                "userAccesses": [],
                "legendSets": [],
                "aggregationLevels": []
            },
            {
                "lastUpdated": "2018-04-19T13:42:10.256",
                "id": "lFKqfDj9Rhk",
                "created": "2018-04-19T13:42:10.256",
                "name": "VA- Age category",
                "shortName": "Age category",
                "aggregationType": "COUNT",
                "domainType": "TRACKER",
                "publicAccess": "rw------",
                "description": "Age category",
                "valueType": "INTEGER_POSITIVE",
                "formName": "Age category",
                "zeroIsSignificant": False,
                "optionSet": {
                    "id": "AXlVIlSE9zB"
                },
                "translations": [],
                "userGroupAccesses": [],
                "attributeValues": [],
                "userAccesses": [],
                "legendSets": [],
                "aggregationLevels": []
            }
        ],
        "options": [
            {
                "lastUpdated": "2018-04-19T13:07:32.584",
                "code": "107",
                "created": "2018-04-19T13:07:32.551",
                "name": "Adult - Colorectal Cancer (C18)",
                "id": "U3gJ2b6mW1k",
                "sortOrder": 6,
                "optionSet": {
                    "id": "tMkHCKkuxpD"
                },
                "translations": [],
                "attributeValues": []
            },
            {
                "lastUpdated": "2018-04-19T13:07:32.584",
                "code": "135",
                "created": "2018-04-19T13:07:32.552",
                "name": "Adult - Chronic Respiratory (J44)",
                "id": "UgfoWoGUBO5",
                "sortOrder": 32,
                "optionSet": {
                    "id": "tMkHCKkuxpD"
                },
                "translations": [],
                "attributeValues": []
            }
        ]
    }

    assert remove_keys(metadata, ['lastUpdatedBy', 'user']) == expected


def test_print_error_categories(capsys):
    expected = "Validation Errors (600-699)\n" \
               "- ID:600 - Could not parse [birth_date]\n" \
               "- ID:601 - Could not parse [death_date]\n" \
               "- ID:602 - Could not parse [age] as Integer\n" \
               "- ID:603 - [age] is not between 0 and 120 years\n" \
               "- ID:604 - [age] is missing\n" \
               "- ID:605 - [icd10] does not match mapping\n" \
               "- ID:606 - [icd10] missing\n" \
               "- ID:607 - [sex] is not an Integer in (1, 2, 3, 8, 9)\n" \
               "- ID:608 - [sex] is missing\n" \
               "- ID:609 - [sid] does not match regex expression\n" \
               "- ID:610 - [sid] is missing\n" \
               "- ID:611 - orgunit is missing\n" \
               "- ID:612 - orgunit UID is not a valid UID\n" \
               "Import Errors (700-799)\n" \
               "- ID:700 - OrgUnit is not a valid UID\n" \
               "- ID:701 - Program is not a valid program\n" \
               "- ID:703 - Non-categorized import exception\n" \
               "- ID:704 - Event for VA.SID already exists\n" \
               "- ID:705 - Orgunit is not assigned to program\n" \
               "Validation Warnings (800-899)\n" \
               "- ID:800 - [age] missing\n" \
               "- ID:801 - [birth_date] missing\n" \
               "- ID:802 - [first_name] is empty\n" \
               "- ID:803 - [surname] is empty\n" \
               "- ID:804 - [interview_date] missing\n" \
               "- ID:805 - Could not parse [interview_date]\n"

    print_error_categories()
    captured = capsys.readouterr()
    assert captured.out == expected
