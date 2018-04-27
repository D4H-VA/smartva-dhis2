import datetime

import pytest

from smartvadhis2.core.exceptions.errors import *
from smartvadhis2.core.exceptions.warnings import *
from smartvadhis2.core.mapping import *
from smartvadhis2.core.config import ODKConfig, SmartVAConfig
from smartvadhis2.core.verbalautopsy import VerbalAutopsy, Event, process_row_data, verbal_autopsy_factory, DAYS_IN_YEAR


class VaAbstractClass(object):
    @pytest.fixture
    def va(self):
        return VerbalAutopsy()


class TestAge(VaAbstractClass):

    def test_va_age_years(self, va):
        va.age = '22 years'
        assert va.age_years == 22
        assert va.age_days == 8035
        assert va.age is None

    def test_va_age_number_without_indicator(self, va):
        with pytest.raises(AgeParseError):
            va.age = '22'

    def test_va_age_days(self, va):
        va.age = '12 days'
        assert va.age_years == 0
        assert va.age_days == 12
        assert va.age is None

    def test_va_age_days_parse_error(self, va):
        with pytest.raises(AgeParseError):
            va.age = '12 days butrestiswrong'

    def test_va_age_years_out_of_bounds(self, va):
        with pytest.raises(AgeOutOfBoundsError):
            va.age = '140 years'
        with pytest.raises(AgeOutOfBoundsError):
            va.age = '-10 years'

    def test_va_age_days_out_of_bounds(self, va):
        with pytest.raises(AgeParseError):
            va.age = '50000 days'
        with pytest.raises(AgeParseError):
            va.age = '-2 days'

    def test_va_age_days_to_years(self, va):
        va.age = '400 days'
        assert va.age_years == 1
        assert va.age_days == 400
        assert va.age is None

    def test_va_age_invalid(self, va):
        with pytest.raises(AgeParseError):
            va.age = 'not an age'

        with pytest.raises(AgeParseError):
            va.age = 'not an age days'

        with pytest.raises(AgeParseError):
            va.age = 'not an age years'

        with pytest.raises(AgeOutOfBoundsError):
            va.age = '135 years'

        with pytest.raises(AgeMissingWarning):
            va.age = ''

    def test_va_age_category_adult(self, va):
        va.age = '13 years'
        assert va.age_years == 13
        assert va.age_days == int(round(13 * DAYS_IN_YEAR))
        assert va.age_category == AgeCategory.options['Adult']

    def test_va_age_category_child(self, va):
        va.age = '10 years'
        assert va.age_years == 10
        assert va.age_days == int(round(10 * DAYS_IN_YEAR))
        assert va.age_category == AgeCategory.options['Child']

    def test_va_age_category_neonate(self, va):
        va.age = '12 days'
        assert va.age_years == 0
        assert va.age_days == 12
        assert va.age_category == AgeCategory.options['Neonate']


class TestBirthDate(VaAbstractClass):

    def test_va_birthdate_valid(self, va):
        va.birth_date = '1980-01-01'
        assert va.birth_date == '1980-01-01'

    def test_va_birthdate_invalid(self, va):
        with pytest.raises(BirthDateParseError):
            va.birth_date = 'not a date'


class TestCauseOfDeath(VaAbstractClass):

    def test_va_cause_of_death(self, va):
        va.icd10 = 'B24'
        va.age_in_years = 90
        va.age_category = 1
        assert va.icd10 == 12
        assert va.age_category == 1
        assert va.cause_of_death == 101


class TestDeathDate(VaAbstractClass):

    def test_va_death_date_valid(self, va):
        va.death_date = '2018-01-01'
        assert va.death_date == '2018-01-01'

    def test_va_death_date_invalid(self, va):
        with pytest.raises(DeathDateParseError):
            va.death_date = 'not a date'

    def test_va_death_date_from_interview_date(self, va):
        va.interview_date = '2018-01-25'
        va.death_date = ''
        assert va.death_date == '2018-01-25'

    def test_va_death_date_is_now(self, va):
        va.death_date = ''
        assert va.death_date == datetime.datetime.now().strftime('%Y-%m-%d')


class TestInterviewDate(VaAbstractClass):

    def test_va_interview_date_valid_1(self, va):
        va.interview_date = '2018-03-01'
        assert va.interview_date == '2018-03-01'

    def test_va_interview_date_valid_2(self, va):
        va.interview_date = 'Mar 26, 2018'
        assert va.interview_date == '2018-03-26'

    def test_va_interview_date_invalid(self, va):
        with pytest.raises(InterviewDateParseWarning):
            va.interview_date = 'not a date xx'

    def test_va_interview_date_missing(self, va):
        with pytest.raises(InterviewDateMissingWarning):
            va.interview_date = ''


