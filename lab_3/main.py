"""
Lab 3
Language classification using n-grams
"""
import json
import math
from typing import Dict, Tuple
import re


def _split_into_letters(token: str) -> tuple:
    """
    Splits a token into letters, framed with '_'
    :param token: a token
    :return: a token split into letters
    """
    ascii_replacement = {"ä": "ae",
                         "ö": "oe",
                         "ü": "ue",
                         "ß": "ss"}
    # replace specified non-ascii letters
    for key, replacement in ascii_replacement.items():
        token.replace(key, replacement)
    # split into letters, remove punctuation
    token = [char for char in token if char.isalpha()]
    # append framing characters
    if token:
        token.insert(0, "_")
        token.append("_")
    return tuple(token)


def _tokenize(text: str) -> tuple:
    """
    Splits a text into tokens, tokens into letters
    Tokens are framed with '_'
    :param text: a text
    :return: a list of tokens split into letters
    """
    tokens = []
    for token in text.lower().split():
        token = _split_into_letters(token)
        if token:
            tokens.append(token)
    return tuple(tokens)


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
    if not isinstance(text, str):
        return ()
    sentences = []
    # The pattern matches a whitespace
    # preceded by sentence-ending punctuation and
    # followed by an uppercase letter
    for sentence in re.split(r"(?<=[!?.])\W(?=[\wäöüßÄÖÜẞ])", text):
        tokens = _tokenize(sentence)
        if tokens:
            sentences.append(tokens)
    return tuple(sentences)


# 4
class LetterStorage:
    """
    Stores and manages letters
    """

    def __init__(self):
        self._counter = 1
        self._letter_to_id = {}
        self._id_to_letter = {}

    # The reason I am using a getter/setter here is to reduce complexity
    # for get_letter_by_id from O(n) to O(1) by keeping a pair of dictionaries.
    @property
    def storage(self):
        """
        Stores letters and their ids
        """
        return self._letter_to_id

    @storage.setter
    def storage(self, value):
        self._letter_to_id = value
        for key, value in self._letter_to_id.items():
            self._id_to_letter[value] = key

    def _put_letter(self, letter: str) -> int:
        """
        Puts a letter into storage, assigns a unique id
        :param letter: a letter
        :return: 0 if succeeds, 1 if not
        """
        if not isinstance(letter, str) or not letter:
            return -1
        if letter not in self.storage:
            self._letter_to_id[letter] = self._counter
            self._id_to_letter[self._counter] = letter
            self._counter += 1
        return 0

    def get_id_by_letter(self, letter: str) -> int:
        """
        Gets a unique id by a letter
        :param letter: a letter
        :return: an id
        """
        if not isinstance(letter, str) or letter not in self._letter_to_id:
            return -1
        return self._letter_to_id[letter]

    def get_letter_by_id(self, letter_id: int) -> str or int:
        """
        Gets a letter by a unique id
        :param letter_id: a unique id
        :return: letter
        """
        if not isinstance(letter_id, int) or letter_id not in self._id_to_letter:
            return -1
        return self._id_to_letter[letter_id]

    def update(self, corpus: tuple) -> int:
        """
        Fills a storage by letters from the corpus
        :param corpus: a tuple of sentences
        :return: 0 if succeeds, 1 if not
        """
        if not isinstance(corpus, tuple):
            return -1
        for sentence in corpus:
            for token in sentence:
                for letter in token:
                    if self._put_letter(letter) == -1:
                        return -1
        return 0

    def encode(self, string: str) -> tuple:
        """
        Encodes a string of letters as a tuple of letter ids, adding them to storage if necessary
        :param string: a string of letters
        :return: a tuple of letter ids
        """
        ids = []
        # While encoding, add letters to storage if they have not been added already
        for letter in string:
            self._put_letter(letter)
            ids.append(self.get_id_by_letter(letter))
        return tuple(ids)

    def decode(self, id_tuple: tuple) -> str:
        """
        Decodes a tuple of ids to a string of letters
        :param id_tuple: a tuple of letter ids
        :return: a string of letters
        """
        return "".join(self.get_letter_by_id(letter_id) for letter_id in id_tuple)


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
    storage.update(corpus)
    # Create a tuple structure identical to corpus, with ids instead of letters.
    # Using single-letter names for letter, token and sentence because i can't think of a way
    # to break this line in a way that doesn't hurt readability
    return tuple(tuple(tuple(storage.get_id_by_letter(c) for c in t) for t in s) for s in corpus)


