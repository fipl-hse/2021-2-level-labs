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
        return None
    removesymbols = ['`', '~', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '-', '+',
                        '=', '{', '[', ']', '}', '|', '\\', ':', ';', '"', "'", '<', ',', '>',
                        '.', '?', '/', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
    text = text.lower()
    for symbols in removesymbols:
        text = text.replace(symbols, '')
    tokens = text.split()
    tokenized_text = []
    for token in tokens:
        word = [letter for letter in token if letter.isalpha()]
        word.append('_')
        word.insert(0, '_')
        word_tuple = tuple(word)
        tokenized_text.append(word_tuple)
    return tuple(tokenized_text)


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
    encoded_corpus = tuple(tuple(storage.get_id(letter) for letter in word) for word in corpus)
    return encoded_corpus


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
    decoded_corpus = tuple(tuple(storage.get_element(letter) for letter in word)
                           for word in sentence)
    return decoded_corpus


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
        predict_dict = {}
        for trie in self.language_profile.tries:
            if trie.size == len(context) + 1:
                for n_gram, freq in trie.n_gram_frequencies.items():
                    if self._used_n_grams == list(trie.n_gram_frequencies.keys()):
                        self._used_n_grams = []
                    if n_gram[:len(context)] == context and \
                            n_gram not in self._used_n_grams:
                        predict_dict[n_gram] = freq
                if predict_dict:
                    prediction = max(predict_dict.keys(), key=predict_dict.get)
                    self._used_n_grams.append(prediction)
                else:
                    prediction = max(trie.n_gram_frequencies.keys(),
                                     key=trie.n_gram_frequencies.get)
                return prediction[-1]
            return -1

    def _generate_word(self, context: tuple, word_max_length=15) -> tuple:
        """
        Generates full word for the context given.
        """
        if not isinstance(context, tuple) or not isinstance(word_max_length, int):
            return ()
        word = list(context)
        while len(word) <= word_max_length:
            if word_max_length == 1:
                word.append(self.language_profile.storage.get_special_token_id())
            else:
                letter = self._generate_letter(context)
                word.append(letter)
                if letter == self.language_profile.storage.get_special_token_id():
                    break
                context = tuple(word[-len(context):])
        return tuple(word)

    def generate_sentence(self, context: tuple, word_limit: int) -> tuple:
        """
        Generates full sentence with fixed number of words given.
        """
        if not isinstance(context, tuple) or not isinstance(word_limit, int):
            return ()
        sentence = []
        while len(sentence) != word_limit:
            word = self._generate_word(context, word_max_length=15)
            sentence.append(word)
            context = tuple(word[-1:])
        return tuple(sentence)

    def generate_decoded_sentence(self, context: tuple, word_limit: int) -> str:
        """
        Generates full sentence and decodes it
        """
        if not isinstance(context, tuple) or not isinstance(word_limit, int):
            return ''
        sentence = self.generate_sentence(context, word_limit)
        decoded_sentence = ""
        for word in sentence:
            for element in word:
                letter = self.language_profile.storage.get_element(element)
                decoded_sentence += letter
        decoded_sentence = decoded_sentence.replace('__', ' ').strip('_').capitalize() + '.'
        return decoded_sentence


# 6
def translate_sentence_to_plain_text(decoded_corpus: tuple) -> str:
    """
    Converts decoded sentence into the string sequence
    """
    if not (isinstance(decoded_corpus, tuple)
            and decoded_corpus):
        return ''
    decoded_sentence = ''
    for word in decoded_corpus:
        for letter in word:
            decoded_sentence += letter
    decoded_sentence = decoded_sentence.replace('__', ' ').replace('_', '').capitalize() + '.'
    return decoded_sentence


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
