# pylint: skip-file
"""
Tests encode_corpus function
"""

import unittest

from main import LetterStorage
from main import encode_corpus


class EncodeCorpusTest(unittest.TestCase):
    """
    checks for encode_corpus function.
    """

    def test_encode_corpus_ideal(self):
        """
        Tests that encode_corpus function
            generates id for each character
        """
        letter_storage = LetterStorage()

        sentences = (
            ('_', 't', 'e', 's', 't', '_'),
            ('_', 's', 'e', 'c', 'o', 'n', 'd', '_')
        )

        actual = encode_corpus(letter_storage, sentences)
        for text in actual:
            for character in text:
                self.assertTrue(isinstance(character, int))

    def test_encode_corpus_same_characters_count(self):
        """
        Tests that encode_corpus function
            can assign correct id to the same character
        """
        letter_storage = LetterStorage()

        sentences = (
            ('_', 't', 'e', 's', 't', '_'),
            ('_', 't', 'e', 's', 't', '_')
        )

        actual = encode_corpus(letter_storage, sentences)
        self.assertEqual(actual[0][0], actual[1][0])

    def test_encode_corpus_inappropriate_sentence(self):
        """
        Tests that encode_corpus function
            can handle inappropriate sentence inputs
        """
        letter_storage = LetterStorage()
        bad_inputs = [None, 123, 'test', [], {}]

        expected = ()
        for bad_input in bad_inputs:
            actual = encode_corpus(letter_storage, bad_input)
            self.assertEqual(expected, actual)

    def test_encode_corpus_inappropriate_storage_instance(self):
        """
        Tests that encode_corpus function
            can handle inappropriate storage instance inputs
        """
        bad_inputs = [None, 123, 'test', [], {}]

        sentences = (
            ('_', 't', 'e', 's', 't', '_'),
            ('_', 's', 'e', 'c', 'o', 'n', 'd', '_')
        )

        expected = ()
        for bad_input in bad_inputs:
            actual = encode_corpus(bad_input, sentences)
            self.assertEqual(expected, actual)

    def test_encode_corpus_empty_sentence(self):
        """
        Tests that encode_corpus function
            can handle empty sentence input
        """
        letter_storage = LetterStorage()
        sentences = ()

        expected = ()
        actual = encode_corpus(letter_storage, sentences)
        self.assertEqual(expected, actual)