class TestNames(VaAbstractClass):

    def test_firstname(self, va):
        va.first_name = 'Fritz'
        assert va.first_name == 'Fritz'

    def test_firstname_2nd(self, va):
        va.first_name_2nd = 'Toni'
        assert va.first_name_2nd == 'Toni'

    def test_surname(self, va):
        va.surname = 'König'
        assert va.surname == 'König'

    def test_surname_2nd(self, va):
        va.surname_2nd = 'Akher-Sufi'
        assert va.surname_2nd == 'Akher-Sufi'


class TestIcd10(VaAbstractClass):

    def test_icd10_valid(self, va):
        va.icd10 = 'B24'
        assert va.icd10 == 12

    def test_icd10_missing(self, va):
        with pytest.raises(Icd10MissingError):
            va.icd10 = ''

        with pytest.raises(Icd10MissingError):
            va.icd10 = None


class TestOrgunit(VaAbstractClass):

    def test_orgunit_valid(self, va):
        va.orgunit = 'Aq72mcgPpbH'
        assert va.orgunit == 'Aq72mcgPpbH'

    def test_orgunit_missing(self, va):
        with pytest.raises(OrgunitMissingError):
            va.orgunit = ''

    def test_orgunit_invalid(self, va):
        with pytest.raises(OrgunitNotValidError):
            va.orgunit = 'Not a UID...'


class TestSex(VaAbstractClass):
    def test_sex_valid(self, va):
        for option in Sex.options:
            va.sex = str(option)
            assert va.sex == option

    def test_sex_invalid_numbers(self, va):
        for option in {0, 4, 5, 100}:
            with pytest.raises(SexParseError):
                va.sex = str(option)

    def test_sex_invalid_strings(self, va):
        for option in {'male', 'female', 'uu'}:
            with pytest.raises(SexParseError):
                va.sex = option

    def test_sex_missing(self, va):
        with pytest.raises(SexMissingError):
            va.sex = ''


class TestSid(VaAbstractClass):

    def test_sid_valid(self, va):
        sid = 'VA_12345678912345678'
        va.sid = sid
        assert va.sid == sid

    def test_sid_invalid(self, va):
        with pytest.raises(SidParseError):
            va.sid = 'Not a valid VA ID'

    def test_sid_missing(self, va):
        with pytest.raises(SidMissingError):
            va.sid = ''


class TestNationalId(VaAbstractClass):

    def test_national_id(self, va):
        national_id = 'something'
        va.national_id = 'something'
        assert va.national_id == national_id


class TestAlgorithmVersion(VaAbstractClass):

    def test_algorithm_version(self, va):
        va.algorithm_version = SmartVAConfig.algorithm_version
        assert va.algorithm_version == SmartVAConfig.algorithm_version


class TestQuestionnaireVersion(VaAbstractClass):

    def test_questionnaire_version(self, va):
        va.questionnaire_version = ODKConfig.form_id
        assert va.questionnaire_version == ODKConfig.form_id


class TestVAClassMethods(VaAbstractClass):

    def test_getitem(self, va):
        va.age = '22 years'
        assert va['age_years'] == 22

    def test_setitem(self, va):
        va['age'] = '22 years'
        assert va.age_years == 22

    def test_getattr(self, va):
        assert va.notexistent is None


def test_process_row_data():
    data = {
        'age': '22 years',
        'death_date': '2018-01-01',
        'interview_date': '2018-02-01'
    }
    r = process_row_data(data)
    r.pop(CauseCode.code_name)

    from collections import OrderedDict
    exp = OrderedDict(sorted({
        Age.code_name: '22 years',
        BirthDate.code_name: None,
        FirstName.code_name: None,
        FirstName2nd.code_name: None,
        InterviewDate.code_name: '2018-02-01',
        Orgunit.code_name: None,
        Surname.code_name: None,
        Surname2nd.code_name: None,
        Sex.code_name: None,
        Sid.code_name: None,
        NationalId.code_name: None
    }.items(), key=lambda t: t[0]))

    # those are parsed later
    exp.update({DeathDate.code_name: '2018-01-01'})
    exp.update({Icd10.code_name: None})

    assert r == exp