# 4
def decode_corpus(storage: LetterStorage, corpus: tuple) -> tuple:
    """
    Decodes sentences by replacing letters with their ids
    :param storage: an instance of the LetterStorage class
    :param corpus: an encoded tuple of sentences
    :return: a tuple of the decoded sentences
    """
    if not isinstance(storage, LetterStorage) or not isinstance(corpus, tuple):
        return ()
    # Create a tuple structure identical to corpus, with letters instead of ids.
    return tuple(tuple(tuple(storage.get_letter_by_id(i) for i in t) for t in s) for s in corpus)


def _word_to_n_gram(word: tuple, size: int) -> tuple:
    return tuple(word[i:i+size] for i in range(len(word)-size+1))


# 6
class NGramTrie:
    """
    Stores and manages ngrams
    """

    def __init__(self, n: int, letter_storage: LetterStorage):
        self.size = n
        self.storage = letter_storage
        self.n_grams = []
        self.n_gram_frequencies = {}
        self.n_gram_log_probabilities = {}

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
        if not isinstance(encoded_corpus, tuple):
            return 1
        # Apply _word_to_n_gram to each word
        n_grams = tuple(tuple(_word_to_n_gram(w, self.size) for w in s) for s in encoded_corpus)
        # Remove any empty tuples.
        # Cannot combine the two steps without sacrificing performance or readability.
        self.n_grams = tuple(tuple(w for w in s if w) for s in n_grams if s)
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
        if not self.n_grams:
            return 1
        for sentence in self.n_grams:
            for word in sentence:
                for n_gram in word:
                    if n_gram not in self.n_gram_frequencies:
                        self.n_gram_frequencies[n_gram] = 0
                    self.n_gram_frequencies[n_gram] += 1
        return 0

    # 8
    def extract_n_grams_frequencies(self, n_grams_dictionary: dict) -> int:
        """
        Extracts n_grams frequencies from given dictionary.
        Fills self.n_gram_frequency field.
        """
        if not isinstance(n_grams_dictionary, dict):
            return 1
        for key, value in n_grams_dictionary.items():
            if isinstance(key, tuple) and isinstance(value, int):
                self.n_gram_frequencies[key] = value
        return 0

    # 10
    def extract_n_grams_log_probabilities(self, n_grams_dictionary: dict) -> int:
        """
        Extracts n_grams log-probabilities from given dictionary.
        Fills self.n_gram_log_probabilities field.
        """
        if not isinstance(n_grams_dictionary, dict):
            return 1
        for n_gram, probability in n_grams_dictionary.items():
            if isinstance(n_gram, tuple) and isinstance(probability, float):
                self.n_gram_log_probabilities[n_gram] = probability
        return 0

    # 10
    def calculate_log_probabilities(self) -> int:
        """
        Gets log-probabilities of n-grams, fills the field n_gram_log_probabilities
        :return: 0 if succeeds, 1 if not
        """
        if not self.n_gram_frequencies:
            return 1
        for n_gram, frequency in self.n_gram_frequencies.items():
            frequencies = 0
            for adjacent_n_gram, adjacent_frequency in self.n_gram_frequencies.items():
                if adjacent_n_gram[:-1] == n_gram[:-1]:
                    frequencies += adjacent_frequency
            self.n_gram_log_probabilities[n_gram] = math.log(frequency / frequencies, math.e)
        return 0


