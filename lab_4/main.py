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
    return_text = ""
    return_list = []
    for letter in text:
        if letter.isalpha() or letter.isspace():
            return_text += return_text.join(letter)
    for word in return_text.lower().strip().split():
        return_list.append(tuple("_" + word + "_"))
    return tuple(return_list)


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
                if self._put(letter) == -1:
                    return -1
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
    encoded_sentences = tuple(tuple(storage.get_id(letter) for letter in word) for word in corpus)
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
    storage.update(sentence)
    decoded_sentences = tuple(tuple(storage.get_element(letter) for letter in word) for word in sentence)
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
        return_list = []
        for trie in self.language_profile.tries:
            if trie.size == len(context) + 1:
                for n_gram, freq in trie.n_gram_frequencies.items():
                    if n_gram[:-1] == context and n_gram not in self._used_n_grams:
                        return_list.append((n_gram, freq))
            if not return_list:
                for n_gram, freq in trie.n_gram_frequencies.items():
                    if n_gram not in self._used_n_grams:
                        return_list.append((n_gram, freq))
            if not return_list:
                self._used_n_grams = []
                for n_gram, freq in trie.n_gram_frequencies.items():
                    if n_gram[:-1] == context and n_gram not in self._used_n_grams:
                        return_list.append((n_gram, freq))
        if not return_list:
            return -1
        return_list = sorted(return_list, key=lambda x: x[1], reverse=True)
        self._used_n_grams.append(return_list[0][0])
        letter = return_list[0][0][-1]
        return letter

    def _generate_word(self, context: tuple, word_max_length=15) -> tuple:
        """
        Generates full word for the context given.
        """
        if not isinstance(context, tuple) or not isinstance(word_max_length, int):
            return ()
        word = list(context)
        while True:
            if len(word) == word_max_length:
                word.append(self.language_profile.storage.storage['_'])
                break
            letter = self._generate_letter(context)
            word.append(letter)
            context = *context[1:], letter
            if word[-1] == self.language_profile.storage.storage['_']:
                break
        return tuple(word)

    def generate_sentence(self, context: tuple, word_limit: int) -> tuple:
        """
        Generates full sentence with fixed number of words given.
        """
        if not isinstance(word_limit, int) or not isinstance(context, tuple):
            return ()
        return_list = []
        while len(return_list) != word_limit:
            new_word = self._generate_word(context)
            return_list.append(new_word)
            context = tuple(new_word[-1:])
        return tuple(return_list)

    def generate_decoded_sentence(self, context: tuple, word_limit: int) -> str:
        """
        Generates full sentence and decodes it
        """
        if not isinstance(context, tuple) or not isinstance(word_limit, int):
            return ''
        encoded_sentence = self.generate_sentence(context, word_limit)
        decoded_sentence = decode_sentence(self.language_profile.storage, encoded_sentence)
        text = translate_sentence_to_plain_text(decoded_sentence)
        return text


# 6
def translate_sentence_to_plain_text(decoded_corpus: tuple) -> str:
    """
    Converts decoded sentence into the string sequence
    """
    if not isinstance(decoded_corpus, tuple) or not decoded_corpus:
        return ''
    list_with_letters = []
    for word in decoded_corpus:
        for letter in word:
            list_with_letters.append(letter)
    last_string = ''.join(list_with_letters)
    last_string = last_string.replace('__', ' ')
    last_string = last_string.replace('_', '')
    last_string += '.'
    return last_string.capitalize()


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
