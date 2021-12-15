"""
Lab 4
Language generation algorithm based on language profiles
"""
import json
from typing import Tuple
from lab_4.storage import Storage
from lab_4.language_profile import LanguageProfile, NGramTrie


# 4
def tokenize_by_letters(text: str) -> Tuple or int:
    """
    Tokenizes given sequence by letters
    """
    if not isinstance(text, str):
        return -1

    # words = [word.lower().strip() for word in text.split(" ") if word]
    # text_tuple = tuple(tuple(letter for letter in word if letter.isalpha()) for word in words)

    text = "".join(letter for letter in text if letter.isalpha() or letter.isspace())
    text_tuple = tuple(tuple("_"+word+"_") for word in text.lower().strip().split())
    return text_tuple


# 4
class LetterStorage(Storage):
    """
    Stores letters and their ids
    """

    def update(self, elements: tuple) -> int:
        """
        Fills a storage by letters from the tuple
        :param elements: a tuple of tuples of letters
        :return: 0 if succeeds, -1 if not
        """
        if not isinstance(elements, tuple):
            return -1
        for word in elements:
            for letter in word:
                self._put(letter)
        return 0

    def get_letter_count(self) -> int:
        """
        Gets the number of letters in the storage
        """
        if not self.storage:
            return -1
        return len(self.storage)


# 4
def encode_corpus(storage: LetterStorage, corpus: tuple) -> tuple:
    """
    Encodes corpus by replacing letters with their ids
    :param storage: an instance of the LetterStorage class
    :param corpus: a tuple of tuples
    :return: a tuple of the encoded letters
    """
    if not (isinstance(storage, LetterStorage) and isinstance(corpus, tuple)):
        return ()
    storage.update(corpus)
    encoded_sentences = tuple(tuple(storage.get_id(letter)
                                    for letter in word)
                              for word in corpus)
    return encoded_sentences


# 4
def decode_sentence(storage: LetterStorage, sentence: tuple) -> tuple:
    """
    Decodes sentence by replacing letters with their ids
    :param storage: an instance of the LetterStorage class
    :param sentence: a tuple of tuples-encoded words
    :return: a tuple of the decoded sentence
    """
    if not (isinstance(storage, LetterStorage) and isinstance(sentence, tuple)):
        return ()
    decoded_sentences = tuple(tuple(storage.get_element(letter)
                                    for letter in word)
                              for word in sentence)
    return decoded_sentences


# 6
class NGramTextGenerator:
    """
    Language model for basic text generation
    """

    def __init__(self, language_profile: LanguageProfile):
        self.language_profile = language_profile
        self._used_n_grams = []

    def _generate_letter(self, context: tuple) -> int:
        """
        Generates the next letter.
            Takes the letter from the most
            frequent ngram corresponding to the context given.
        """
        if not isinstance(context, tuple):
            return -1

        if len(context) + 1 not in [trie.size for trie in self.language_profile.tries]:
            return -1

        frequencies = {}

        for trie in self.language_profile.tries:
            if trie.size == len(context) + 1:
                for n_gram, freq in trie.n_gram_frequencies.items():
                    if n_gram[:-1] == context and n_gram not in self._used_n_grams:
                        frequencies[n_gram] = freq

                if not frequencies:
                    for n_gram, freq in trie.n_gram_frequencies.items():
                        if n_gram not in self._used_n_grams:
                            frequencies[n_gram] = freq

                    self._used_n_grams = []
                    for n_gram, freq in trie.n_gram_frequencies.items():
                        if n_gram[:-1] == context:
                            frequencies[n_gram] = freq

                if not frequencies:
                    return -1

        n_gram = max(frequencies, key=frequencies.get)
        self._used_n_grams.append(n_gram)
        return n_gram[-1]

    def _generate_word(self, context: tuple, word_max_length=15) -> tuple:
        """
        Generates full word for the context given.
        """
        # ПРОБЛЕМА

        if not (isinstance(context, tuple) and isinstance(word_max_length, int)):
            return ()

        generated_word = list(context)

        letter = None

        while not (len(generated_word) == word_max_length
                   or letter == self.language_profile.storage.get_special_token_id()):
            letter = self._generate_letter(context)
            context = *context[1:], letter
            generated_word.append(letter)

        if word_max_length == 1:
            generated_word.append(self.language_profile.storage.get_special_token_id())

        if len(generated_word) == word_max_length:
            generated_word.append(self.language_profile.storage.get_special_token_id())

        return tuple(generated_word)

    def generate_sentence(self, context: tuple, word_limit: int) -> tuple:
        """
        Generates full sentence with fixed number of words given.
        """
        # ПРОБЛЕМА

        if not isinstance(context, tuple) or not isinstance(word_limit, int):
            return ()

        generated_sentence = []

        while len(generated_sentence) != word_limit:
            word = self._generate_word(context)
            generated_sentence.append(word)
            context = tuple(word[-1:])

        return tuple(generated_sentence)

    def generate_decoded_sentence(self, context: tuple, word_limit: int) -> str:
        """
        Generates full sentence and decodes it
        """
        if not isinstance(context, tuple) or not isinstance(word_limit, int):
            return ""

        sentence = self.generate_sentence(context, word_limit)
        letters = [self.language_profile.storage.get_element(i) for word in sentence for i in word]
        text = "".join(letters).replace("__", " ").replace("_", "").capitalize() + "."

        return text


