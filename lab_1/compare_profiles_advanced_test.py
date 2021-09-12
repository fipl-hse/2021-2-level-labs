# pylint: skip-file
"""
Checks the first lab language comparison function
"""

import unittest
from main import compare_profiles_advanced


class CompareProfilesAdvancedTest(unittest.TestCase):
    """
    Tests profile comparison advanced  function
    """

    def test_compare_profiles_ideal(self):
        """
        Ideal scenario
        """
        en_profile = {'name': 'en',
                      'freq': {'happy': 2, 'he': 1, 'man': 1, 'a': 2},
                      'n_words': 3}

        unk_profile = {'name': 'unk',
                       'freq': {'ich': 3, 'weiß': 1, 'nicht': 1, 'machen': 1,
                                'möchte': 1, 'vielleicht': 1, 'überlegen': 1, 'man': 1, 'a': 3},
                       'n_words': 9}

        expected = {'name': 'en',
                    'common': ['a', 'man'],
                    'score': 0.222,
                    'max_length_word': 'man',
                    'min_length_word': 'a',
                    'average_token_length': 2.75,
                    'sorted_common': ['a', 'man']}

        actual = compare_profiles_advanced(unk_profile, en_profile, 2)
        self.assertEqual(expected, actual)

    def test_compare_profiles_ideal_deutsch(self):
        """
        Ideal scenario with deutsch
        """
        unk_profile = {'name': 'de',
                       'freq': {'ich': 5, 'weiß': 1, 'nicht': 1,
                                'staat': 2, 'wunderbar': 1, 'möchte': 1},
                       'n_words': 6}

        de_profile = {'name': 'de',
                      'freq': {'ich': 3, 'weiß': 1, 'nicht': 1, 'machen': 1,
                               'möchte': 1, 'vielleicht': 1, 'überlegen': 1, 'man': 1},
                      'n_words': 8}

        expected = {'name': 'de',
                    'common': ['möchte', 'nicht', 'weiß', 'ich'],
                    'score': 0.714,
                    'max_length_word': 'möchte',
                    'min_length_word': 'ich',
                    'average_token_length': 5.75,
                    'sorted_common': ['ich', 'möchte', 'nicht', 'weiß']}

        actual = compare_profiles_advanced(unk_profile, de_profile, 4)
        self.assertEqual(expected, actual)

    def test_compare_profiles_bad_input(self):
        """
        Bad input scenario
        """
        unk_profile = [{'name': 'de',
                        'freq': {'ich': 5, 'weiß': 1, 'nicht': 1,
                                 'staat': 2, 'wunderbar': 1, 'möchte': 1},
                        'n_words': 6}]

        de_profile = {'name': 'de',
                      'freq': {'ich': 3, 'weiß': 1, 'nicht': 1, 'machen': 1,
                               'möchte': 1, 'vielleicht': 1, 'überlegen': 1, 'man': 1},
                      'n_words': 8}

        expected = None

        actual = compare_profiles_advanced(unk_profile, de_profile, 4)
        self.assertEqual(expected, actual)

    def test_compare_profiles_bad_input_top_n(self):
        """
        Bad input scenario
        """
        unk_profile = {'name': 'de',
                       'freq': {'ich': 5, 'weiß': 1, 'nicht': 1,
                                'staat': 2, 'wunderbar': 1, 'möchte': 1},
                       'n_words': 6}

        de_profile = {'name': 'de',
                      'freq': {'ich': 3, 'weiß': 1, 'nicht': 1, 'machen': 1,
                               'möchte': 1, 'vielleicht': 1, 'überlegen': 1, 'man': 1},
                      'n_words': 8}

        expected = None

        actual = compare_profiles_advanced(unk_profile, de_profile, [])
        self.assertEqual(expected, actual)
