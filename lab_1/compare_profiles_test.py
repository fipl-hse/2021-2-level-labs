# pylint: skip-file
"""
Checks the first lab language comparison function
"""

import unittest
from main import calculate_distance


class CompareProfilesTest(unittest.TestCase):
    """
    Tests profile comparison function
    """

    def test_compare_profiles_ideal(self):
        """
        Ideal scenario
        """
        en_profile = {'name': 'en',
                      'freq': {'happy': 2, 'he': 1, 'man': 1},
                      'n_words': 3}

        de_profile = {'name': 'de',
                      'freq': {'ich': 3, 'weiß': 1, 'nicht': 1, 'machen': 1,
                               'möchte': 1, 'vielleicht': 1, 'überlegen': 1, 'man': 1},
                      'n_words': 8}

        expected = 0.25
        actual = calculate_distance(en_profile, de_profile, 4)
        self.assertEqual(expected, actual)

    def test_compare_profiles_no_intersections_ideal(self):
        """
        Ideal scenario with no intersections
        """
        en_profile = {'name': 'en',
                      'freq': {'happy': 2, 'he': 1, 'man': 1},
                      'n_words': 3}

        de_profile = {'name': 'de',
                      'freq': {'ich': 3, 'weiß': 1, 'nicht': 1, 'machen': 1,
                               'möchte': 1, 'vielleicht': 1, 'überlegen': 1},
                      'n_words': 7}

        expected = 0.0
        actual = calculate_distance(en_profile, de_profile, 4)
        self.assertEqual(expected, actual)

    def test_compare_profiles_identical(self):
        """
        Ideal scenario with identical profiles
        """
        first_profile = {'name': 'en',
                         'freq': {'happy': 2, 'he': 1, 'man': 1},
                         'n_words': 3}

        second_profile = {'name': 'en',
                          'freq': {'happy': 2, 'he': 1, 'man': 1},
                          'n_words': 3}

        expected = 1.0
        actual = calculate_distance(first_profile, second_profile, 2)
        self.assertEqual(expected, actual)

    def test_compare_profiles_bad_input(self):
        """
        Bad input scenario
        """
        en_profile = []

        de_profile = {'name': 'de',
                      'freq': {'ich': 3, 'weiß': 1, 'nicht': 1, 'machen': 1,
                               'möchte': 1, 'vielleicht': 1, 'überlegen': 1},
                      'n_words': 7}

        expected = None
        actual = calculate_distance(en_profile, de_profile, 4)
        self.assertEqual(expected, actual)

    def test_compare_profiles_bad_input_top_n(self):
        """
        Bad input scenario
        """
        en_profile = {'name': 'en',
                      'freq': {'happy': 2, 'he': 1, 'man': 1},
                      'n_words': 3}

        de_profile = {'name': 'de',
                      'freq': {'ich': 3, 'weiß': 1, 'nicht': 1, 'machen': 1,
                               'möchte': 1, 'vielleicht': 1, 'überlegen': 1},
                      'n_words': 7}

        expected = None
        actual = calculate_distance(en_profile, de_profile, dict())
        self.assertEqual(expected, actual)
