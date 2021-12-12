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
    invaluable_trash = ('`', '~', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '-', '+',
                        '=', '{', '[', ']', '}', '|', '\\', ':', ';', '"', "'", '<', ',', '>',
                        '/', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '.', '?', '!', '…')
    for symbol in invaluable_trash:
        text = text.replace(symbol, '')
    text = text.lower().split()
    new_word = ['_']
    all_words = []
    for word in text:
        new_word.extend(word)
        new_word.append('_')
        all_words.append(tuple(new_word))
        new_word = ['_']
    all_words = tuple(all_words)
    return all_words


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
    encoded_corpus = tuple(tuple(storage.get_id(letter) for letter in word) for word in corpus)
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
    decoded_corpus = tuple(tuple(storage.get_element(number) for number in word) for word in sentence)
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
                and len(context)+1 in [trie.size for trie in self.profile.tries]):
            return -1

        possible_n_grams = {}

        for trie in self.profile.tries:
            if trie.size - 1 == len(context):
                for key, value in trie.n_gram_frequencies.items():
                    if self._used_n_grams == list(trie.n_gram_frequencies.keys()):
                        self._used_n_grams = []
                    if key[:len(context)] == context and key not in self._used_n_grams:
                        possible_n_grams[key] = value
                if possible_n_grams == {}:
                    n_gram_for_generation = max(trie.n_gram_frequencies, key=trie.n_gram_frequencies.get)
                else:
                    n_gram_for_generation = max(possible_n_grams, key=possible_n_grams.get)
                self._used_n_grams.append(n_gram_for_generation)
        return n_gram_for_generation[-1]

    def _generate_word(self, context: tuple, word_max_length=15) -> tuple:
        """
        Generates full word for the context given.
        """

        if not isinstance(context, tuple) or not isinstance(word_max_length, int):
            return ()

        generated_word = list(context)

        if len(generated_word) >= word_max_length:
            generated_word.append(self.profile.storage.get_special_token_id())
            return tuple(generated_word)

        while len(generated_word) != word_max_length:
            generated_letter = self._generate_letter(context)
            generated_word.append(generated_letter)
            if generated_letter == self.profile.storage.get_special_token_id():
                break
            context = tuple(generated_word[-len(context):])
            if len(generated_word) == word_max_length:
                generated_word.append(self.profile.storage.get_special_token_id())
        return tuple(generated_word)

    def generate_sentence(self, context: tuple, word_limit: int) -> tuple:
        """
        Generates full sentence with fixed number of words given.
        """
        if not isinstance(context, tuple) or not isinstance(word_limit, int):
            return ()

        generated_sentence = []

        while len(generated_sentence) != word_limit:
            generated_word = self._generate_word(context, word_max_length=15)
            generated_sentence.append(generated_word)
            context = tuple(generated_word[-len(context):])
        return tuple(generated_sentence)

    def generate_decoded_sentence(self, context: tuple, word_limit: int) -> str:
        """
        Generates full sentence and decodes it
        """
        if not isinstance(context, tuple) or not isinstance(word_limit, int):
            return ""
        sentence_to_decode = self.generate_sentence(context, word_limit)
        decoded_sentence = ''
        for word in sentence_to_decode:
            for symbol in word:
                letter = self.profile.storage.get_element(symbol)
                decoded_sentence += letter
        decoded_sentence = decoded_sentence.replace('__', ' ').strip('_').capitalize() + '.'
        return decoded_sentence


# 6
def translate_sentence_to_plain_text(decoded_corpus: tuple) -> str:
    """
    Converts decoded sentence into the string sequence
    """
    if not isinstance(decoded_corpus, tuple) or not decoded_corpus:
        return ''

    decoded_sentence = ''
    for word in decoded_corpus:
        for letter in word:
            decoded_sentence += letter
    decoded_sentence = decoded_sentence.replace('__', ' ').strip('_').capitalize() + '.'
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