# 6
class LanguageProfile:
    """
    Stores and manages language profile information
    """

    def __init__(self, letter_storage: LetterStorage, language_name: str):
        self.storage = letter_storage
        self.language = language_name
        self.tries = []
        self.n_words = []

    def create_from_tokens(self, encoded_corpus: tuple, ngram_sizes: tuple) -> int:
        """
        Creates a language profile
        :param encoded_corpus: a corpus of encoded letters
        :param ngram_sizes: a tuple of ngram sizes,
            e.g. (1, 2, 3) will indicate the function to create 1,2,3-grams
        :return: 0 if succeeds, 1 if not
        e.g.
        encoded_corpus = (((1, 2, 3, 1), (1, 4, 5, 1), (1, 2, 6, 7, 7, 8, 1)),)
        ngram_sizes = (2, 3)

        self.tries --> [<__main__.NGramTrie object at 0x09DB9BB0>,
                        <__main__.NGramTrie object at 0x09DB9A48>]
        self.n_words --> [11, 9]
        self.tries[0].n_grams --> (
            (((1, 2), (2, 3), (3, 1)),
             ((1, 4), (4, 5), (5, 1)),
             ((1, 2), (2, 6), (6, 7), (7, 7), (7, 8), (8, 1))),
        )
        """
        if not isinstance(encoded_corpus, tuple) or not isinstance(ngram_sizes, tuple):
            return 1
        for size in ngram_sizes:
            n_gram_trie = NGramTrie(size, self.storage)
            if n_gram_trie.extract_n_grams(encoded_corpus):
                return 1
            if n_gram_trie.get_n_grams_frequencies():
                return 1
            self.tries.append(n_gram_trie)
            self.n_words.append(len(n_gram_trie.n_gram_frequencies))
        return 0

    def get_trie_by_level(self, trie_level: int) -> NGramTrie or None:
        """
        Gets NGramTrie of the requested N-gram size
        :param trie_level: N-gram size
        :return: NGramTrie if succeeds, None if not
        """
        for trie in self.tries:
            if trie.size == trie_level:
                return trie
        return None

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
        if not isinstance(k, int) or not isinstance(trie_level, int):
            return ()
        if k <= 0:
            return ()
        trie = self.get_trie_by_level(trie_level)
        if not trie:
            return ()
        frequencies = trie.n_gram_frequencies
        return tuple(sorted(frequencies, key=frequencies.get, reverse=True)[:k])

    # 8
    def save(self, name: str) -> int:
        """
        Saves language profile into json file
        :param name: name of the json file with .json format
        :return: 0 if profile saves, 1 if any errors occurred
        """
        if not isinstance(name, str):
            return 1
        profile = {"name": self.language,
                   "n_words": self.n_words}
        freq = {}
        for n_gram_trie in self.tries:
            for n_gram, frequency in n_gram_trie.n_gram_frequencies.items():
                freq[self.storage.decode(n_gram)] = frequency
        profile["freq"] = freq
        with open(name, "w", encoding="utf-8") as file:
            json.dump(profile, file)
        return 0

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
        if not isinstance(file_name, str):
            return 1
        with open(file_name, encoding="utf-8") as file:
            profile = json.load(file)
        self.language = profile["name"]
        self.n_words = profile["n_words"]
        tries_dict = {}
        for n_gram, frequency in profile["freq"].items():
            if not len(n_gram) in tries_dict:
                tries_dict[len(n_gram)] = NGramTrie(len(n_gram), self.storage)
            tries_dict[len(n_gram)].n_gram_frequencies[self.storage.encode(n_gram)] = frequency
        self.tries = list(tries_dict.values())
        return 0


