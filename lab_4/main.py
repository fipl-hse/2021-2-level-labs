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

    invaluable_trash = ['!', '.', '?','`', '~', '@', '#', '$', '%', '^',
                        '&', '*', '(', ')', '_', '-', '+',
                        '=', '{', '[', ']', '}', '|', '\\', ':', ';', '"', "'", '<', ',', '>',
                        '/', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']

    for symbols in invaluable_trash:
        text = text.replace(symbols, '')
    text = text.lower().split()
    new_character = ['_']
    new_tokens = []
    for character in text:
        new_character.extend(character)
        new_character.append('_')
        new_tokens.append(tuple(new_character))
        new_character = ['_']
    return tuple(new_tokens)



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
        for sentence in elements:
            for token in sentence:
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
    encoded_corpus = tuple(tuple(storage.get_id(letter)
                                          for letter in word)
                                    for word in corpus)
    return tuple(encoded_corpus)



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
    decoded_sentences = tuple(tuple(storage.get_element(letter_id)
                                          for letter_id in word_id)
                                    for word_id in sentence)
    return tuple(decoded_sentences)



# 6
class NGramTextGenerator:
    """
    Language model for basic text generation
    """

    def __init__(self, language_profile: LanguageProfile):
        self.language_profile = language_profile
        self._used_n_grams = []
        pass

    def _generate_letter(self, context: tuple) -> int:
        """
        Generates the next letter.
            Takes the letter from the most
            frequent ngram corresponding to the context given.
        """
        if not isinstance(context, tuple) or not self.language_profile.tries:
            return -1

        for letter in context:
            if self.language_profile.storage.get_element(letter) == -1:
                pass

        no_used_ngrams = {}
        all_no_used_ngrams = {}
        all_ngrams = {}
        context_length = len(context)
        for trie in self.language_profile.tries:
            for ngram in trie.n_gram_frequencies:
                if len(ngram) == context_length + 1:
                    all_ngrams[ngram] = trie.n_gram_frequencies[ngram]
                    if ngram[:-1] == context:
                        all_no_used_ngrams[ngram] = trie.n_gram_frequencies[ngram]
                        if ngram not in self._used_n_grams:
                            no_used_ngrams[ngram] = trie.n_gram_frequencies[ngram]

        if no_used_ngrams:
            next_ngram = max(no_used_ngrams, key=no_used_ngrams.get)
        elif all_no_used_ngrams:
            self._used_n_grams = []
            next_ngram = max(all_no_used_ngrams, key=all_no_used_ngrams.get)
        elif all_ngrams:
            next_ngram = max(all_ngrams, key=all_ngrams.get)
        else:
            return -1
        self._used_n_grams.append(next_ngram)

        return next_ngram[- 1]



    def _generate_word(self, context: tuple, word_max_length=15) -> tuple:
        """
        Generates full word for the context given.
        """
        if not isinstance(context, tuple) or not isinstance(word_max_length, int):
            return ()

        word = []
        special_token_id = self.language_profile.storage.get_special_token_id()
        word.extend(context)
        context_length = len(context)
        while len(word) < word_max_length:
            if word:
                context = tuple(word[-context_length:])

            generated_character_id = self._generate_letter(context)

            if generated_character_id == special_token_id:
                word.append(generated_character_id)
                break
            word.append(generated_character_id)
        else:
            generated_character_id = special_token_id
            word.append(generated_character_id)

        return tuple(word)



    def generate_sentence(self, context: tuple, word_limit: int) -> tuple:
        """
        Generates full sentence with fixed number of words given.
        """
        if not isinstance(context, tuple) or not isinstance(word_limit, int):
            return ()
        generated_sentence = []
        while len(generated_sentence)!= word_limit:
            word = self._generate_word(context, word_max_length = 15)
            generated_sentence.append(word)
            context = tuple(word[-1:])
        return tuple(generated_sentence)



    def generate_decoded_sentence(self, context: tuple, word_limit: int) -> str:
        """
        Generates full sentence and decodes it
        """
        if not isinstance(context, tuple):
            return ()
        sentence = self.generate_sentence(context, word_limit)
        return translate_sentence_to_plain_text\
            (decode_sentence(self.language_profile.storage, sentence))

# 6


def translate_sentence_to_plain_text(decoded_corpus: tuple) -> str:
    """
    Converts decoded sentence into the string sequence
    """
    if not isinstance(decoded_corpus, tuple) or not decoded_corpus:
        return ''
    decoded_string = ''

    for word in decoded_corpus:
        for character in word:
            if not decoded_string and character == '_':
                continue
            if not decoded_string:
                decoded_string += character.upper()
            else:
                decoded_string += character
    decoded_string = decoded_string.replace('__', ' ')
    decoded_string = decoded_string.replace('_', '')
    decoded_string += '.'
    return decoded_string


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

        the_number_of_letter_occurs = 0
        the_number_of_sequence_occurs = 0

        for trie in self.language_profile.tries:
            for ngram in trie.n_gram_frequencies:
                ngram_without_last = ngram[:-1]
                last_character = ngram[-1]

                if ngram_without_last == context:
                    ngram_frequency = trie.n_gram_frequencies[ngram]

                    the_number_of_sequence_occurs += ngram_frequency

                    if last_character == letter:
                        the_number_of_letter_occurs += ngram_frequency

        if the_number_of_sequence_occurs != 0:
            likelihood = the_number_of_letter_occurs / the_number_of_sequence_occurs
            return likelihood

        return 0


    def _generate_letter(self, context: tuple) -> int:
        """
        Generates the next letter.
            Takes the letter with highest
            maximum likelihood frequency.
        """
        if not isinstance(context, tuple) or not self.language_profile.tries or not context:
            return -1

        all_likelihood = {}

        for letter in self.language_profile.storage.storage.values():
            likelihood = self._calculate_maximum_likelihood(letter, context)

            if likelihood > 0:
                all_likelihood[letter] = likelihood

        if all_likelihood:
            return max(all_likelihood, key=all_likelihood.get)

        for trie in self.language_profile.tries:
            if trie.size == 1:
                return max(trie.n_gram_frequencies, key=trie.n_gram_frequencies.get)[0]

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
        pass
