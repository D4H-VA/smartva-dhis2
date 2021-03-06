import json
import re
from collections import OrderedDict
from datetime import datetime

from logzero import logger

from .config import DhisConfig, ODKConfig, SmartVAConfig
from .exceptions.errors import (
    ValidationError,
    BirthDateParseError,
    DeathDateParseError,
    AgeParseError,
    AgeOutOfBoundsError,
    Icd10ParseError,
    Icd10MissingError,
    SexParseError,
    SexMissingError,
    SidParseError,
    SidMissingError,
    OrgunitMissingError,
    OrgunitNotValidError
)
from .exceptions.warnings import (
    ValidationWarning,
    AgeMissingWarning,
    BirthDateMissingWarning,
    FirstNameMissingWarning,
    SurnameMissingWarning,
    InterviewDateMissingWarning,
    InterviewDateParseWarning
)
from .helpers import sanitize, is_uid, years_to_days
from .mapping import Mapping, Sex, AgeCategory, Icd10, cause_of_death_option_code
from ..__version__ import __version__


"""
Module for Verbal Autopsy
"""


def process_row_data(data):
    """
    Process row data
    first get the one we need to add those properties whose `set_order` (see mapping.py) start with 0, then 1, ...
    and sort it alphabetically by key
    """
    row_data = OrderedDict()
    for i in Mapping.set_order_range():
        # get row based on mapping properties and sort it alphabetically
        row_data.update(sorted({
            mapping.code_name: sanitize(data, mapping.csv_name)
            for mapping in Mapping.properties()
            if mapping.set_order == i and mapping.csv_name is not None
        }.items(), key=lambda t: t[0]))
    return row_data


def verbal_autopsy_factory(data):
    """
    Factory method to set VerbalAutopsy instance attributes
    and collect all validation exceptions and warnings
    return VerbalAutopsy, its exceptions and its warnings as a tuple
    """
    row_data = process_row_data(data)

    va = VerbalAutopsy()
    exceptions = []
    warnings = []

    # set CSV row attributes
    for k, v in row_data.items():
        try:
            setattr(va, k, v)
            va.algorithm_version = SmartVAConfig.algorithm_version
            va.questionnaire_version = ODKConfig.form_id
        except ValidationError as e:
            exceptions.append(e)
        except ValidationWarning as e:
            warnings.append(e)

    return va, exceptions, warnings


