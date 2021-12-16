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

    # words = [word.lower().strip() for word in text.split(" ") if word]
    # text_tuple = tuple(tuple(letter for letter in word if letter.isalpha()) for word in words)

    text = "".join(letter for letter in text if letter.isalpha() or letter.isspace())
    text_tuple = tuple(tuple("_" + word + "_") for word in text.lower().strip().split())
    return text_tuple


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
    decoded_sentences = tuple(tuple(storage.get_element(letter) for letter
                                    in word) for word in sentence)
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
        if not isinstance(context, tuple) or len(context) + 1 not in [trie.size for trie
                                                                      in self.language_profile.tries]:
            return -1
        overall_list = []
        for trie in self.language_profile.tries:
            if trie.size == len(context) + 1:
                for key, value in trie.n_gram_frequencies.items():
                    if key[:-1] == context and key not in self._used_n_grams:
                        overall_list.append((key, value))
            if not overall_list:
                for key, value in trie.n_gram_frequencies.items():
                    if key not in self._used_n_grams:
                        overall_list.append((key, value))
            if not overall_list:
                self._used_n_grams = []
                for key, value in trie.n_gram_frequencies.items():
                    if key[:-1] == context and key not in self._used_n_grams:
                        overall_list.append((key, value))
        if not overall_list:
            return -1
        overall_list = sorted(overall_list, key=lambda x: x[1], reverse=True)
        self._used_n_grams.append(overall_list[0][0])
        return overall_list[0][0][-1]

    def _generate_word(self, context: tuple, word_max_length=15) -> tuple:
        """
        Generates full word for the context given.
        """
        if not isinstance(context, tuple) or not isinstance(word_max_length, int):
            return ()
        token = []
        under = self.language_profile.storage.get_special_token_id()
        context_len = len(context)
        context_length = len(context)
        if context_length > 1 \
                and context[-1] == self.language_profile.storage.get_special_token_id():
            context = (self.language_profile.storage.get_special_token_id(),)
        for character in context:
            token.append(character)
        while True:
            if len(token) == word_max_length:
                token.append(under)
                break
            new_letter = self._generate_letter(context)
            token.append(new_letter)
            context = tuple(token[-context_len:])
            if token[-1] == under:
                break
        return tuple(token)

    def generate_sentence(self, context: tuple, word_limit: int) -> tuple:
        """
        Generates full sentence with fixed number of words given.
        """
        if not isinstance(context, tuple) or not isinstance(word_limit, int):
            return ()
        return_list = []
        while len(return_list) != word_limit:
            new_word = self._generate_word(context)
            return_list.append(new_word)
            context = tuple(new_word[-len(context):])
        return tuple(return_list)

    def generate_decoded_sentence(self, context: tuple, word_limit: int) -> str:
        """
        Generates full sentence and decodes it
        """
        if not isinstance(context, tuple) or not isinstance(word_limit, int):
            return ''
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
    list_with_letters = []
    for word in decoded_corpus:
        for letter in word:
            list_with_letters.append(letter)
    last_string = ''.join(list_with_letters).replace('__', ' ').replace('_', '')
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
        if not isinstance(letter, int) or not isinstance(context, tuple) or not context:
            return -1
        letter_freq = 0.0
        all_freq = 0.0
        for trie in self.language_profile.tries:
            for ngram in trie.n_gram_frequencies:
                if ngram[:-1] == context:
                    ngram_frequency = trie.n_gram_frequencies[ngram]
                    all_freq += ngram_frequency
                    if ngram[-1] == letter:
                        letter_freq += ngram_frequency
        if all_freq != 0.0:
            return letter_freq / all_freq
        return 0.0

    def _generate_letter(self, context: tuple) -> int:
        """
        Generates the next letter.
            Takes the letter with highest
            maximum likelihood frequency.
        """
        if not isinstance(context, tuple) or not self.language_profile.tries or not context:
            return -1
        letters_likelihood = {}
        for letter in self.language_profile.storage.storage.values():
            likelihood = self._calculate_maximum_likelihood(letter, context)
            if likelihood > 0.0:
                letters_likelihood[letter] = likelihood
        if letters_likelihood:
            return max(letters_likelihood, key=letters_likelihood.get)
        under = self.language_profile.storage.get_special_token_id()
        for trie in self.language_profile.tries:
            unigram_list = []
            if trie.size == 1:
                for ngram in trie.n_gram_frequencies:
                    if context[-1] == under and ngram[0] == under:
                        continue
                    unigram_list.append((ngram, trie.n_gram_frequencies[ngram]))
                new_ngram = sorted(unigram_list, key=lambda x: x[1], reverse=True)[0][0][-1]
                return new_ngram
        return -1


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
