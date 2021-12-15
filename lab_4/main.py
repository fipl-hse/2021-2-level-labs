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
    text = text.lower().split()
    final_tuple = []
    for words in text:
        word = []
        for letter in words:
            if letter.isalpha():
                word.append(letter)
        if word:
            word.append('_')
            word.insert(0, '_')
            final_tuple.append(tuple(word))
    return tuple(final_tuple)


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
    if not isinstance(corpus, tuple) or not isinstance(storage, LetterStorage):
        return ()
    storage.update(corpus)
    encode_tuple = tuple(tuple(storage.get_id(letter) for letter in word) for word in corpus)
    return encode_tuple


# 4
def decode_sentence(storage: LetterStorage, sentence: tuple) -> tuple:
    """
    Decodes sentence by replacing letters with their ids
    :param storage: an instance of the LetterStorage class
    :param sentence: a tuple of tuples-encoded words
    :return: a tuple of the decoded sentence
    """
    if not isinstance(sentence, tuple) or not isinstance(storage, LetterStorage):
        return ()
    decode_tuple = tuple(tuple(storage.get_element(letter) for letter in word) for word in sentence)
    return decode_tuple


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
        if not isinstance(context, tuple) or \
                len(context) + 1 not in [trie.size for trie in self.profile.tries]:
            return -1
        freq = {}
        needed_gram = ()
        for trie in self.profile.tries:
            if len(context) + 1 == trie.size:
                for gram, freq_gram in trie.n_gram_frequencies.items():
                    if self._used_n_grams == list(trie.n_gram_frequencies.keys()):
                        self._used_n_grams = []
                    if gram[:len(context)] == context and gram not in self._used_n_grams:
                        freq[gram] = freq_gram
                if freq:
                    needed_gram = max(freq.keys(), key=freq.get)
                else:
                    needed_gram = max(trie.n_gram_frequencies, key=trie.n_gram_frequencies.get)
                self._used_n_grams.append(needed_gram)
        return needed_gram[-1]

    def _generate_word(self, context: tuple, word_max_length=15) -> tuple:
        """
        Generates full word for the context given.
        """
        if not isinstance(context, tuple) or not isinstance(word_max_length, int):
            return ()
        gen_word = list(context)
        if len(gen_word) >= word_max_length:
            gen_word.append(self.profile.storage.get_special_token_id())
            return tuple(gen_word)
        while len(gen_word) != word_max_length:
            letter = self._generate_letter(context)
            gen_word.append(letter)
            if letter == self.profile.storage.get_special_token_id():
                break
            context = tuple(gen_word[-1:])
        return tuple(gen_word)

    def generate_sentence(self, context: tuple, word_limit: int) -> tuple:
        """
        Generates full sentence with fixed number of words given.
        """
        if not isinstance(context, tuple) or not isinstance(word_limit, int):
            return ()
        gen_sentence = []
        while len(gen_sentence) != word_limit:
            word = self._generate_word(context)
            gen_sentence.append(word)
            context = tuple(word[-1:])
        return tuple(gen_sentence)

    def generate_decoded_sentence(self, context: tuple, word_limit: int) -> str:
        """
        Generates full sentence and decodes it
        """
        if not isinstance(context, tuple) or not isinstance(word_limit, int):
            return ''
        gen_sentence = self.generate_sentence(context, word_limit)
        dec_sentence = ''
        for word in gen_sentence:
            for symbol in word:
                letter = self.profile.storage.get_element(symbol)
                dec_sentence += letter
        dec_sentence = dec_sentence.replace('__', ' ').strip('_').capitalize() + '.'
        return dec_sentence


# 6
def translate_sentence_to_plain_text(decoded_corpus: tuple) -> str:
    """
    Converts decoded sentence into the string sequence
    """
    if not isinstance(decoded_corpus, tuple) or not decoded_corpus:
        return ''
    dec_sentence = ''
    for word in decoded_corpus:
        for symbol in word:
            dec_sentence += symbol
    dec_sentence = dec_sentence.replace('__', ' ').strip('_').capitalize() + '.'
    return dec_sentence


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
        if not isinstance(letter, int) or not isinstance(context, tuple) \
                or len(context) + 1 not in [trie.size for trie in self.profile.tries] \
                or not context:
            return -1
        word = context + (letter,)
        freq_d = {}
        freq_word = 0
        for trie in self.profile.tries:
            if trie.size == len(word):
                for n_gram, freq in trie.n_gram_frequencies.items():
                    if n_gram[:len(context)] == context:
                        freq_d[n_gram] = freq
                        if n_gram[-1] == letter:
                            freq_word = freq
                if not freq_d:
                    return 0.0
        freq_context = sum(freq_d.values())
        prob = freq_word / freq_context
        return prob

    def _generate_letter(self, context: tuple) -> int:
        """
        Generates the next letter.
            Takes the letter with highest
            maximum likelihood frequency.
        """
        if not isinstance(context, tuple)\
                or len(context) + 1 not in [trie.size for trie in self.profile.tries]\
                or not context:
            return -1
        prob_dict = {}
        for trie in self.profile.tries:
            if trie.size == len(context) + 1:
                for n_gram in trie.n_gram_frequencies:
                    if n_gram[:-1] == context:
                        prob_dict[n_gram] = self._calculate_maximum_likelihood(n_gram[-1], context)
        if not prob_dict:
            for trie in self.profile.tries:
                if trie.size == 1:
                    return max(trie.n_gram_frequencies.keys(), key=trie.n_gram_frequencies.get)[0]
        possible_letter = max(prob_dict.keys(), key=prob_dict.get)[-1]
        return possible_letter

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
