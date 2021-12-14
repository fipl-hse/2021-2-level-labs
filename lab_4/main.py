"""
Lab 4
Language generation algorithm based on language profiles
"""
import re
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
    words = []
    text = text.lower()
    text = re.split(r'[.!?]', text)
    new_text = ''
    for sentence in text:
        for symbol in sentence:
            if symbol.isalpha() or symbol.isspace():
                new_text += symbol
    new_text = new_text.split()
    for word in new_text:
        framed_letters = []
        for letter in word:
            framed_letters.append(letter)
        framed_letters.insert(0, '_')
        framed_letters.append('_')
        words.append(framed_letters)
    text_tuple = (tuple(word) for word in words)
    return tuple(text_tuple)


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
        super().update(elements)
        return 0

    def get_letter_count(self) -> int:
        """
        Gets the number of letters in the storage
        """
        if len(self.storage) == 0:
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
        possibilities = {}
        for trie in self.language_profile.tries:
            if trie.size == len(context)+1:
                for key, value in trie.n_gram_frequencies.items():
                    if self._used_n_grams == list(trie.n_gram_frequencies.keys()):
                        self._used_n_grams = []
                    elif key[:-1] == context and key not in self._used_n_grams:
                        possibilities[key] = value
                if possibilities:
                    max_possible = max(possibilities.keys(), key=possibilities.get)
                    self._used_n_grams.append(max_possible)
                else:
                    max_possible = max(trie.n_gram_frequencies.keys(), key=trie.n_gram_frequencies.get)
                return max_possible[-1]
            else:
                return -1

    def _generate_word(self, context: tuple, word_max_length=15) -> tuple:
        """
        Generates full word for the context given.
        """
        if not isinstance(context, tuple) or not isinstance(word_max_length, int):
            return ()
        generated_word = list(context)
        if word_max_length == 1:
            generated_word.append(self.language_profile.storage.get_special_token_id())
            return tuple(generated_word)
        while len(generated_word) != word_max_length:
            symbol = self._generate_letter(context)
            generated_word.append(symbol)
            if symbol == self.language_profile.storage.get_special_token_id():
                break
            context = tuple(generated_word[-len(context):])
        return tuple(generated_word)

    def generate_sentence(self, context: tuple, word_limit: int) -> tuple:
        """
        Generates full sentence with fixed number of words given.
        """
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
        string = ""
        for elem in sentence:
            for symbol in elem:
                string += self.language_profile.storage.get_element(symbol)
        string = string.replace('__', ' ').replace('_', '').capitalize()+'.'
        return string


# 6
def translate_sentence_to_plain_text(decoded_corpus: tuple) -> str:
    """
    Converts decoded sentence into the string sequence
    """
    if not isinstance(decoded_corpus, tuple) or not decoded_corpus:
        return ""
    raw_result = ""
    for word in decoded_corpus:
        for symbol in word:
            raw_result += symbol
    result = raw_result.replace('__', ' ').replace('_', '').capitalize() + '.'
    return result


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
