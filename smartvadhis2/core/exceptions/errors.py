from .base import SmartVADHIS2Exception


class ValidationError(SmartVADHIS2Exception):

    def __init__(self, message, code):
        self.message = message
        self.code = code
        super(SmartVADHIS2Exception, self).__init__(self.message)

    def __str__(self):
        return "Error ({}): {}".format(self.code, self.message)

    def __repr__(self):
        return str(self)


class BirthDateParseError(ValidationError):
    code = 600
    err_type = 'VALIDATION'
    message = "Could not parse [birth_date]"

    def __init__(self):
        super(ValidationError, self).__init__(self.message, self.code)


class DeathDateParseError(ValidationError):
    code = 601
    err_type = 'VALIDATION'
    message = "Could not parse [death_date]"

    def __init__(self):
        super(ValidationError, self).__init__(self.message, self.code)


class DeathDateMissingError(ValidationError):
    code = 602
    err_type = 'VALIDATION'
    message = "[death_date] missing"

    def __init__(self):
        super(ValidationError, self).__init__(self.message, self.code)


class AgeParseError(ValidationError):
    code = 603
    err_type = 'VALIDATION'
    message = "Could not parse [age] as Integer"

    def __init__(self):
        super(ValidationError, self).__init__(self.message, self.code)


class AgeOutOfBoundsError(ValidationError):
    code = 604
    err_type = 'VALIDATION'
    message = "[age] is not between 0 and 120 years"

    def __init__(self):
        super(ValidationError, self).__init__(self.message, self.code)


class AgeMissingError(ValidationError):
    code = 605
    err_type = 'VALIDATION'
    message = "[age] is missing"

    def __init__(self):
        super(ValidationError, self).__init__(self.message, self.code)


class CauseOfDeathMissingError(ValidationError):
    code = 606
    err_type = 'VALIDATION'
    message = "[cause34] (cause of death) is missing"

    def __init__(self):
        super(ValidationError, self).__init__(self.message, self.code)


class Icd10ParseError(ValidationError):
    code = 607
    err_type = 'VALIDATION'
    message = "[icd10] does not match mapping"

    def __init__(self):
        super(ValidationError, self).__init__(self.message, self.code)


class Icd10MissingError(ValidationError):
    code = 608
    err_type = 'VALIDATION'
    message = "[icd10] missing"

    def __init__(self):
        super(ValidationError, self).__init__(self.message, self.code)


class SexParseError(ValidationError):
    code = 609
    err_type = 'VALIDATION'
    message = "[sex] is not an Integer in (1, 2, 3, 8, 9)"

    def __init__(self):
        super(ValidationError, self).__init__(self.message, self.code)


class SexMissingError(ValidationError):
    code = 610
    err_type = 'VALIDATION'
    message = "[sex] is missing"

    def __init__(self):
        super(ValidationError, self).__init__(self.message, self.code)


class SidParseError(ValidationError):
    code = 611
    err_type = 'VALIDATION'
    message = "[sid] does not match regex expression"

    def __init__(self):
        super(ValidationError, self).__init__(self.message, self.code)


class SidMissingError(ValidationError):
    code = 612
    err_type = 'VALIDATION'
    message = "[sid] is missing"

    def __init__(self):
        super(ValidationError, self).__init__(self.message, self.code)


class OrgunitMissingError(ValidationError):
    code = 613
    err_type = 'VALIDATION'
    message = "orgunit is missing"

    def __init__(self):
        super(ValidationError, self).__init__(self.message, self.code)


class OrgunitNotValidError(ValidationError):
    code = 614
    err_type = 'VALIDATION'
    message = "orgunit UID is not a valid UID"

    def __init__(self):
        super(ValidationError, self).__init__(self.message, self.code)


class ImportException(SmartVADHIS2Exception):
    def __init__(self, message, code):
        self.message = message
        self.code = code
        super(SmartVADHIS2Exception, self).__init__(self.message)

    def __str__(self):
        return "DHIS2 import error ({}): {}".format(self.code, self.message)

    def __repr__(self):
        return str(self)


class OrgunitNotValidImportError(ImportException):
    message = "OrgUnit is not a valid UID"
    code = 700
    err_type = 'IMPORT'

    def __init__(self, description):
        super(ImportException, self).__init__("{}: {}".format(self.message, description), self.code)


class ProgramNotValidError(ImportException):
    message = "Program is not a valid program"
    code = 701
    err_type = 'IMPORT'

    def __init__(self, description):
        super(ImportException, self).__init__("{}: {}".format(self.message, description), self.code)


class GenericImportError(ImportException):
    message = "Non-categorized import exception"
    code = 703
    err_type = 'IMPORT'

    def __init__(self, response):
        super(ImportException, self).__init__("{}: {}".format(self.message, response), self.code)


class DuplicateEventImportError(ImportException):
    message = "Event for VA.SID already exists"
    code = 704
    err_type = 'IMPORT'

    def __init__(self, response):
        super(ImportException, self).__init__("{}: {}".format(self.message, response), self.code)


class OrgUnitNotAssignedError(ImportException):
    message = "Orgunit is not assigned to program"
    code = 705
    err_type = 'IMPORT'

    def __init__(self, response):
        super(ImportException, self).__init__("{}: {}".format(self.message, response), self.code)


__all__ = [
    'ValidationError',
    'BirthDateParseError',
    'DeathDateParseError',
    'DeathDateMissingError',
    'AgeParseError',
    'AgeOutOfBoundsError',
    'AgeMissingError',
    'CauseOfDeathMissingError',
    'Icd10ParseError',
    'Icd10MissingError',
    'SexParseError',
    'SexMissingError',
    'SidParseError',
    'SidMissingError',
    'OrgunitMissingError',
    'OrgunitNotValidError',
    'ImportException',
    'OrgunitNotValidImportError',
    'ProgramNotValidError',
    'GenericImportError',
    'DuplicateEventImportError',
    'OrgUnitNotAssignedError'
]
