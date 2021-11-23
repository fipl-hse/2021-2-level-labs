"""
Lab 3
Language classification using n-grams
"""

from typing import Dict, Tuple
import re
import random

# 4
def tokenize_by_sentence(text: str) -> tuple:
    """
    Splits a text into sentences, sentences into tokens, tokens into letters
    Tokens are framed with '_'
    :param text: a text
    :return: a list of sentence with lists of tokens split into letters
    e.g.
    text = 'She is happy. He is happy.'
    -->  (
         (('_', 's', 'h', 'e', '_'), ('_', 'i', 's', '_'), ('_', 'h', 'a', 'p', 'p', 'y', '_')),
         (('_', 'h', 'e', '_'), ('_', 'i', 's', '_'), ('_', 'h', 'a', 'p', 'p', 'y', '_'))
         )
    """

    if not isinstance(text, str) or not text:
        return ()

    # creating phrases with regex split
    # regex = anything ending from the .?!'" sequence
    # ended by any break (\n included in \s)
    phrases = re.split(r" *[.?!]['\")]*\s", text)

    # for future removal of irregularities
    irregular_symbols = {'ö': 'oe', 'ü': 'ue', 'ä': 'ae', 'ß': 'ss'}
    punctuation = """'!@#$%^&*()-_=+/|"№;%:?><,.`~’…—[]{}1234567890"""

    for i, phrase in enumerate(phrases):
        # correcting the phrase - replacing case, umlauts etc
        tmp_phrase = phrase.lower()
        for symbol in phrase:
            if symbol in punctuation:
                tmp_phrase = tmp_phrase.replace(symbol, '')
            if symbol in irregular_symbols:
                tmp_phrase = tmp_phrase.replace(symbol, irregular_symbols.get(symbol))
        # dividing the phrase into words
        tmp_phrase = tmp_phrase.split()
        if not tmp_phrase:
            return ()
        # going through a phrase word by word
        # adding _ and rewriting it back into tmp_phrase
        for ii, word in enumerate(tmp_phrase):
            tmp_word = '_' + word + '_'
            tmp_phrase[ii] = tuple(tmp_word)
        # adding an updated phrase into phrases
        phrases[i] = tuple(tmp_phrase)
    return tuple(phrases)


# 4
class LetterStorage:
    """
    Stores and manages letters
    """

    def __init__(self):
        self.storage = {}
        self.id_number = 1

    def _put_letter(self, letter: str) -> int:
        """
        Puts a letter into storage, assigns a unique id
        :param letter: a letter
        :return: 0 if succeeds, 1 if not
        """
        if not isinstance(letter, str):
            return -1
        # if we already have the number we return 0
        # if not than a new element added
        while True:
            if letter in self.storage:
                return 0
            if self.id_number in self.storage.values():
                self.id_number += 1
            else:
                self.storage[letter] = self.id_number
                return 0

    def get_id_by_letter(self, letter: str) -> int:
        """
        Gets a unique id by a letter
        :param letter: a letter
        :return: an id
        """
        if letter not in self.storage:
            return -1
        else:
            return self.storage[letter]

    def get_letter_by_id(self, letter_id: int) -> str or int:
        """
        Gets a letter by a unique id
        :param letter_id: a unique id
        :return: letter
        """
        if letter_id not in self.storage.values():
            return -1
        else:
            for key, value in self.storage.items():
                if value == letter_id:
                    return key

    def update(self, corpus: tuple) -> int:
        """
        Fills a storage by letters from the corpus
        :param corpus: a tuple of sentences
        :return: 0 if succeeds, 1 if not
        """
        if not isinstance(corpus, tuple):
            return -1
        if corpus == ():
            return 0

        for sentence in corpus:
            for word in sentence:
                for letter in word:
                    self._put_letter(letter)
        return 0