def test_verbal_autopsy_factory_full():
    data = {
        Age.csv_name: '22 years',
        BirthDate.csv_name: '1990-01-01',
        CauseCode.csv_name: '23',
        CauseOfDeath.csv_name: '1',
        FirstName.csv_name: 'Toni ',
        FirstName2nd.csv_name: '',
        InterviewDate.csv_name: '2018-02-01',
        Surname.csv_name: 'König',
        Surname2nd.csv_name: '',
        Orgunit.csv_name: 'Aq72mcgPpbH',
        Icd10.csv_name: 'B24',
        Sex.csv_name: '1',
        Sid.csv_name: 'VA_12345678912345678',
        NationalId.csv_name: '111222333'
    }
    va, exc, w = verbal_autopsy_factory(data)
    assert isinstance(va, VerbalAutopsy)
    assert va.age_years == 22
    assert va.age_days == 8035
    assert va.age_category == 1
    assert va.age is None
    assert va.birth_date == '1990-01-01'
    assert va.cause_of_death == 101
    assert va.first_name == 'Toni'
    assert va.first_name_2nd is None
    assert va.interview_date == '2018-02-01'
    assert va.surname == 'König'
    assert va.surname_2nd is None
    assert va.orgunit == 'Aq72mcgPpbH'
    assert va.icd10 == 12
    assert va.sex == 1
    assert va.sid == 'VA_12345678912345678'
    assert va.national_id == '111222333'
    assert va.algorithm_version == SmartVAConfig.algorithm_version
    assert va.questionnaire_version == ODKConfig.form_id


def test_verbal_autopsy_factory_exceptions():
    data = {
        Age.csv_name: '',
        BirthDate.csv_name: '',
        CauseCode.csv_name: '',
        CauseOfDeath.csv_name: '',
        FirstName.csv_name: ' ',
        FirstName2nd.csv_name: '',
        InterviewDate.csv_name: '',
        Surname.csv_name: '',
        Surname2nd.csv_name: '',
        Icd10.csv_name: '',
        Sex.csv_name: '',
        Sid.csv_name: ''
    }
    va, exc, war = verbal_autopsy_factory(data)
    assert isinstance(va, VerbalAutopsy)
    assert len(exc) != 0
    assert len(war) != 0
    assert all(isinstance(e, ValidationError) for e in exc)
    assert all(isinstance(w, ValidationWarning) for w in war)


class TestEvent(object):

    @pytest.fixture
    def va(self):
        va_instance = VerbalAutopsy()
        va_instance.age_years = 22
        va_instance.age_category = 1
        va_instance.birth_date = '1990-01-01'
        va_instance.icd10 = 'B24'
        va_instance.first_name = 'Toni'
        va_instance.interview_date = '2018-02-01'
        va_instance.surname = 'König'
        va_instance.sex = 1
        va_instance.sid = 'VA_12345678912345678'
        va_instance.orgunit = 'htJeatF5ITk'
        return va_instance

    def test_event_program(self, va):
        ev = Event(va)
        assert ev.program == 'HPrJOsYuM1K'

    def test_event_orgunit(self, va):
        ev = Event(va)
        assert ev.orgunit == 'htJeatF5ITk'

    def test_event_datavalues(self, va):
        ev = Event(va)

        expected = [
            {"dataElement": AgeInYears.dhis_uid, "value": 22},
            {"dataElement": AgeInDays.dhis_uid, "value": 8035},
            {"dataElement": AgeCategory.dhis_uid, "value": AgeCategory.options["Adult"]},
            {"dataElement": CauseOfDeath.dhis_uid, "value": 101},
            {"dataElement": BirthDate.dhis_uid, "value": "1990-01-01"},
            {"dataElement": DeathDate.dhis_uid, "value": "2018-02-01"},
            {"dataElement": FirstName.dhis_uid, "value": "Toni"},
            {"dataElement": Surname.dhis_uid, "value": "König"},
            {"dataElement": Icd10.dhis_uid, "value": 12},
            {"dataElement": Sex.dhis_uid, "value": 1},
            {"dataElement": Sid.dhis_uid, "value": "VA_12345678912345678"},
            {"dataElement": InterviewDate.dhis_uid, "value": "2018-02-01"},
            {"dataElement": QuestionnaireVersion.dhis_uid, "value": ODKConfig.form_id},
            {"dataElement": AlgorithmVersion.dhis_uid, "value": SmartVAConfig.algorithm_version},
        ]
        pairs = zip(ev.datavalues, expected)
        assert any(x != y for x, y in pairs)

    def test_event_throws_for_non_verbal_autopsy_objects(self):
        va = dict()
        with pytest.raises(ValueError):
            Event(va)