def create_profile_from_text(text: str, storage: LetterStorage, ngram_sizes: tuple,
                             language_name: str) -> LanguageProfile or None:
    """
    Convenient shorthand for creating a language profile and applying all expected steps.
    :param text: a text to be turned into a profile
    :param storage: a letter storage
    :param ngram_sizes: a tuple of ngram sizes
    :param language_name: profile name
    :return: created profile
    """
    if (not isinstance(text, str)
            or not isinstance(storage, LetterStorage)
            or not isinstance(ngram_sizes, tuple)
            or not isinstance(language_name, str)):
        return None
    corpus = tokenize_by_sentence(text)
    storage.update(corpus)
    profile = LanguageProfile(storage, language_name)
    profile.create_from_tokens(encode_corpus(storage, corpus), ngram_sizes)
    return profile


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
    Например, первый набор N-грамм для неизвестного профиля -
    first_n_grams = ((1, 2), (4, 5), (2, 3)),
    второй набор N-грамм для известного профиля – second_n_grams = ((1, 2), (2, 3), (4, 5)).
    Расстояние для (1, 2) равно 0, так как индекс в первом наборе – 0, во втором – 0, |0 – 0| = 0.
    Расстояние для (4, 5) равно 1, расстояние для (2, 3) равно 1.
    Соответственно расстояние между наборами равно 2.
    """
    if (not isinstance(unknown_profile, LanguageProfile)
            or not isinstance(known_profile, LanguageProfile)
            or not isinstance(k, int)
            or not isinstance(trie_level, int)):
        return -1
    n_grams_first = unknown_profile.get_top_k_n_grams(k, trie_level)
    n_grams_second = known_profile.get_top_k_n_grams(k, trie_level)
    distance = 0
    for index, n_gram in enumerate(n_grams_first):
        if n_gram in n_grams_second:
            distance += abs(index - n_grams_second.index(n_gram))
        else:
            distance += len(n_grams_second)
    return distance


# 8
class LanguageDetector:
    """
    Detects profile language using distance
    """

    def __init__(self):
        self.language_profiles = {}

    def register_language(self, language_profile: LanguageProfile) -> int:
        """
        Adds a new language profile to the storage,
        where the storage is a dictionary like {language: language_profile}
        :param language_profile: a language profile
        :return: 0 if succeeds, 1 if not
        """
        if not isinstance(language_profile, LanguageProfile):
            return 1
        self.language_profiles[language_profile.language] = language_profile
        return 0

    def detect(self, unknown_profile: LanguageProfile, k: int,
               trie_levels: Tuple[int]) -> Dict[str, int] or int:
        """
        Detects the language of an unknown profile and its score
        :param unknown_profile: a dictionary
        :param k: a number of the most common n-grams
        :param trie_levels: N-gram size - tuple with one int for score 8
        :return: a dictionary with language labels and their scores if input is correct,
            otherwise -1
        """
        if (not isinstance(unknown_profile, LanguageProfile)
                or not isinstance(k, int)
                or not isinstance(trie_levels, tuple)):
            return -1
        distances = {}
        for language, profile in self.language_profiles.items():
            distances[language] = calculate_distance(unknown_profile, profile, k, trie_levels[0])
        return distances


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
    if (not isinstance(unknown_profile, LanguageProfile)
            or not isinstance(known_profile, LanguageProfile)
            or not isinstance(k, int)
            or not isinstance(trie_level, int)):
        return -1
    trie = known_profile.get_trie_by_level(trie_level)
    trie.calculate_log_probabilities()
    probability = 0
    for n_gram in unknown_profile.get_top_k_n_grams(k, trie_level):
        if n_gram in trie.n_gram_log_probabilities:
            probability += trie.n_gram_log_probabilities[n_gram]
    return probability


# 10
class ProbabilityLanguageDetector(LanguageDetector):
    """
    Detects profile language using probabilities
    """

    def detect(self, unknown_profile: LanguageProfile, k: int, trie_levels: tuple) -> \
            Dict[Tuple[str, int], int or float] or int:
        """
        Detects the language of an unknown profile and its probability score
        :param unknown_profile: an instance of LanguageDetector
        :param k: a number of the most common n-grams
        :param trie_levels: N-gram size
        :return: sorted language labels with corresponding ngram size and their prob scores
            if input is correct, otherwise -1
        """
        if (not isinstance(unknown_profile, LanguageProfile)
                or not isinstance(k, int)
                or not isinstance(trie_levels, tuple)):
            return -1
        probabilities = {}
        for language, profile in self.language_profiles.items():
            probabilities[language] = calculate_probability(unknown_profile,
                                                            profile, k, trie_levels[0])
        return probabilities