# 6
def translate_sentence_to_plain_text(decoded_corpus: tuple) -> str:
    """
    Converts decoded sentence into the string sequence
    """
    if not isinstance(decoded_corpus, tuple) or not decoded_corpus:
        return ""

    letters = [letter for word in decoded_corpus for letter in word]
    text = "".join(letters).replace("__", " ").replace("_", "").capitalize() + "."

    return text


# 8
class LikelihoodBasedTextGenerator(NGramTextGenerator):
    """
    Language model for likelihood based text generation
    """

    def _calculate_maximum_likelihood(self, letter: int, context: tuple) -> float:
        """
        Calculates maximum likelihood for a given letter
        :param letter: a letter given
        :param context: a context for the letter given
        :return: float number, that indicates maximum likelihood
        """
        if not (isinstance(letter, int) and isinstance(context, tuple) and context):
            return -1

        letter_freq = 0
        sequence_freq = 0

        for trie in self.language_profile.tries:
            if trie.size == len(context) + 1:
                for n_gram, frequency in trie.n_gram_frequencies.items():
                    if n_gram[:len(context)] == context and n_gram[-1] == letter:
                        letter_freq += frequency
                    if n_gram[:len(context)] == context:
                        sequence_freq += frequency
            if sequence_freq == 0:
                return 0.0

        return letter_freq / sequence_freq

    def _generate_letter(self, context: tuple) -> int:
        """
        Generates the next letter.
            Takes the letter with highest
            maximum likelihood frequency.
        """
        if not (isinstance(context, tuple) and self.language_profile.tries and context):
            return -1

        frequencies_m_l = {}

        for trie in self.language_profile.tries:
            if trie.size == len(context) + 1:
                for n_gram in trie.n_gram_frequencies:
                    if n_gram[:-1] == context:
                        frequencies_m_l[n_gram] = self._calculate_maximum_likelihood(n_gram[-1],
                                                                                     context)

        if not frequencies_m_l:
            for trie in self.language_profile.tries:
                if trie.size == 1:
                    return max(trie.n_gram_frequencies, key=trie.n_gram_frequencies.get)[-1]

        return max(frequencies_m_l.keys(), key=frequencies_m_l.get)[-1]


# 10
class BackOffGenerator(NGramTextGenerator):
    """
    Language model for back-off based text generation
    """

    def _generate_letter(self, context: tuple) -> int:
        """
        Generates the next letter.
            Takes the letter with highest
            available frequency for the corresponding context.
            if no context can be found, reduces the context size by 1.
        """
        pass


# 10
class PublicLanguageProfile(LanguageProfile):
    """
    Language Profile to work with public language profiles
    """

    def open(self, file_name: str) -> int:
        """
        Opens public profile and adapts it.
        :return: o if succeeds, 1 otherwise
        """
        pass
