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
    if not isinstance(text, str):
        return -1
    processing_text = text.lower()
    processing_text = re.sub(r'[.\'!@#$%^&*()\-_=+/|"№;:?><,`~’…—\[\]{}1234567890]', '',
                             processing_text)
    processing_text = processing_text.split()
    if not processing_text:
        return ()
    for word_index, word in enumerate(processing_text):
        new_word = '_' + word + '_'
        processing_text[word_index] = tuple(new_word)
        # processed_text = tuple(split_text)
    return tuple(processing_text)


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
        return len(self.storage)


# 4
def encode_corpus(storage: LetterStorage, corpus: tuple) -> tuple:
    """
    Encodes corpus by replacing letters with their ids
    :param storage: an instance of the LetterStorage class
    :param corpus: a tuple of tuples
    :return: a tuple of the encoded letters
    """
    if not isinstance(storage, LetterStorage) or not isinstance(corpus, tuple):
        return ()
    storage.update(corpus)
    corpus_id = []
    for word in corpus:
        word_id = []
        for letter in word:
            if letter in storage.storage:
                word_id.append(storage.get_id(letter))
        corpus_id.append(tuple(word_id))
    return tuple(corpus_id)


# 4
def decode_sentence(storage: LetterStorage, sentence: tuple) -> tuple:
    """
    Decodes sentence by replacing letters with their ids
    :param storage: an instance of the LetterStorage class
    :param sentence: a tuple of tuples-encoded words
    :return: a tuple of the decoded sentence
    """
    if not isinstance(storage, LetterStorage) or not isinstance(sentence, tuple):
        return ()
    storage.update(sentence)
    text_corpus = []
    for word_id in sentence:
        word = []
        for letter_id in word_id:
            if letter_id in storage.storage.values():
                word.append(storage.get_element(letter_id))
        text_corpus.append(tuple(word))
    return tuple(text_corpus)


# 6
class NGramTextGenerator:
    """
    Language model for basic text generation
    """

    def __init__(self, language_profile: LanguageProfile):
        self._used_n_grams = []
        self.profile = language_profile

    def _generate_letter(self, context: tuple) -> int:
        """
        Generates the next letter.
            Takes the letter from the most
            frequent ngram corresponding to the context given.
        """
        if not isinstance(context, tuple):
            return -1
        for trie in self.profile.tries:
            if trie.size == 2:
                possible_n_grams = trie.n_gram_frequencies
        possible_n_grams = sorted(possible_n_grams, key=possible_n_grams.get, reverse=True)
        for n_gram_index, possible_n_gram in enumerate(possible_n_grams):
            if possible_n_gram not in self._used_n_grams and possible_n_gram[0] == context[0]:
                    self._used_n_grams.append(possible_n_gram)
                    return possible_n_gram[-1]
            elif n_gram_index == len(possible_n_grams) - 1 and self._used_n_grams:
                self._used_n_grams.clear()
                continue
        return -1

    def _generate_word(self, context: tuple, word_max_length=15) -> tuple:
        """
        Generates full word for the context given.
        """
        if not isinstance(context, tuple):
            return ()
        if len(context) >= word_max_length:
            return_context = []
            for letter_id in context:
                return_context.append(letter_id)
            return_context.append(self.profile.storage.get_special_token_id())
            return tuple(return_context)

        word = [context[0]]
        for letter_id in word:
            word.append(self._generate_letter(tuple([letter_id])))
            if word[-1] == self.profile.storage.get_special_token_id():
                return tuple(word)
            elif len(word) == word_max_length:
                word.append(self.profile.storage.get_special_token_id())
                return tuple(word)
        return ()

    def generate_sentence(self, context: tuple, word_limit: int) -> tuple:
        """
        Generates full sentence with fixed number of words given.
        """
        if not isinstance(context, tuple) or not isinstance(word_limit, int) or word_limit <= 0:
            return ()
        sentence = []
        while len(sentence) < word_limit:
            sentence.append(self._generate_word(context))
        return tuple(sentence)

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
    if not isinstance(decoded_corpus, tuple) or not decoded_corpus:
        return ''
    sentence = []
    for word in decoded_corpus:
        sentence.extend(word)
    if sentence[0] == '_':
        sentence[0] = ''
    if sentence[-1] == '_':
        sentence[-1] = '.'
    decoded_sentence = ''.join(sentence)
    decoded_sentence = decoded_sentence.replace('__', ' ')
    return decoded_sentence.capitalize()



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
