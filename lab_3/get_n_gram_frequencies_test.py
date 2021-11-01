# pylint: skip-file
"""
Tests for NGramTrie (frequencies calculation)
"""

import unittest

from lab_3.main import NGramTrie, LetterStorage, encode_corpus


class CalculateNgramFrequenciesTest(unittest.TestCase):
    """
    checks for NGram storage (frequencies calculation).
    """

    def test_calculate_ngram_frequencies_ideal(self):
        """
        Calculate n-gram frequencies
        """

        text = (
            (('_', 'h', 'e', '_'), ('_', 'i', 's', '_'), ('_', 'h', 'a', 'p', 'p', 'y', '_')),
        )
        storage = LetterStorage()
        storage.update(text)
        encoded_text = encode_corpus(storage, text)
        trie = NGramTrie(n=2, letter_storage=storage)
        trie.extract_n_grams(encoded_text)
        self.assertEqual(trie.get_n_grams_frequencies(), 0)

        expected = {
            (1, 2): 2, (2, 3): 1,
            (3, 1): 1, (1, 4): 1,
            (4, 5): 1, (5, 1): 1,
            (2, 6): 1, (6, 7): 1,
            (7, 7): 1, (7, 8): 1,
            (8, 1): 1
        }

        self.assertEqual(expected, trie.n_gram_frequencies)

    def test_calculate_ngram_frequencies_empty(self):
        """
        Test with empty input
        """

        storage = LetterStorage()
        trie = NGramTrie(n=2, letter_storage=storage)
        empty_encoded_text = ()
        trie.extract_n_grams(empty_encoded_text)
        self.assertEqual(trie.get_n_grams_frequencies(), 1)
        self.assertTrue(not trie.n_gram_frequencies)
