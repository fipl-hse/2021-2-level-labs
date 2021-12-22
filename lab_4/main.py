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
    f_txt = ""
    f_lst = []
    for letter in text:
        if letter.isalpha() or letter.isspace():
            f_txt += f_txt.join(letter)
    for word in f_txt.lower().strip().split():
        f_lst.append(tuple("_" + word + "_"))
    return tuple(f_lst)


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
        if not isinstance(context, tuple)\
		or if len(context) + 1 not in [trie.size for trie in self.language_profile.tries]:
            return -1
        n_grams = []
        for trie in self.language_profile.tries:
            if trie.size == len(context) +1:
                for n_gram in trie.n_gram_frequencies:
                    if n_gram[:-1] == context and n_gram not in self._used_n_grams:
                        n_grams.append((n_gram, trie.n_gram_frequencies[n_gram]))
            if not n_grams:
                for n_gram in trie.n_gram_frequencies:
                    if n_gram not in self._used_n_grams:
                        n_grams.append((n_gram, trie.n_gram_frequencies[n_gram]))
            if not n_grams:
                self._used_n_grams = []
                for n_gram in trie.n_gram_frequencies:
                    if n_gram[:-1] == context and n_gram not in self._used_n_grams:
                        n_grams.append((n_gram, trie.n_gram_frequencies[n_gram]))
        if not n_grams:
            return -1
        n_grams = sorted(n_grams, key=lambda x: x[1], reverse = True)
        self._used_n_grams.append(n_grams[0][0])
        return n_grams[0][0][-1]

    def _generate_word(self, context: tuple, word_max_length=15) -> tuple:
        """
        Generates full word for the context given.
        """
        if not isinstance(context, tuple) or not isinstance(word_max_length, int):
            return ()
        f_word = []
        for letter in context:
            f_word.append(letter)
        while True:
            if len(f_word) == word_max_length:
                f_word.append(self.language_profile.storage.storage['_'])
                break
            following_letter = self._generate_letter(context)
            f_word.append(following_letter)
            context = *context[1:], following_letter
            if f_word[-1] == self.language_profile.storage.storage['_']:
                break
        return tuple(f_word)



    def generate_sentence(self, context: tuple, word_limit: int) -> tuple:
        """
        Generates full sentence with fixed number of words given.
        """

        if not isinstance(context, tuple) or not isinstance(word_limit, int):
            return ()
        f_sentence = []
        while len(f_sentence) != word_limit:
            following_word = self._generate_word(context)
            f_sentence.append(following_word)
            context = tuple(following_word[-1:])
        return tuple(f_sentence)


    def generate_decoded_sentence(self, context: tuple, word_limit: int) -> str:
        """
        Generates full sentence and decodes it
        """
        if not isinstance(context, tuple):
            return ""
        encoded_sentence = self.generate_sentence(context, word_limit)
        decoded_sentence = decode_sentence(self.language_profile.storage, encoded_sentence)
        return translate_sentence_to_plain_text(decoded_sentence)


# 6
def translate_sentence_to_plain_text(decoded_corpus: tuple) -> str:
    """
    Converts decoded sentence into the string sequence
    """
    if not isinstance(decoded_corpus, tuple) or not decoded_corpus:
        return ''
    result = ''
    for element in decoded_corpus:
        for symbol in element:
            result += symbol
    result = result.replace('__', ' ')
    result = result.replace('_', '')
    result = result.capitalize()
    result += '.'
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

        if not isinstance(letter, int) or not isinstance(context, tuple) \
                or len(context) + 1 not in [trie.size for trie in self.language_profile.tries] \
                or not context:
            return -1
        word = context + (letter,)
        freq_d = {}
        freq_word = 0
        for trie in self.language_profile.tries:
            if trie.size == len(word):
                for n_gram, freq in trie.n_gram_frequencies.items():
                    if n_gram[:len(context)] == context:
                        freq_d[n_gram] = freq
                        if n_gram[-1] == letter:
                            freq_word = freq
                if not freq_d:
                    return 0.0
        freq_context = sum(freq_d.values())
        prob = freq_word / freq_context
        return prob



    def _generate_letter(self, context: tuple) -> int:


        """
            Generates the next letter.

            Takes the letter with highest

            maximum likelihood frequency.
        """

        if not isinstance(context, tuple)\
                or len(context) + 1 not in [trie.size for trie in self.language_profile.tries]\
                or not context:
            return -1
        prob_dict = {}
        for trie in self.language_profile.tries:
            if trie.size == len(context) + 1:
                for n_gram in trie.n_gram_frequencies:
                    if n_gram[:-1] == context:
                        prob_dict[n_gram] = self._calculate_maximum_likelihood(n_gram[-1], context)
        if not prob_dict:
            for trie in self.language_profile.tries:
                if trie.size == 1:
                    return max(trie.n_gram_frequencies.keys(), key=trie.n_gram_frequencies.get)[0]
        possible_letter = max(prob_dict.keys(), key=prob_dict.get)[-1]
        return possible_letter


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
