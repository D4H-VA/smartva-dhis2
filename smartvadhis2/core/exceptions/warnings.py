from .base import SmartVADHIS2Exception


class ValidationWarning(SmartVADHIS2Exception):
    """ Base class for Validation warnings"""

    def __init__(self, message, code):
        self.message = message
        self.code = code
        self.type = 'VALIDATION'
        super(SmartVADHIS2Exception, self).__init__(self.message)

    def __str__(self):
        return "Warning ({}): {}".format(self.code, self.message)

    def __repr__(self):
        return str(self)


class AgeMissingWarning(ValidationWarning):
    message = "[age] missing"
    code = 800
    err_type = 'VALIDATION'

    def __init__(self):
        super(ValidationWarning, self).__init__(self.message, self.code)


class BirthDateMissingWarning(ValidationWarning):
    message = "[birth_date] missing"
    code = 801
    err_type = 'VALIDATION'

    def __init__(self):
        super(ValidationWarning, self).__init__(self.message, self.code)


class FirstNameMissingWarning(ValidationWarning):
    code = 802
    err_type = 'VALIDATION'
    message = "[first_name] is empty"

    def __init__(self):
        super(ValidationWarning, self).__init__(self.message, self.code)


class SurnameMissingWarning(ValidationWarning):
    code = 803
    err_type = 'VALIDATION'
    message = "[surname] is empty"

    def __init__(self):
        super(ValidationWarning, self).__init__(self.message, self.code)


class InterviewDateMissingWarning(ValidationWarning):
    message = "[interview_date] missing"
    code = 804
    err_type = 'VALIDATION'

    def __init__(self):
        super(ValidationWarning, self).__init__(self.message, self.code)


__all__ = [
    'ValidationWarning',
    'AgeMissingWarning',
    'BirthDateMissingWarning',
    'FirstNameMissingWarning',
    'SurnameMissingWarning',
    'InterviewDateMissingWarning'
]
