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
    new_text = ''
    for element in text.lower():
        if element.isalpha() or element.isspace():
            new_text = new_text + element
    token_list = []
    for token in new_text.split():
        tokens = '_'
        for element in token:
            tokens = tokens + element
        tokens += '_'
        token_list.append(tuple(tokens))
    return tuple(token_list)

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
            for element in token:
                self._put(element)
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
    encoded_corpus = tuple(tuple(storage.get_id(element)
                                 for element in token)
                           for token in corpus)
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
    storage.update(sentence)
    decoded_corpus = tuple(tuple(storage.get_element(num)
                                 for num in token)
                           for token in sentence)
    return decoded_corpus


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
        for trie in self.profile.tries:
            if trie.size != len(context) + 1:
                return -1

        letter_predict = {}

        for trie in self.profile.tries:
            if trie.size == len(context) + 1:
                for k, v in trie.n_gram_frequencies.items():
                    if self._used_n_grams == list(trie.n_gram_frequencies.keys()):
                        self._used_n_grams = []
                    elif k[:len(context)] == context and k not in self._used_n_grams:
                        letter_predict[k] = v
                if letter_predict:
                    accurate_prediction = max(letter_predict.keys(), key=letter_predict.get)
                    self._used_n_grams.append(accurate_prediction)
                else:
                    accurate_prediction = max(trie.n_gram_frequencies.keys(),
                                              key=trie.n_gram_frequencies.get)
                return accurate_prediction[-1]
        return -1



    def _generate_word(self, context: tuple, word_max_length=15) -> tuple:
        """
        Generates full word for the context given.
        """
        if not (isinstance(context, tuple) and isinstance(word_max_length, int)):
            return ()

        generated_w = list(context)
        while len(generated_w) <= word_max_length:
            if not word_max_length == 1:
                letter = self._generate_letter(context)
                generated_w.append(letter)
                if letter == self.profile.storage.get_special_token_id():
                    break
            else:
                generated_w.append(self.profile.storage.get_special_token_id())
                return tuple(generated_w)

            context = tuple(generated_w[-1:])
        return tuple(generated_w)


    def generate_sentence(self, context: tuple, word_limit: int) -> tuple:
        """
        Generates full sentence with fixed number of words given.
        """
        if not (isinstance(context, tuple) and isinstance(word_limit, int)):
            return ()

        sentence = []

        while len(sentence) < word_limit:
            generated_word = self._generate_word(context)
            sentence.append(generated_word)
            context = tuple(generated_word[-1:])
        return tuple(sentence)

    def generate_decoded_sentence(self, context: tuple, word_limit: int) -> str:
        """
        Generates full sentence and decodes it
        """
        if not (isinstance(context, tuple) and isinstance(word_limit, int)):
            return ''

        sentence = self.generate_sentence(context, word_limit)
        empty_string = ''

        for word in sentence:
            for element in word:
                letter = self.profile.storage.get_element(element)
                empty_string += letter
        updated_string = empty_string.replace('__', ' ').replace('_', '').capitalize() + '.'
        return updated_string


# 6
def translate_sentence_to_plain_text(decoded_corpus: tuple) -> str:
    """
    Converts decoded sentence into the string sequence
    """
    if not (isinstance(decoded_corpus, tuple) and decoded_corpus):
        return ''

    empty_string = ''
    for element in decoded_corpus:
        for symbol in element:
            empty_string += symbol
    updated_string = empty_string.replace('__', ' ').replace('_', '').capitalize() + '.'
    return updated_string

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
