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
    trash_symbols = '1234567890-=!@#$%^&*()_+{}[]":;?/>.<,\'\|/'

    text = text.lower()
    for letter in text:
        if letter in trash_symbols:
            text = text.replace(letter, '')

    list_of_tokens = []
    clear_text = text.split()
    for word in clear_text:
        tokens = ''
        for letter in word:
            tokens += letter
        list_of_tokens.append(tuple(['_'] + list(tokens) + ['_']))
    return tuple(list_of_tokens)


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
        for element in elements:
            for letter in element:
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
    storage.update(sentence)
    encoded_sentences = tuple(tuple(storage.get_element(number)
                                    for number in word)
                              for word in sentence)
    return encoded_sentences



# 6
class NGramTextGenerator:
    """
    Language model for basic text generation
    """

    def __init__(self, language_profile: LanguageProfile):
        self.profile = language_profile
        self._used_n_grams = []

    def _generate_letter(self, context: tuple) -> int:
        """
        Generates the next letter.
            Takes the letter from the most
            frequent ngram corresponding to the context given.
        """
        if not isinstance(context, tuple):
            return -1
        prediction = {}
        for trie in self.profile.tries:
            if trie.size == len(context) + 1:
                for key, value in trie.n_gram_frequencies.items():
                    if self._used_n_grams == list(trie.n_gram_frequencies.keys()):
                        self._used_n_grams = []
                    elif key[:len(context)] == context and key not in self._used_n_grams:
                        prediction[key] = value
                if prediction:
                    accurate_prediction = max(prediction.keys(), key=prediction.get)
                    self._used_n_grams.append(accurate_prediction)
                else:
                    accurate_prediction = max(trie.n_gram_frequencies.keys(), key=trie.n_gram_frequencies.get)
                return accurate_prediction[-1]
            else:
                return -1

    def _generate_word(self, context: tuple, word_max_length=15) -> tuple:
        """
        Generates full word for the context given.
        """
        if not isinstance(context, tuple) or \
                not isinstance(word_max_length, int):
            return ()
        final_word = list(context)
        while len(final_word) <= word_max_length:
            if word_max_length == 1:
                final_word.append(self.profile.storage.get_special_token_id())
                return tuple(final_word)
            else:
                letter = self._generate_letter(context)
                final_word.append(letter)
                if letter == self.profile.storage.get_special_token_id():
                    break
            context = tuple(final_word[-1:])
        return tuple(final_word)

    def generate_sentence(self, context: tuple, word_limit: int) -> tuple:
        """
        Generates full sentence with fixed number of words given.
        """
        if not isinstance(context, tuple) \
                or not isinstance(word_limit, int):
            return ()
        final_sentence = []
        while len(final_sentence) != word_limit:
            word = self._generate_word(context, word_max_length=15)
            final_sentence.append(word)
            context = tuple(word[-1:])
        return tuple(final_sentence)

    def generate_decoded_sentence(self, context: tuple, word_limit: int) -> str:
        """
        Generates full sentence and decodes it
        """
        if not isinstance(context, tuple) or not isinstance(word_limit, int):
            return ''
        sentence = self.generate_sentence(context, word_limit)
        string = ''
        for element in sentence:
            for numer in element:
                letter = self.profile.storage.get_element(numer)
                string += letter
        string = string.replace('__', ' ').replace('_', '').capitalize() + '.'
        return string


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
