"""
Lab 4
Language generation algorithm based on language profiles
"""

from typing import Tuple
import re
from lab_4.storage import Storage
from lab_4.language_profile import LanguageProfile


# 4
def tokenize_by_letters(text: str) -> Tuple or int:
    """
    Tokenizes given sequence by letters
    """
    if not isinstance(text, str):
        return -1
    text = re.sub(r'[^\w\s]', '', text)
    text = text.lower().split()
    tokenised_text = tuple(('_', *list(token), '_') for token in text if token.isalpha())
    return tokenised_text


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
    if not isinstance(storage, LetterStorage) or not isinstance(corpus, tuple):
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
    if not isinstance(storage, LetterStorage) or not isinstance(sentence, tuple):
        return ()
    decoded_corpus = tuple(tuple(storage.get_element(element_id)
                                       for element_id in token_id)
                                 for token_id in sentence)
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
        if not (isinstance(context, tuple)
                and len(context) + 1 in [trie.size for trie in self.profile.tries]):
            return -1
        possible_n_grams = {}
        for i in self.profile.tries:
            if i.size == len(context) + 1:
                trie = i
        for ngram, freq in trie.n_gram_frequencies.items():
            if ngram[:-1] == context and ngram not in self._used_n_grams:
                possible_n_grams[ngram] = freq
        if not possible_n_grams:
            for ngram, freq in trie.n_gram_frequencies.items():
                if ngram not in self._used_n_grams:
                    possible_n_grams[ngram] = freq
        if not possible_n_grams:
            self._used_n_grams = []
            for ngram, freq in trie.n_gram_frequencies.items():
                if ngram[:-1] == context:
                    possible_n_grams[ngram] = freq
        if not possible_n_grams:
            return -1
        ngram = max(possible_n_grams, key=possible_n_grams.get)
        self._used_n_grams.append(ngram)
        return ngram[-1]

    def _generate_word(self, context: tuple, word_max_length=15) -> tuple:
        """
        Generates full word for the context given.
        """
        if not (isinstance(context, tuple) and isinstance(word_max_length, int)):
            return ()
        generated_word = []
        generated_word.extend(context)
        if word_max_length == 1:
            generated_word.append(self.profile.storage.get_special_token_id())
            return tuple(generated_word)
        while len(generated_word) < word_max_length:
            generated_word.append(self._generate_letter(tuple(context)))
            context = [generated_word[-1]]
            if generated_word[-1] == self.profile.storage.get_special_token_id():
                return tuple(generated_word)
            if len(generated_word) == word_max_length:
                generated_word.append(self.profile.storage.get_special_token_id())
                return tuple(generated_word)
        return ()

    def generate_sentence(self, context: tuple, word_limit: int) -> tuple:
        """
        Generates full sentence with fixed number of words given.
        """
        if not (isinstance(context, tuple)
                and isinstance(word_limit, int)
                and word_limit >= 0):
            return ()
        generated_sentence = []
        for _ in range(word_limit):
            generated_word = self._generate_word(context)
            context = generated_word[-len(context):]
            generated_sentence.append(generated_word)
        return tuple(generated_sentence)

    def generate_decoded_sentence(self, context: tuple, word_limit: int) -> str:
        """
        Generates full sentence and decodes it
        """
        if not (isinstance(context, tuple)
                and isinstance(word_limit, int)
                and word_limit >= 0):
            return ''
        sentence_to_decode = self.generate_sentence(context, word_limit)
        decoded_sentence = ''
        for word in sentence_to_decode:
            for letter_id in word:
                letter = self.profile.storage.get_element(letter_id)
                decoded_sentence += letter
        decoded_sentence = decoded_sentence.replace('__', ' ').replace('_', '').capitalize() + '.'
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
        if not (isinstance(letter, int)
                and isinstance(context, tuple)
                and context):
            return -1
        all_possibles = {}
        likelihood = 0.0
        for trie in self.profile.tries:
            if trie.size == len(context) + 1:
                for ngram, freq in trie.n_gram_frequencies.items():
                    if ngram[:-1] == context:
                        all_possibles[ngram] = freq
                        if ngram[-1] == letter:
                            likelihood = freq
        if not all_possibles:
            return likelihood
        return likelihood / sum(list(all_possibles.values()))

    def _generate_letter(self, context: tuple) -> int:
        """
        Generates the next letter.
            Takes the letter with highest
            maximum likelihood frequency.
        """
        if not (isinstance(context, tuple) and context):
            return -1
        for i in self.profile.tries:
            if i.size == len(context) + 1:
                trie = i
        probabilities = {}
        possibles = {}
        for ngram, freq in trie.n_gram_frequencies.items():
            if ngram[:-1] == context:
                possibles[ngram] = freq
        if not possibles:
            for i in self.profile.tries:
                if i.size == 1:
                    trie = i
            possibles = trie.n_gram_frequencies
        for ngram in possibles:
            probabilities[ngram] = self._calculate_maximum_likelihood(ngram[-1], ngram[:-1])
        return max(probabilities, key=probabilities.get)[-1]


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
