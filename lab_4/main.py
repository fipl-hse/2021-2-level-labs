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
    clear_text = ''
    for symbol in text.lower():
        if symbol.isalpha() or symbol.isspace():
            clear_text += symbol
    text_list = []
    for word in clear_text.split():
        text_list.append(tuple([letter for letter in '_' + word + '_']))
    return tuple(text_list)


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
    if not (isinstance(storage, LetterStorage) and isinstance(corpus, tuple)):
        return ()
    storage.update(corpus)
    encoded = tuple(tuple(Storage.get_id(storage, letter)
                          for letter in element)
                    for element in corpus)
    return encoded


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
    decoded = tuple(tuple(Storage.get_element(storage, id_letter)
                          for id_letter in element)
                    for element in sentence)
    return decoded


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
        if len(context) + 1 not in [trie.size for trie in self.profile.tries]:
            return -1
        freq_dict = {}
        use_gram = ()
        for trie in self.profile.tries:
            if trie.size == len(context) + 1:
                for n_gram, freq in trie.n_gram_frequencies.items():
                    if self._used_n_grams == list(trie.n_gram_frequencies.keys()):
                        self._used_n_grams = []
                    if n_gram[:-1] == context and n_gram not in self._used_n_grams:
                        freq_dict[n_gram] = freq
            sorted_freq = sorted(freq_dict, key=freq_dict.get, reverse=True)
            if freq_dict:
                use_gram = sorted_freq[0]
                self._used_n_grams.append(use_gram)
            else:
                use_gram = max(trie.n_gram_frequencies.keys(), key=trie.n_gram_frequencies.get)
        return use_gram[-1]

    def _generate_word(self, context: tuple, word_max_length=15) -> tuple:
        """
        Generates full word for the context given.
        """
        if not isinstance(context, tuple) or not isinstance(word_max_length, int):
            return ()
        word = list(context)
        if word_max_length == 1:
            word.append(self.profile.storage.get_special_token_id())
            return tuple(word)
        while len(word) != word_max_length:
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
        while len(sentence) != word_limit:
            word = self._generate_word(context)
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
        raw_string = ''
        for word in sentence:
            for element_id in word:
                letter = self.profile.storage.get_element(element_id)
                raw_string += letter
        final_sentence = raw_string.replace('__', ' ').replace('_', '').capitalize() + '.'
        return final_sentence


# 6
def translate_sentence_to_plain_text(decoded_corpus: tuple) -> str:
    """
    Converts decoded sentence into the string sequence
    """
    if not isinstance(decoded_corpus, tuple) or not decoded_corpus:
        return ''
    raw_string = ''
    for word in decoded_corpus:
        for letter in word:
            raw_string += letter
    final_sentence = raw_string.replace('__', ' ').replace('_', '').capitalize() + '.'
    return final_sentence


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
        if len(context) + 1 not in [trie.size for trie in self.profile.tries]:
            return -1
        word = context + (letter,)
        freq_dict = {}
        for trie in self.profile.tries:
            if trie.size == len(word):
                for n_gram, freq in trie.n_gram_frequencies.items():
                    if n_gram[:len(context)] == context:
                        freq_dict[n_gram] = freq
                if not freq_dict:
                    return 0.0
        context_freq = sum(freq_dict.values())
        word_freq = freq_dict[word]
        probability = word_freq/context_freq
        return probability

    def _generate_letter(self, context: tuple) -> int:
        """
        Generates the next letter.
            Takes the letter with highest
            maximum likelihood frequency.
        """
        if not isinstance(context, tuple) or not context:
            return -1
        if len(context) + 1 not in [trie.size for trie in self.profile.tries]:
            return -1
        prob_dict = {}
        for trie in self.profile.tries:
            if trie.size == len(context) + 1:
                for n_gram, freq in trie.n_gram_frequencies.items():
                    if n_gram[:len(context)] == context:
                        prob_dict[n_gram] = self._calculate_maximum_likelihood(n_gram[-1], context)
        if not prob_dict:
            for trie in self.profile.tries:
                if trie.size == 1:
                    letter = max(trie.n_gram_frequencies.keys(), key=trie.n_gram_frequencies.get)
                    return letter[0]
        else:
            letter = max(prob_dict.keys(), key=prob_dict.get)[-1]
            return letter


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
