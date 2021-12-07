"""
Lab 4
Language generation algorithm based on language profiles
"""

from typing import Tuple
from lab_4.storage import Storage
from lab_4.language_profile import LanguageProfile


# 4
def tokenize_by_letters(text: str) -> Tuple or int:
    """
    Tokenizes given sequence by letters
    """
    if not isinstance(text, str):
        return -1
    # remove punctuation
    text = "".join(letter for letter in text if letter.isalpha() or letter.isspace())
    # tokenize
    return tuple(tuple(f"_{word}_") for word in text.lower().split())


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
        for token in elements:
            for letter in token:
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
    return tuple(tuple(storage.get_id(letter) for letter in token) for token in corpus)


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
    return tuple(tuple(storage.get_element(letter) for letter in token) for token in sentence)


# 6
class NGramTextGenerator:
    """
    Language model for basic text generation
    """

    def __init__(self, language_profile: LanguageProfile):
        self.profile = language_profile
        self._used_n_grams = []

    def get_trie_by_level(self, trie_level: int):
        """
        Gets NGramTrie of the requested N-gram size
        :param trie_level: N-gram size
        :return: NGramTrie if succeeds, None if not
        """
        for trie in self.profile.tries:
            if trie.size == trie_level:
                return trie
        return None

    def _generate_letter(self, context: tuple) -> int:
        """
        Generates the next letter.
            Takes the letter from the most
            frequent ngram corresponding to the context given.
        """
        if not isinstance(context, tuple):
            return -1
        trie = self.get_trie_by_level(len(context) + 1)
        if not trie:
            return -1
        # exclude N-gram frequencies that do not abide by the context
        # or that have already been used
        frequencies = {n_gram: freq for n_gram, freq in trie.n_gram_frequencies.items()
                       if n_gram[:-1] == context and n_gram not in self._used_n_grams}
        # print(frequencies)
        # print(self.profile.storage.storage)
        if not frequencies:
            # ignore context
            frequencies = {n_gram: freq for n_gram, freq in trie.n_gram_frequencies.items()
                           if n_gram not in self._used_n_grams}
        # print(frequencies)
        # print(self.profile.storage.storage)
        if not frequencies:
            # clear self._used_n_grams, try again
            self._used_n_grams = []
            frequencies = {n_gram: freq for n_gram, freq in trie.n_gram_frequencies.items()
                           if n_gram[:-1] == context}
        if not frequencies:
            return -1
        # print(frequencies)
        # print(self.profile.storage.storage)
        # if not frequencies:
            # ignore context again. is this necessary? no idea.
            # it seems like something that might occur, though.
            # frequencies = {n_gram: freq for n_gram, freq in trie.n_gram_frequencies.items()}
        # print(frequencies)
        # print(self.profile.storage.storage)
        n_gram = max(frequencies, key=frequencies.get)
        self._used_n_grams.append(n_gram)
        return n_gram[-1]

    def _generate_word(self, context: tuple, word_max_length=15) -> tuple:
        """
        Generates full word for the context given.
        """
        if not isinstance(context, tuple) or not isinstance(word_max_length, int):
            return ()
        token = [*context]
        letter = None
        print(self.profile.storage.storage)
        while not (letter == self.profile.storage.get_special_token_id()
                   or len(token) > word_max_length + 1):
            letter = self._generate_letter(context)
            context = *context[1:], letter
            token.append(letter)
            print(context)
        return tuple(token)

    def generate_sentence(self, context: tuple, word_limit: int) -> tuple:
        """
        Generates full sentence with fixed number of words given.
        """
        pass

    def generate_decoded_sentence(self, context: tuple, word_limit: int) -> str:
        """
        Generates full sentence and decodes it
        """
        pass


# 6
def translate_sentence_to_plain_text(decoded_corpus: tuple) -> str:
    """
    Converts decoded sentence into the string sequence
    """
    pass


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
        pass

    def _generate_letter(self, context: tuple) -> int:
        """
        Generates the next letter.
            Takes the letter with highest
            maximum likelihood frequency.
        """
        pass


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
