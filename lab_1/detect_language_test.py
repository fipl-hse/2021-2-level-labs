# pylint: skip-file
"""
Checks the first lab language detection function
"""

import unittest
from main import detect_language


class DetectLanguageTest(unittest.TestCase):
    """
    Tests language detection function
    """

    def test_detect_language_ideal(self):
        """
        Ideal scenario
        """

        unknown_profile = {'name': 'unk',
                           'freq': {'happy': 5, 'she': 2, 'man': 1},
                           'n_words': 3}

        en_profile = {'name': 'en',
                      'freq': {'happy': 2, 'he': 1, 'man': 1},
                      'n_words': 3}

        de_profile = {'name': 'de',
                      'freq': {'ich': 3, 'weiß': 1, 'nicht': 1, 'machen': 1,
                               'möchte': 1, 'vielleicht': 1, 'überlegen': 1, 'man': 1},
                      'n_words': 8}

        expected = en_profile['name']
        actual = detect_language(unknown_profile, en_profile, de_profile)
        self.assertEqual(expected, actual)

    def test_detect_language_ideal(self):
        """
        Ideal scenario
        """

        unknown_profile = {'name': 'unk',
                           'freq': {'happy': 5, 'she': 2, 'man': 1},
                           'n_words': 3}

        en_profile = {'name': 'en',
                      'freq': {'happy': 2, 'he': 1, 'man': 1},
                      'n_words': 3}

        de_profile = {'name': 'de',
                      'freq': {'ich': 3, 'weiß': 1, 'nicht': 1, 'machen': 1,
                               'möchte': 1, 'vielleicht': 1, 'überlegen': 1, 'man': 1},
                      'n_words': 8}

        expected = en_profile['name']
        actual = detect_language(unknown_profile, en_profile, de_profile)
        self.assertEqual(expected, actual)
