class Mapping(object):
    """ Base class for Mappings"""

    @classmethod
    def properties(cls):
        return cls.__subclasses__()

    @classmethod
    def set_order_range(cls):
        return set([c.set_order for c in cls.__subclasses__()])


class Age(Mapping):
    set_order = 0
    csv_name = 'age'
    code_name = 'age'
    dhis_uid = None


class AgeInYears(Mapping):
    set_order = 0
    csv_name = None
    code_name = 'age_years'
    dhis_uid = 'C2OT4YktNGX'


class AgeInDays(Mapping):
    set_order = 0
    csv_name = None
    code_name = 'age_days'
    dhis_uid = 'NsmhGfGhFRO'


class AgeCategory(Mapping):
    set_order = 0
    csv_name = None
    code_name = 'age_category'
    dhis_uid = 'lFKqfDj9Rhk'

    options = {
        "Adult": 1,
        "Child": 2,
        "Neonate": 3
    }


class CauseCode(Mapping):
    set_order = 0
    csv_name = 'cause list #'
    code_name = 'cause_code'
    dhis_uid = None


class CauseOfDeath(Mapping):
    set_order = 2
    csv_name = None
    code_name = 'cause_of_death'
    dhis_uid = 'EGuQ4jmbsjc'

    options = {
        1: {
            'B24': 101,
            'X27': 103,
            'C50': 104,
            'C53': 105,
            'K74': 106,
            'C18': 107,
            'E14': 109,
            'A09': 110,
            'W74': 111,
            'G40': 112,
            'C15': 113,
            'W19': 114,
            'X09': 115,
            'Y09': 116,
            'C96': 118,
            'C34': 119,
            'B54': 120,
            'O95': 121,
            'I99': 122,
            'B99': 123,
            'X58': 124,
            'R100': 125,
            'J22': 126,
            'X49': 127,
            'C61': 128,
            'N18': 129,
            'V89': 130,
            'C16': 131,
            'I64': 132,
            'X84': 133,
            'A16': 134,
            'J44': 135,
            'I24': 136,
            'C76': 137,
            'R99': 199
        },
        2: {
            'B24': 201,
            'X27': 202,
            'A09': 203,
            'W74': 204,
            'G04': 205,
            'W19': 206,
            'X09': 207,
            'A99': 208,
            'B54': 209,
            'B05': 210,
            'G03': 211,
            'C76': 212,
            'I99': 213,
            'R101': 214,
            'K92': 215,
            'B99': 216,
            'J22': 217,
            'X49': 218,
            'V89': 219,
            'A41': 220,
            'Y09': 221,
            'R99': 299,
        },
        3: {
            'P21': 301,
            'Q89': 302,
            'P36': 303,
            'P23': 304,
            'P07': 305,
            'P95': 306,
            'R99': 399,
        }
    }

class BirthDate(Mapping):
    set_order = 0
    csv_name = 'birth_date'
    code_name = 'birth_date'
    dhis_uid = 'ih4W8j2jDAS'


class DeathDate(Mapping):
    set_order = 1
    csv_name = 'death_date'
    code_name = 'death_date'
    dhis_uid = None


class FirstName(Mapping):
    set_order = 0
    csv_name = 'name'
    code_name = 'first_name'
    dhis_uid = 'uWGd9pUSgBK'


class FirstName2nd(Mapping):
    set_order = 0
    csv_name = 'name2'
    code_name = 'first_name_2nd'
    dhis_uid = 'd52GkmmpLMM'


class Surname(Mapping):
    set_order = 0
    csv_name = 'surname'
    code_name = 'surname'
    dhis_uid = 'NM9CFZmYq9S'


class Surname2nd(Mapping):
    set_order = 0
    csv_name = 'surname2'
    code_name = 'surname_2nd'
    dhis_uid = 'VEGzj76HCEN'


class Orgunit(Mapping):
    set_order = 0
    csv_name = 'geography3'
    code_name = 'orgunit'
    dhis_uid = None


class Icd10(Mapping):
    set_order = 1
    csv_name = 'icd10'
    code_name = 'icd10'
    dhis_uid = 'TSljgUq6Xfd'

    options = {
        "X58": 1,
        "I24": 2,
        "P07": 3,
        "A09": 4,
        "E14": 5,
        "P21": 6,
        "W74": 7,
        "B54": 8,
        "P95": 9,
        "G03": 10,
        "V89": 11,
        "B24": 12,
        "X09": 13,
        "P23": 14,
        "C16": 15,
        "I64": 16,
        "C76": 17,
        "N18": 18,
        "X84": 19,
        "C96": 20,
        "J22": 21,
        "B99": 22,
        "K74": 23,
        "A99": 24,
        "G04": 25,
        "J44": 26,
        "G40": 27,
        "R99": 28,
        "C18": 29,
        "C34": 30,
        "K92": 31,
        "C61": 32,
        "C15": 33,
        "X27": 34,
        "C50": 35,
        "O95": 36,
        "A41": 37,
        "A16": 38,
        "I99": 39,
        "C53": 40,
        "P36": 41,
        "R101": 42,
        "Y09": 43,
        "X49": 44,
        "R100": 45,
        "Q89": 46,
        "B05": 47,
        "W19": 48,
    }

    reverse = {v: k for k, v in options.items()}


class InterviewDate(Mapping):
    set_order = 0
    csv_name = 'interview_date'
    code_name = 'interview_date'
    dhis_uid = 't6O2A1gou0g'


class Sex(Mapping):
    set_order = 0
    csv_name = 'sex'
    code_name = 'sex'
    dhis_uid = 'GVVDthqI2Sz'

    options = {
        1,  # male
        2,  # female
        3,  # third gender
        8,  # don't know
        9   # refused to answer
    }


class Sid(Mapping):
    set_order = 0
    csv_name = 'sid'
    code_name = 'sid'
    dhis_uid = 'L370gG5pb3P'


class NationalId(Mapping):
    set_order = 0
    csv_name = 'national_id'
    code_name = 'national_id'
    dhis_uid = 'iJzYZN4MIjD'


class AlgorithmVersion(Mapping):
    set_order = 0
    csv_name = None
    code_name = 'algorithm_version'
    dhis_uid = 'ePYyHl0VfmB'


class QuestionnaireVersion(Mapping):
    set_order = 0
    csv_name = None
    code_name = 'questionnaire_version'
    dhis_uid = 'qQuck3LgWeY'


def cause_of_death_option_code(age_category, icd10):
    if icd10 in Icd10.options.keys():
        return CauseOfDeath.options[age_category][icd10]
    else:
        original_code_lookup = Icd10.reverse[icd10]
        return CauseOfDeath.options[age_category][original_code_lookup]
