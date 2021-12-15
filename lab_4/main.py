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
    text = text.lower()
    text = re.split(r'[.!?]\s', text)
    new_text = []
    for sentence in text:
        sentence = sentence.split()
        clear_sent = []
        for word in sentence:
            clear_sent.append(word)
        for word in clear_sent:
            letters = [letter for letter in word if letter.isalpha()]
            if letters:
                letters.insert(0, '_')
                letters.append('_')
                new_text.append(tuple(letters))
            if not new_text:
                return ()
    return tuple(new_text)

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
    if not isinstance(storage, LetterStorage) or not isinstance(corpus, tuple):
        return ()
    storage.update(corpus)
    encoded_corpus = []
    for word in corpus:
        enc_word = []
        for letter in word:
            if letter in storage.storage:
                enc_word.append(storage.get_id(letter))
        encoded_corpus.append(tuple(enc_word))
    return tuple(encoded_corpus)

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
    decoded_sentences = []
    for word in sentence:
        dec_words = []
        for letter in word:
            if letter in storage.storage.values():
                dec_words.append(storage.get_element(letter))
        decoded_sentences.append(tuple(dec_words))
    return tuple(decoded_sentences)

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
        prediction = {}
        grams = ()
        if len(context) + 1 not in [trie.size for trie in self.profile.tries]:
            return -1
        for trie in self.profile.tries:
            if trie.size == len(context) + 1:
                for key, value in trie.n_gram_frequencies.items():
                    if self._used_n_grams == list(trie.n_gram_frequencies.keys()):
                        self._used_n_grams = []
                    if key[:len(context)] == context and key not in self._used_n_grams:
                        prediction[key] = value
                if prediction:
                    grams = max(prediction.keys(), key=prediction.get)
                    self._used_n_grams.append(grams)
                else:
                    grams = max(trie.n_gram_frequencies.keys(), key=trie.n_gram_frequencies.get)
        return grams[-1]

    def _generate_word(self, context: tuple, word_max_length=15) -> tuple:
        """
        Generates full word for the context given.
        """
        if not isinstance(context, tuple) or not isinstance(word_max_length, int):
            return ()
        word = list(context)
        while len(word) <= word_max_length:
            if word_max_length == 1:
                word.append(self.profile.storage.get_special_token_id())
                return tuple(word)
            else:
                letter = self._generate_letter(context)
                word.append(letter)
                if letter == self.profile.storage.get_special_token_id():
                    break
            context = tuple(word[-1:])
        return tuple(word)

    def generate_sentence(self, context: tuple, word_limit: int) -> tuple:
        """
        Generates full sentence with fixed number of words given.
        """
        if not isinstance(context, tuple) or not isinstance(word_limit, int):
            return ()
        sentence = []
        while len(sentence) < word_limit:
            sentence.append(self._generate_word(context))
        return tuple(sentence)

    def generate_decoded_sentence(self, context: tuple, word_limit: int) -> str:
        """
        Generates full sentence and decodes it
        """
        if not isinstance(context, tuple) or not isinstance(word_limit, int):
            return ''
        sentence = self.generate_sentence(context, word_limit)
        string = ''
        for word in sentence:
            for id_number in word:
                letter = self.profile.storage.get_element(id_number)
                string += letter
        decoded_sentence = string.replace('__', ' ').replace('_', '').capitalize() + '.'
        return decoded_sentence

# 6
def translate_sentence_to_plain_text(decoded_corpus: tuple) -> str:
    """
    Converts decoded sentence into the string sequence
    """
    if not isinstance(decoded_corpus, tuple) or not decoded_corpus:
        return ''
    string = ''
    for word in decoded_corpus:
        for symbol in word:
            string += str(symbol)
    new_text = string.replace("__", " ").replace("_", "").capitalize() + '.'
    return new_text


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