# 4
def encode_corpus(storage: LetterStorage, corpus: tuple) -> tuple:
    """
    Encodes sentences by replacing letters with their ids
    :param storage: an instance of the LetterStorage class
    :param corpus: a tuple of sentences
    :return: a tuple of the encoded sentences
    """
    if not isinstance(storage, LetterStorage) or not isinstance(corpus, tuple):
        return ()
    encoded_corpus = ()
    # getting id for each letter and then adding recursively
    # to tuple sequences
    for sentence in corpus:
        word_tuple = ()
        for word in sentence:
            id_letter = ()
            for letter in word:
                id_letter += (storage.get_id_by_letter(letter),)
            word_tuple += (id_letter,)
        encoded_corpus += (word_tuple,)
    return encoded_corpus

# 4
def decode_corpus(storage: LetterStorage, corpus: tuple) -> tuple:
    """
    Decodes sentences by replacing letters with their ids
    :param storage: an instance of the LetterStorage class
    :param corpus: an encoded tuple of sentences
    :return: a tuple of the decoded sentences
    """
    # getting letter for each id and then adding recursively
    # to tuple sequences
    if not isinstance(storage, LetterStorage) or not isinstance(corpus, tuple):
        return ()
    decoded_corpus = ()
    for sentence in corpus:
        word_tuple = ()
        for word in sentence:
            id_letter = ()
            for letter in word:
                id_letter += (storage.get_letter_by_id(letter),)
            word_tuple += (id_letter,)
        decoded_corpus += (word_tuple,)
    return decoded_corpus


# 6
class NGramTrie:
    """
    Stores and manages ngrams
    """

    def __init__(self, n: int, letter_storage: LetterStorage):
        self.size = n
        self.storage = letter_storage
        self.n_grams = ()
        self.n_gram_frequencies = {}

    # 6 - biGrams
    # 8 - threeGrams
    # 10 - nGrams
    def extract_n_grams(self, encoded_corpus: tuple) -> int:
        """
        Extracts n-grams from the given sentence, fills the field n_grams
        :return: 0 if succeeds, 1 if not
        e.g.
        encoded_corpus = (
            ((1, 2, 3, 4, 1), (1, 5, 2, 1)),
            ((1, 3, 4, 1), (1, 5, 2, 1))
        )
        self.size = 2
        --> (
            (
                ((1, 2), (2, 3), (3, 4), (4, 1)), ((1, 5), (5, 2), (2, 1))),
                (((1, 3), (3, 4), (4, 1)), ((1, 5), (5, 2), (2, 1))
            )
        )
        """

        # works for 2 and 3 grams

        if not isinstance(encoded_corpus, tuple):
            return 1

        for sentence in encoded_corpus:
            sentence_grams = ()
            for word in sentence:
                word_grams = ()
                # splitting the whole tuple into sentences, then words
                # cutting to tuples of position + gram size length
                # adding them to the word, then sentence, then corpus
                for i in range(len(word) - self.size+1):
                    word_grams += ((word[i:i + self.size]),)
                sentence_grams += (word_grams,)
            self.n_grams += (sentence_grams,)

        return 0

    def get_n_grams_frequencies(self) -> int:
        """
        Fills in the n-gram storage from a sentence, fills the field n_gram_frequencies
        :return: 0 if succeeds, 1 if not
        e.g.
        self.n_grams = (
            (
                ((1, 2), (2, 3), (3, 4), (4, 1)), ((1, 5), (5, 2), (2, 1))),
                (((1, 3), (3, 4), (4, 1)), ((1, 5), (5, 2), (2, 1))
            )
        )
        --> {
            (1, 2): 1, (2, 3): 1, (3, 4): 2, (4, 1): 2,
            (1, 5): 2, (5, 2): 2, (2, 1): 2, (1, 3): 1
        }
        """
        if not self.n_grams or not isinstance(self.n_grams, tuple):
            return 1

        # if the gram isn't found it's added with the counter-value of 1
        # if the gram is present in keys - the value is updated
        for sentence in self.n_grams:
            for word in sentence:
                for gram in word:
                    if gram not in self.n_gram_frequencies:
                        self.n_gram_frequencies[gram] = 1
                    else:
                        self.n_gram_frequencies[gram] += 1
        return 0

    # 8
    def extract_n_grams_frequencies(self, n_grams_dictionary: dict) -> int:
        """
        Extracts n_grams frequencies from given dictionary.
        Fills self.n_gram_frequency field.
        """
        pass

    # 10
    def extract_n_grams_log_probabilities(self, n_grams_dictionary: dict) -> int:
        """
        Extracts n_grams log-probabilities from given dictionary.
        Fills self.n_gram_log_probabilities field.
        """
        pass

    # 10
    def calculate_log_probabilities(self) -> int:
        """
        Gets log-probabilities of n-grams, fills the field n_gram_log_probabilities
        :return: 0 if succeeds, 1 if not
        """
        pass


