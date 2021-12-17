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

    text = text.lower()
    words = text.split()
    tokens = []

    for word in words:
        token = []
        for letter in word:
            if letter.isalpha():
                token.append(letter)
        if token != []:
            token.append('_')
            token.insert(0, '_')
            tokens.append(tuple(token))

    tokens = tuple(tokens)
    return tokens


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
        
        default_id = 0
        
        for word in elements:
            for letter in word:
                if letter.isalpha() or letter == '_':
                    if letter not in self.storage:
                        default_id += 1
                        self.storage[letter] = default_id
        return 0
    
    def get_letter_count(self) -> int:
        """
        Gets the number of letters in the storage
        """
        if default_id == 0:
            return -1
        else:
            return default_id


# 4
def encode_corpus(storage: LetterStorage, corpus: tuple) -> tuple:
    """
    Encodes corpus by replacing letters with their ids
    :param storage: an instance of the LetterStorage class
    :param corpus: a tuple of tuples
    :return: a tuple of the encoded letters
    """
    if not isinstance(corpus, tuple):
        return ()
    if not isinstance(storage, LetterStorage):
        return ()

    storage.update(corpus)

    encoded_corpus = []

    for word in corpus:
        encoded_word = []
        for letter in word:
            encoded_word.append(storage.storage.get(letter))
        encoded_corpus.append(tuple(encoded_word))

    encoded_corpus = tuple(encoded_corpus)
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

    decoded_corpus = []

    letters = list(storage.storage.keys())
    ids = list(storage.storage.values())

    for word in sentence:
        decoded_word = []
        for letter in word:
            if letter > 0:
                decoded_word.append(letters[ids.index(letter)])
        decoded_corpus.append(tuple(decoded_word))

    decoded_corpus = tuple(decoded_corpus)
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
        if not isinstance(context, tuple) or len(context) < 1:
            return -1

        context_length = len(context)
        temp_ngrams = self.profile.tries[0].n_gram_frequencies.copy()
        top_match = ()
        top_frequency = 0

        attempt = 0
        while attempt <= 2:
            if len(self._used_n_grams) == len(temp_ngrams.keys()):
                self._used_n_grams.clear()

            for ngram in temp_ngrams:
                for i in range(context_length):
                    if context[i] != ngram[i]:
                        continue
                if temp_ngrams[ngram] > top_frequency:
                    top_match = ngram
                    top_frequency = temp_ngrams[top_match]

            if top_frequency == 0:
                ngrams = temp_ngrams.keys
                top_match = ngrams[0]

            if top_match not in self._used_n_grams:
                self._used_n_grams.append(top_match)
                top_match = list(top_match)
                return top_match[-1]

            attempt += 1

        return -1

    def _generate_word(self, context: tuple, word_max_length=15) -> tuple:
        """
        Generates full word for the context given.
        """
        if not isinstance(context, tuple) or len(context) < 1:
            return ()

        context_length = len(context)
        generated_word = []
        stop_sign = self.profile.storage.get_special_token_id()

        for letter in context:
            generated_word.append(letter)

        current_context = context
        current_word_length = len(context)
        while current_word_length <= word_max_length:
            generated_letter = self._generate_letter(current_context)
            generated_word.append(generated_letter)
            if generated_letter > 0:
                if generated_letter == stop_sign:
                    break

            current_context = generated_word.copy()
            current_context.reverse()
            current_context = tuple(current_context[:context_length])

            current_word_length += 1

        if len(generated_word) == word_max_length:
            generated_word.append(stop_sign)

        return tuple(generated_word)

    def generate_sentence(self, context: tuple, word_limit: int) -> tuple:
        """
        Generates full sentence with fixed number of words given.
        """
        if not isinstance(context, tuple) or len(context) < 1:
            return ()
        if not isinstance(word_limit, int) or word_limit < 1:
            return ()

        context_length = len(context)
        generated_sentence = []

        current_context = context
        current_word_count = 1
        while current_word_count <= word_limit:
            generated_word = self._generate_word(current_context)
            if generated_word:
                generated_sentence.append(generated_word)

            current_context = list(generated_sentence[current_word_count - 1])
            current_context.reverse()
            current_context = tuple(current_context[:context_length])

            current_word_count += 1

        return tuple(generated_sentence)

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
    if not isinstance(decoded_corpus, tuple):
        return ''

    plain_sentence = ''

    for word in decoded_corpus:
        for letter in word:
            plain_sentence += letter

    if not plain_sentence:
        return ''

    if plain_sentence[0] == '_':
        plain_sentence = plain_sentence.replace('_', '', 1)
    plain_sentence = plain_sentence[0].upper() + plain_sentence[1::]
    plain_sentence = plain_sentence.replace('__', ' ')
    plain_sentence = plain_sentence.replace('_', '.', -1)

    return plain_sentence


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
