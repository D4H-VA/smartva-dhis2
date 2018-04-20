import csv
import os
import re

from smartvadhis2.core.config import Config
from smartvadhis2.core.mapping import (
    Mapping,
    CauseOfDeath,
    Sex,
    AgeCategory,
    Icd10,
    cause_of_death_option_code
)


def test_dhis_uid_unique():
    prop = [mapping.dhis_uid for mapping in Mapping.properties() if mapping.dhis_uid is not None]
    assert len(set(prop)) == len(prop)


def test_csv_name_unique():
    prop = [mapping.csv_name for mapping in Mapping.properties() if mapping.csv_name is not None]
    assert len(set(prop)) == len(prop)


def test_code_name_unique():
    prop = [mapping.code_name for mapping in Mapping.properties()]
    assert len(set(prop)) == len(prop)


def test_set_order():
    numbers = [mapping.set_order for mapping in Mapping.properties()]
    assert Mapping.set_order_range() == set(numbers)
    assert set(numbers) == {0, 1, 2}


class TestMetadataMapping(object):

    @staticmethod
    def open_csv(filename):
        with open(os.path.join(Config.ROOT_DIR, 'metadata', filename)) as f:
            reader = csv.DictReader(f, delimiter=',')
            return [row for row in reader]

    def test_data_elements(self):
        data = self.open_csv('dataelements.csv')
        try:
            csv_uids = [de['UID'] for de in data]
        except KeyError:
            csv_uids = [de['id'] for de in data]

        mapping_uids = [m.dhis_uid for m in Mapping.properties() if m.dhis_uid is not None]

        assert set(csv_uids) == set(mapping_uids)

    def test_cause_of_death_optionset(self):
        data = self.open_csv('optionset_cause_of_death.csv')
        rows = [row for row in data if row.get('optionsetname').startswith('VA- Cause of Death')]

        ICD10_REGEX = '(?<=\()(.*?)(?=\))'  # to get ICD10 between (brackets)

        cause_list_adult = [re.search(ICD10_REGEX, r['optionname']).group(1) for r in rows if
                            r['optionname'].startswith('Adult')]
        cause_list_child = [re.search(ICD10_REGEX, r['optionname']).group(1) for r in rows if
                            r['optionname'].startswith('Child')]
        cause_list_neonate = [re.search(ICD10_REGEX, r['optionname']).group(1) for r in rows if
                              r['optionname'].startswith('Neonate')]

        mapping_options_adult = CauseOfDeath.options[1].keys()
        mapping_options_child = CauseOfDeath.options[2].keys()
        mapping_options_neonate = CauseOfDeath.options[3].keys()

        assert set(cause_list_adult) == set(mapping_options_adult)
        assert set(cause_list_child) == set(mapping_options_child)
        assert set(cause_list_neonate) == set(mapping_options_neonate)

        options_adult = [int(v.get('optioncode')) for v in rows if v.get('optionname').startswith('Adult -')]
        options_child = [int(v.get('optioncode')) for v in rows if v.get('optionname').startswith('Child -')]
        options_neonate = [int(v.get('optioncode')) for v in rows if v.get('optionname').startswith('Neonate -')]

        assert len(set(options_adult)) == len(options_adult)
        assert len(set(options_child)) == len(options_child)
        assert len(set(options_neonate)) == len(options_neonate)

        assert all([101 <= v <= 199 for v in options_adult])
        assert all([201 <= v <= 299 for v in options_child])
        assert all([301 <= v <= 399 for v in options_neonate])

    def test_icd10_optionset(self):
        data = self.open_csv('optionset_ICD10.csv')
        rows = [row for row in data if row.get('optionsetname').startswith('VA- ICD10')]

        option_names = [o.get('optionname') for o in rows]
        assert len(option_names) == len(set(option_names))

        option_codes = [o.get('optioncode') for o in rows]
        assert len(option_codes) == len(set(option_codes))
        assert all([1 <= int(o) <= len(option_codes) for o in option_codes])

    def test_sex_optionset(self):
        data = self.open_csv('optionset_sex.csv')
        rows = [row for row in data if row.get('optionsetname').startswith('VA- Sex')]

        options = [v.get('optioncode') for v in rows]
        assert all([int(o) for o in options])
        assert len(options) == len(set(options))
        assert set([int(o) for o in options]) == Sex.options

    def test_age_category_optionset(self):
        data = self.open_csv('optionset_age_category.csv')
        rows = [row for row in data if row.get('optionsetname').startswith('VA- Age Category')]

        options = [v.get('optioncode') for v in rows]
        assert all([int(o) for o in options])
        assert len(options) == len(set(options))
        assert set([int(o) for o in options]) == set(AgeCategory.options.values())

    def test_get_option_code(self):
        assert cause_of_death_option_code(age_category=1, icd10='B24') == 101

    def test_icd10_vs_cause_of_death_options(self):

        icd10_original = list(Icd10.options.keys())
        cod_age_categories = CauseOfDeath.options.keys()

        age_category_icd10 = list()
        for cat in cod_age_categories:
            age_category_icd10.extend(list(CauseOfDeath.options[cat].keys()))

        assert set(icd10_original) == set(age_category_icd10)