# 6
class LanguageProfile:
    """
    Stores and manages language profile information
    """

    def __init__(self, letter_storage: LetterStorage, language_name: str):
        self.storage = letter_storage
        self.language_name = language_name
        self.tries = []
        self.n_words = []

    def create_from_tokens(self, encoded_corpus: tuple, ngram_sizes: tuple) -> int:
        """
        Creates a language profile
        :param letters: a tuple of encoded letters
        :param ngram_sizes: a tuple of ngram sizes,
            e.g. (1, 2, 3) will indicate the function to create 1,2,3-grams
        :return: 0 if succeeds, 1 if not
        e.g.
        encoded_corpus = (((1, 2, 3, 1), (1, 4, 5, 1), (1, 2, 6, 7, 7, 8, 1)),)
        ngram_sizes = (2, 3)

        self.tries --> [<__main__.NGramTrie object at 0x09DB9BB0>, <__main__.NGramTrie object at 0x09DB9A48>]
        self.n_words --> [11, 9]
        self.tries[0].n_grams --> (
            (((1, 2), (2, 3), (3, 1)), ((1, 4), (4, 5), (5, 1)), ((1, 2), (2, 6), (6, 7), (7, 7), (7, 8), (8, 1))),
        )
        """
        if not isinstance(encoded_corpus, tuple) or not isinstance(ngram_sizes, tuple):
            return 1
        # creating one n_gram
        # filling n_gram with encoded corpus and frequencies
        # adding it to ties storage
        # filling n_words as well
        for s in ngram_sizes:
            n_gram = NGramTrie(s, self.storage)
            n_gram.extract_n_grams(encoded_corpus)
            n_gram.get_n_grams_frequencies()
            self.tries.append(n_gram)
            self.n_words.append(len(n_gram.n_gram_frequencies))

    def get_top_k_n_grams(self, k: int, trie_level: int) -> tuple:
        """
        Returns the most common n-grams
        :param k: a number of the most common n-grams
        :param trie_level: N-gram size
        :return: a tuple of the most common n-grams
        e.g.
        language_profile = {
            'name': 'en',
            'freq': {
                (1,): 8, (2,): 3, (3,): 2, (4,): 2, (5,): 2,
                (1, 2): 1, (2, 3): 1, (3, 4): 2, (4, 1): 2,
                (1, 5): 2, (5, 2): 2, (2, 1): 2, (1, 3): 1,
                (1, 2, 3): 1, (2, 3, 4): 1, (3, 4, 1): 2,
                (1, 5, 2): 2, (5, 2, 1): 2, (1, 3, 4): 1
            },
            'n_words': [5, 8, 6]
        }
        k = 5
        --> (
            (1,), (2,), (3,), (4,), (5,),
            (3, 4), (4, 1), (1, 5), (5, 2), (2, 1)
        )
        """

        if not isinstance(k, int) or not isinstance(trie_level, int) or (k < 1 or trie_level < 1):
            return ()
        # creates a reversely sorted tuple with needed trie level
        # and cuts it to necessary length
        for n_trie in self.tries:
            if n_trie.size == trie_level:
                sorted_ngrams_freqs = tuple(sorted(n_trie.n_gram_frequencies.items(), reverse=True)[:k])
                return sorted_ngrams_freqs

        return ()

    # 8
    def save(self, name: str) -> int:
        """
        Saves language profile into json file
        :param name: name of the json file with .json format
        :return: 0 if profile saves, 1 if any errors occurred
        """
        pass

    # 8
    def open(self, file_name: str) -> int:
        """
        Opens language profile from json file and writes output to
            self.language,
            self.tries,
            self.n_words fields.
        :param file_name: name of the json file with .json format
        :return: 0 if profile is opened, 1 if any errors occurred
        """
        pass


