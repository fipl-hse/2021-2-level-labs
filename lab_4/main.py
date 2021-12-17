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
    new_text = ""
    new_list = []
    for letter in text:
        if letter.isalpha() or letter.isspace():
            new_text += new_text.join(letter)
    for word in new_text.lower().strip().split():
        new_list.append(tuple("_" + word + "_"))
    return tuple(new_list)


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
        n_grams = []
        for trie in self.language_profile.tries:
            if trie.size == len(context) + 1:
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
        n_grams = sorted(n_grams, key=lambda x: x[1], reverse=True)
        self._used_n_grams.append(n_grams[0][0])
        return n_grams[0][0][-1]

    def _generate_word(self, context: tuple, word_max_length=15) -> tuple:
        """
        Generates full word for the context given.
        """
        if not isinstance(context, tuple) or not isinstance(word_max_length, int):
            return ()
        new_word = []
        for letter in context:
            new_word.append(letter)
        while True:
            if len(new_word) == word_max_length:
                new_word.append(self.language_profile.storage.storage['_'])
                break
            following_letter = self._generate_letter(context)
            new_word.append(following_letter)
            context = *context[1:], following_letter
            if new_word[-1] == self.language_profile.storage.storage['_']:
                break
        return tuple(new_word)

    def generate_sentence(self, context: tuple, word_limit: int) -> tuple:
        """
        Generates full sentence with fixed number of words given.
        """
        if not isinstance(context, tuple) or not isinstance(word_limit, int):
            return ()
        new_sentence = []
        while len(new_sentence) != word_limit:
            following_word = self._generate_word(context)
            new_sentence.append(following_word)
            context = tuple(following_word[-1:])
        return tuple(new_sentence)

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
