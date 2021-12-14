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
    not_letters = ['`', '~', '!', '@', '#', '$', '%', '^', '&', '*',
                   '(', ')', '_', '-', '+', '=', '{', '[', ']', '}',
                   '|', '\\', ':', ';', '"', "'", '<', ',', '>', '.',
                   '?', '/', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
    for not_letter in not_letters:
        text = text.replace(not_letter, "")
    text = text.lower()
    text_list = text.split()
    tokenized_text = []
    for word in text_list:
        word_by_letter = ['_']
        for letter in word:
            word_by_letter.append(letter)
        word_by_letter.append('_')
        tokenized_text.append(tuple(word_by_letter))
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
        indexes = list(self.storage.values())
        # if indexes != []:
        # index = max(indexes) + 1
        # else:
        index = 1
        for word in elements:
            for letter in word:
                if letter not in self.storage:
                    self.storage[letter] = index
                    index += 1
        return 0

    def get_letter_count(self) -> int:
        """
        Gets the number of letters in the storage
        """
        length = len(self.storage.keys())
        if length == 0:
            return -1
        return length


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
    encoded_corpus = []
    for word in corpus:
        encoded_word = []
        for letter in word:
            encoded_word.append(storage.get_id(letter))
        encoded_corpus.append(tuple(encoded_word))
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
    decoded_sentence = []
    for word in sentence:
        encoded_word = []
        for id in word:
            encoded_word.append(storage.get_element(id))
        decoded_sentence.append(tuple(encoded_word))
    return tuple(decoded_sentence)


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
        possible_n_grams = []
        if (not isinstance(context, tuple)) or len(context) < 1 or self.language_profile.tries == []:
            return -1
        all_n_grams = []
        found_tries = 1
        used_n_grams = self._used_n_grams
        result = ()
        for trie in self.language_profile.tries:
            if trie.size == len(context) + 1:
                found_tries = 0
                for n_gram, freq in trie.n_gram_frequencies.items():
                    if n_gram not in used_n_grams:
                        all_n_grams.append((freq, n_gram))
            if all_n_grams == []:
                self._used_n_grams = []
                for n_gram, freq in trie.n_gram_frequencies.items():
                    all_n_grams.append((freq, n_gram))
        if found_tries:
            return -1
        for n_gram_n_fr in all_n_grams:
            counter = 0
            for index, letter in enumerate(context):
                if letter != n_gram_n_fr[1][index]:
                    counter -= 1
            if counter == 0:
                possible_n_grams.append(n_gram_n_fr)
        if possible_n_grams == []:
            all_n_grams = sorted(all_n_grams)
            result = all_n_grams[-1][1]
        else:
            possible_n_grams = sorted(possible_n_grams, key=lambda x: x[0], reverse=True)
            result = possible_n_grams[0][1]
        self._used_n_grams.append(result)
        return result[-1]


    def _generate_word(self, context: tuple, word_max_length=15) -> tuple:
        """
        Generates full word for the context given.
        """
        if not (isinstance(context, tuple) and isinstance(word_max_length, int)):
            return ()
        generated_word = []
        stop = -len(context)-1
        for number in context:
            generated_word.append(number)
        while len(generated_word) < word_max_length:
            letter = self._generate_letter(context)
            generated_word.append(letter)
            if len(generated_word) <= len(context):
                new_context = generated_word[-1::-1]
            else:
                new_context = generated_word[-1:stop:-1]
            context = tuple(new_context[::-1])
            if letter == 1:
                break
        if generated_word[-1] != 1:
            generated_word.append(1)
        return tuple(generated_word)

    def generate_sentence(self, context: tuple, word_limit: int) -> tuple:
        """
        Generates full sentence with fixed number of words given.
        """
        if not (isinstance(context, tuple) and isinstance(word_limit, int)):
            return ()
        generated_sentence = []
        stop = -1 - len(context)
        while len(generated_sentence) < word_limit:
            generated_word = self._generate_word(context)
            generated_sentence.append(generated_word)
            new_context = generated_word[-1:stop:-1]
            context = tuple(new_context[::-1])
        return tuple(generated_sentence)

    def generate_decoded_sentence(self, context: tuple, word_limit: int) -> str:
        """
        Generates full sentence and decodes it
        """
        if not (isinstance(context, tuple) and isinstance(word_limit, int)):
            return ""
        encoded_corpus = self.generate_sentence(context, word_limit)
        decoded_sentence = []
        for word in encoded_corpus:
            encoded_word = []
            for id in word:
                encoded_word.append(self.language_profile.storage.get_element(id))
            decoded_sentence.append(tuple(encoded_word))
        normal_sentence = translate_sentence_to_plain_text(tuple(decoded_sentence))
        return normal_sentence


# 6
def translate_sentence_to_plain_text(decoded_corpus: tuple) -> str:
    """
    Converts decoded sentence into the string sequence
    """
    if not isinstance(decoded_corpus,tuple):
        return ''
    list_of_symbols = []
    for word in decoded_corpus:
        for symbol in word:
            list_of_symbols.append(symbol)
    if list_of_symbols[0] == '_':
        del list_of_symbols[0]
    first_letter = list_of_symbols[0]
    first_letter = first_letter.upper()
    list_of_symbols[0] = first_letter
    list_of_symbols[-1] = '.'
    string_version = ''.join(list_of_symbols)
    string_version = string_version.replace('__', ' ')
    return string_version



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