class VerbalAutopsy(object):
    """
    Base class for Verbal Autopsy that utilizes Python's @property decorators
    implemented as class whose attributes can be accessed both as keys and attributes.
    """

    def __getitem__(self, item):
        """If va.attribute is set, va['attribute'] should return the same"""
        return self.__getattribute__(item)

    def __setitem__(self, key, value):
        """If va['attribute'] is set, va.attribute should return the same"""
        return self.__setattr__(key, value)

    def __getattr__(self, _):
        """Return None if instance attribute does not exist"""
        return None

    def keys(self):
        return [k for k in dir(self) if not k.startswith('_') and not callable(self[k])]

    def __str__(self):
        """Print VerbalAutopsy instance as JSON"""
        return json.dumps(dict(self), sort_keys=True)

    @property
    def age(self):
        return self._age

    @age.setter
    def age(self, value):
        lower_limit = 0
        upper_limit = 131
        if value:
            try:
                f = float(value)
            except ValueError:
                raise AgeParseError()
            else:
                if int(f) not in range(lower_limit, upper_limit):
                    raise AgeOutOfBoundsError()
                else:
                    self._age = round(f, 2)
                    if years_to_days(f) < 29:
                        self._age_category = AgeCategory.options['Neonate']
                    elif int(f) < 12:
                        self._age_category = AgeCategory.options['Child']
                    else:
                        self._age_category = AgeCategory.options['Adult']
        else:
            raise AgeMissingWarning()

    @property
    def age_category(self):
        return self._age_category

    @age_category.setter
    def age_category(self, value):
        self._age_category = value

    @property
    def cause_of_death(self):
        try:
            return cause_of_death_option_code(self._age_category, self._icd10)
        except KeyError:
            raise Exception("Bug detected: Age category was not calculated correctly")

    @property
    def birth_date(self):
        return self._birth_date

    @birth_date.setter
    def birth_date(self, birth_date):
        DATE_FMT = '%Y-%m-%d'
        if birth_date:
            try:
                d = datetime.strptime(birth_date, DATE_FMT)
            except ValueError:
                raise BirthDateParseError()
            else:
                self._birth_date = d.strftime(DATE_FMT)
        else:
            raise BirthDateMissingWarning()

    @property
    def death_date(self):
        return self._death_date

    @death_date.setter
    def death_date(self, death_date):
        DATE_FMT = '%Y-%m-%d'
        if death_date:
            try:
                d = datetime.strptime(death_date, DATE_FMT)
            except ValueError:
                raise DeathDateParseError()
            else:
                self._death_date = d.strftime(DATE_FMT)
        elif self._interview_date:
            self._death_date = self._interview_date
        else:
            self._death_date = datetime.now().strftime(DATE_FMT)

    @property
    def interview_date(self):
        return self._interview_date

    @interview_date.setter
    def interview_date(self, interview_date):
        DATE_FMT_1 = '%Y-%m-%d'
        DATE_FMT_2 = '%b %d, %Y'  # corresponds to 'Mar 26, 2018' on the locale expression of the Month (e.g. Jan)
        if interview_date:
            try:
                d = datetime.strptime(interview_date, DATE_FMT_1)
                self._interview_date = d.strftime(DATE_FMT_1)
            except ValueError:
                try:
                    d = datetime.strptime(interview_date, DATE_FMT_2)
                    self._interview_date = d.strftime(DATE_FMT_1)
                except ValueError:
                    raise InterviewDateParseWarning()
        else:
            raise InterviewDateMissingWarning()

    @property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, name1):
        if name1:
            self._first_name = name1
        else:
            raise FirstNameMissingWarning()

    @property
    def first_name_2nd(self):
        return self._first_name_2nd

    @first_name_2nd.setter
    def first_name_2nd(self, name2):
        self._first_name_2nd = name2

    @property
    def surname(self):
        return self._surname

    @surname.setter
    def surname(self, name3):
        if name3:
            self._surname = name3
        else:
            raise SurnameMissingWarning()

    @property
    def surname_2nd(self):
        return self._surname_2nd

    @surname_2nd.setter
    def surname_2nd(self, name4):
        self._surname_2nd = name4

    @property
    def orgunit(self):
        return self._orgunit

    @orgunit.setter
    def orgunit(self, value):
        if value:
            if is_uid(value):
                self._orgunit = value
            else:
                raise OrgunitNotValidError()
        else:
            raise OrgunitMissingError()

    @property
    def icd10(self):
        return self._icd10

    @icd10.setter
    def icd10(self, value):
        if value:
            if value in Icd10.options.keys():
                self._icd10 = Icd10.options[value]
            else:
                raise Icd10ParseError()
        else:
            raise Icd10MissingError()

    @property
    def sex(self):
        return self._sex

    @sex.setter
    def sex(self, sex):
        if sex:
            try:
                value = int(sex)
            except ValueError:
                raise SexParseError()
            else:
                if value not in Sex.options:
                    raise SexParseError()
                else:
                    self._sex = value
        else:
            raise SexMissingError()

    @property
    def sid(self):
        return self._sid

    @sid.setter
    def sid(self, sid):
        if sid:
            if re.compile(ODKConfig.sid_regex).match(sid):
                self._sid = sid
            else:
                raise SidParseError()
        else:
            raise SidMissingError()

    @property
    def national_id(self):
        return self._national_id

    @national_id.setter
    def national_id(self, value):
        self._national_id = value

    @property
    def algorithm_version(self):
        return self._algorithm_version

    @algorithm_version.setter
    def algorithm_version(self, _):
        self._algorithm_version = SmartVAConfig.algorithm_version

    @property
    def questionnaire_version(self):
        return self._questionnaire_version

    @questionnaire_version.setter
    def questionnaire_version(self, _):
        self._questionnaire_version = ODKConfig.form_id


class Event(object):
    """Class that transforms a VerbalAutopsy Instance to a DHIS2 Event"""

    def __init__(self, va):
        if not isinstance(va, VerbalAutopsy):
            raise ValueError("Cannot process objects of type {}".format(type(va)))
        self.program = DhisConfig.program_uid
        self.orgunit = va.orgunit
        self.datavalues = va
        self.event_date = va.death_date

        self.payload = {
            "program": self.program,
            "orgUnit": self.orgunit,
            "eventDate": self.event_date,
            "status": "COMPLETED",
            "storedBy": "smartvadhis2_v{}".format(__version__),
            "dataValues": self.datavalues
        }

    @property
    def datavalues(self):
        return self._datavalues

    @datavalues.setter
    def datavalues(self, va):
        """Set Event.datavalues if...
        - mapping.code_name is not None, and
        - mapping.dhis_uid is not None, and
        - VA attribute is not None
        """
        self._datavalues = [
            {
                "dataElement": mapping.dhis_uid,
                "value": va[mapping.code_name]
            }
            for mapping in Mapping.properties()
            if all([mapping.code_name, mapping.dhis_uid])
            and va[mapping.code_name] is not None
        ]

    def __str__(self):
        """Print Event instance as JSON"""
        return json.dumps(self.payload)