# 6
def calculate_distance(unknown_profile: LanguageProfile, known_profile: LanguageProfile,
                       k: int, trie_level: int) -> int:
    """
    Calculates distance between top_k n-grams of unknown profile and known profile
    :param unknown_profile: LanguageProfile class instance
    :param known_profile: LanguageProfile class instance
    :param k: number of frequent N-grams to take into consideration
    :param trie_level: N-gram sizes to use in comparison
    :return: a distance
    Например, первый набор N-грамм для неизвестного профиля - first_n_grams = ((1, 2), (4, 5), (2, 3)),
    второй набор N-грамм для известного профиля – second_n_grams = ((1, 2), (2, 3), (4, 5)).
    Расстояние для (1, 2) равно 0, так как индекс в первом наборе – 0, во втором – 0, |0 – 0| = 0.
    Расстояние для (4, 5) равно 1, расстояние для (2, 3) равно 1.
    Соответственно расстояние между наборами равно 2.
    """
    if not isinstance(unknown_profile, LanguageProfile) or not isinstance(known_profile, LanguageProfile):
        return -1
    if not isinstance(k, int) or not isinstance(trie_level, int):
        return -1

    known_top_n_grams = known_profile.get_top_k_n_grams(k, trie_level)
    unknown_top_n_grams = unknown_profile.get_top_k_n_grams(k, trie_level)
    distance = 0

    for n_gram in unknown_top_n_grams:
        if n_gram in known_top_n_grams:
            distance += abs(known_top_n_grams.index(n_gram) - unknown_top_n_grams.index(n_gram))
        else:
            distance += len(known_top_n_grams)

    return distance


# 8
class LanguageDetector:
    """
    Detects profile language using distance
    """

    def __init__(self):
        pass

    def register_language(self, language_profile: LanguageProfile) -> int:
        """
        Adds a new language profile to the storage,
        where the storage is a dictionary like {language: language_profile}
        :param language_profile: a language profile
        :return: 0 if succeeds, 1 if not
        """
        pass

    def detect(self, unknown_profile: LanguageProfile, k: int, trie_levels: Tuple[int]) -> Dict[str, int] or int:
        """
        Detects the language of an unknown profile and its score
        :param unknown_profile: a dictionary
        :param k: a number of the most common n-grams
        :param trie_levels: N-gram size - tuple with one int for score 8
        :return: a dictionary with language labels and their scores if input is correct, otherwise -1
        """
        pass


def calculate_probability(unknown_profile: LanguageProfile, known_profile: LanguageProfile,
                          k: int, trie_level: int) -> float or int:
    """
    Calculates probability of unknown_profile top_k ngrams in relation to known_profile
    :param unknown_profile: an instance of unknown profile
    :param known_profile: an instance of known profile
    :param k: number of most frequent ngrams
    :param trie_level: the size of ngrams
    :return: a probability of unknown top k ngrams
    """
    pass


# 10
class ProbabilityLanguageDetector(LanguageDetector):
    """
    Detects profile language using probabilities
    """

    def detect(self, unknown_profile: LanguageProfile, k: int, trie_levels: tuple) -> Dict[Tuple[
                                                                                               str, int], int or float] or int:
        """
        Detects the language of an unknown profile and its probability score
        :param unknown_profile: an instance of LanguageDetector
        :param k: a number of the most common n-grams
        :param trie_levels: N-gram size
        :return: sorted language labels with corresponding ngram size and their prob scores if input is correct, otherwise -1
        """
        pass
