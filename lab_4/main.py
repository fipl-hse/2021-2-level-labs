"""
Lab 4
Language generation algorithm based on language profiles
"""

from typing import Tuple
from lab_4.storage import Storage
from lab_4.language_profile import LanguageProfile
import re


# 4
def tokenize_by_letters(text: str) -> Tuple or int:
    """
    Tokenizes given sequence by letters
    """
    pass
    if not isinstance(text, str):
        return -1
    useless_symbols = ['`', '~', '@', '*', '#', '$', '%', '^', '&', '(', ')', '_', '-', '+',
                       '=', '{', '[', ']', '}', '|', '\\', ':', ';', '"', "'", '<', ',', '>',
                       '/', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
    patterns = ('ö', 'ü', 'ä', 'ß')
    replacements = ('oe', 'ue', 'ae', 'ss')
    if text:
        last_letter = text[-1]
        if last_letter in ('.', '!', '?'):
            text = text[:-1]
    for symbol in useless_symbols:
        text = text.replace(symbol, '')
    if not text:
        return ()
    sentences = re.split(r'[.!?] ?', text.lower())
    text_output = []
    for sentence in sentences:
        tokens = sentence.split()
        for token in tokens:
            for pattern, replacement in zip(patterns, replacements):
                token.replace(pattern, replacement)
            letters = []
            letters.insert(0, '_')
            for letter in token:
                letters.append(letter)
            letters.append('_')
            text_output.append(tuple(letters))
    return tuple(text_output)


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
        pass
        if not isinstance(elements, tuple):
            return -1
        return super().update(elements)

    def get_letter_count(self) -> int:
        """
        Gets the number of letters in the storage
        """
        pass
        if not self.storage:
            return -1
        return len(self.storage.keys())


# 4
def encode_corpus(storage: LetterStorage, corpus: tuple) -> tuple:
    """
    Encodes corpus by replacing letters with their ids
    :param storage: an instance of the LetterStorage class
    :param corpus: a tuple of tuples
    :return: a tuple of the encoded letters
    """
    pass
    if not isinstance(storage, LetterStorage) or not isinstance(corpus, tuple):
        return ()
    storage.update(corpus)
    encoded_corpus = tuple(tuple(storage.get_id(element) for element in word) for word in corpus)
    return encoded_corpus


# 4
def decode_sentence(storage: LetterStorage, sentence: tuple) -> tuple:
    """
    Decodes sentence by replacing letters with their ids
    :param storage: an instance of the LetterStorage class
    :param sentence: a tuple of tuples-encoded words
    :return: a tuple of the decoded sentence
    """
    pass
    if not isinstance(storage, LetterStorage) or not isinstance(sentence, tuple):
        return ()
    decoded_sentences = tuple(tuple(storage.get_element(element_id) for element_id in word) for word in sentence)
    return decoded_sentences


# 6
class NGramTextGenerator:
    """
    Language model for basic text generation
    """

    def __init__(self, language_profile: LanguageProfile):
        pass

    def _generate_letter(self, context: tuple) -> int:
        """
        Generates the next letter.
            Takes the letter from the most
            frequent ngram corresponding to the context given.
        """
        pass

    def _generate_word(self, context: tuple, word_max_length=15) -> tuple:
        """
        Generates full word for the context given.
        """
        pass

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
