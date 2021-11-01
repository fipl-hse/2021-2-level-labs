# pylint: skip-file
"""
Tests for Language Profile (get top frequencies)
"""

import unittest

from lab_3.main import NGramTrie, LetterStorage, encode_corpus, LanguageProfile


class GetTopKBiGramsTest(unittest.TestCase):
    """
    Tests for Language Profile (get top frequencies)
    """

    def test_get_top_k_ideal(self):
        """
        Get top k by frequency
        """

        text = (
            (('_', 'h', 'e', '_'), ('_', 'i', 's', '_'), ('_', 'h', 'a', 'p', 'p', 'y', '_'), ('_', 'h', 'a', '_')),
        )
        storage = LetterStorage()
        storage.update(text)
        encoded_text = encode_corpus(storage, text)
        trie = NGramTrie(n=2, letter_storage=storage)
        trie.extract_n_grams(encoded_text)

        profile = LanguageProfile(letter_storage=storage, language_name='en')
        self.assertEqual(profile.tries, [])
        self.assertEqual(profile.n_words, [])
        self.assertEqual(profile.language, 'en')
        self.assertEqual(profile.storage, storage)

        profile.create_from_tokens(encoded_text, (2,))

        actual = profile.get_top_k_n_grams(2, 2)
        self.assertEqual(len(actual), 2)
        expected = (('_', 'h'), ('h', 'a'))
        for top_ngram in actual:
            decoded = (storage.get_letter_by_id(letter_id) for letter_id in top_ngram)
            self.assertIn(tuple(decoded), expected)

    def test_get_top_k_bad_inputs(self):
        """
        Tests with bad inputs
        """

        text = (
            (('_', 'h', 'e', '_'), ('_', 'i', 's', '_'), ('_', 'h', 'a', 'p', 'p', 'y', '_')),
        )
        storage = LetterStorage()
        storage.update(text)

        profile = LanguageProfile(letter_storage=storage, language_name='en')

        bad_inputs = [None, 'asd', LetterStorage]
        for bad_input in bad_inputs:
            actual = profile.get_top_k_n_grams(bad_input, 2)
            self.assertEqual(actual, ())

        for bad_input in bad_inputs:
            actual = profile.get_top_k_n_grams(2, bad_input)
            self.assertEqual(actual, ())
