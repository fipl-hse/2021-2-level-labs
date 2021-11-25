"""
Lab 3
Language classification using n-grams
"""
import json
from math import fabs, log
from typing import Dict, Tuple
import re


# 4
def split_words(token: str) -> tuple:
    """
    Splits a word into letters and add '_'
    :param token: a token
    :return: a token split into letters
    """
    # deutsch_letters = {"ä": "ae", "ü": "ue", "ß": "ss", "ö": "oe"}
    # for key in deutsch_letters.items():
    #    token = token.replace(key[0], key[1])
    skip_signs = ["'", "-", "%", ">", "<", "$", "@", "#", "&", "*", ",", ".", "!", ":", "º"]
    token_list = []
    for sign in skip_signs:
        token.replace(sign, '')
    for element in token:
        if element.isalpha():
            token_list.append(element)
    if token_list:
        token_list.insert(0, "_")
        token_list.append("_")
    return tuple(token_list)


def deep_tokenization(text: str) -> tuple:
    """
    Splits a text into tokens and tokens into letters
    :param text: a text
    :return: a list of tokens split into letters
    """
    tokens = []
    for token in text.lower().split():
        token = split_words(token)
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
    list_of_sentence = []
    for line in text.splitlines():
        for sentence in re.split(r"([!?.])", line):
            tokens = deep_tokenization(sentence)
            if tokens:
                list_of_sentence.append(tokens)
    return tuple(list_of_sentence)


# 4
class LetterStorage:
    """
    Stores and manages letters
    """

    def __init__(self):
        self.storage = {}

    def _put_letter(self, letter: str) -> int:
        """
        Puts a letter into storage, assigns a unique id
        :param letter: a letter
        :return: 0 if succeeds, 1 if not
        """
        if not isinstance(letter, str) or not letter:
            return -1
        if letter in self.storage:
            return 0
        self.storage[letter] = len(self.storage) + 1
        return 0

    def get_id_by_letter(self, letter: str) -> int:
        """
        Gets a unique id by a letter
        :param letter: a letter
        :return: an id
        """
        if not isinstance(letter, str) or letter not in self.storage.keys():
            return -1
        return self.storage[letter]

    def get_letter_by_id(self, letter_id: int) -> str or int:
        """
        Gets a letter by a unique id
        :param letter_id: a unique id
        :return: letter
        """
        if not isinstance(letter_id, int) or letter_id not in self.storage.values():
            return -1
        for letter, ids in self.storage.items():
            if ids == letter_id:
                final_letter = letter
        return final_letter

    def update(self, corpus: tuple) -> int:
        """
        Fills a storage by letters from the corpus
        :param corpus: a tuple of sentences
        :return: 0 if succeeds, 1 if not
        """
        if not isinstance(corpus, tuple):
            return -1
        if not corpus:
            return 0
        for sentence in corpus:
            for word in sentence:
                for letter in word:
                    if self._put_letter(letter) == -1:
                        return -1
        return 0

    def update_letter(self, letter: str) -> int:
        """
        Fills a storage with a letter
        :param letter: a letter
        :return: 0 if succeeds, 1 if not
        """
        if not isinstance(letter, str):
            return 1
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
    storage.update(corpus)
    last_tuple = tuple(tuple(tuple(storage.get_id_by_letter(letter)
                                   for letter in word) for word in sentence) for sentence in corpus)
    return last_tuple


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
    last_tuple = tuple(tuple(tuple(storage.get_letter_by_id(letter)
                                   for letter in word) for word in sentence) for sentence in corpus)
    return last_tuple


# 6
class NGramTrie:
    """
    Stores and manages ngrams
    """

    def __init__(self, n: int, letter_storage: LetterStorage):
        self.n_gram_log_probabilities = {}
        self.size = n
        self.storage = letter_storage
        self.n_grams = []
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
        if not isinstance(encoded_corpus, tuple):
            return 1
        list_n_gramms = []
        final_list = []
        for i in encoded_corpus:
            for element in i:
                seq = [element[q:] for q in range(self.size)]
                n_gramm = tuple(zip(*seq))
                if n_gramm == ():
                    continue
                list_n_gramms.append(n_gramm)
        final_list.append(tuple(list_n_gramms))
        self.n_grams = tuple(final_list)
        if self.n_grams[0] == ():
            self.n_grams = []
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
        for i in self.n_grams:
            for n_gramm in i:
                for element in n_gramm:
                    if element in self.n_gram_frequencies:
                        self.n_gram_frequencies[element] += 1
                    else:
                        self.n_gram_frequencies[element] = 1
        return 0

    # 8
    def extract_n_grams_frequencies(self, n_grams_dictionary: dict) -> int:
        """
        Extracts n_grams frequencies from given dictionary.
        Fills self.n_gram_frequency field.
        """
        if not isinstance(n_grams_dictionary, dict):
            return 1
        for i in n_grams_dictionary.items():
            if isinstance(i[0], tuple) and isinstance(i[1], int):
                self.n_gram_frequencies[i[0]] = i[1]
        return 0

    # 10
    def extract_n_grams_log_probabilities(self, n_grams_dictionary: dict) -> int:
        """
        Extracts n_grams log-probabilities from given dictionary.
        Fills self.n_gram_log_probabilities field.
        """
        if not isinstance(n_grams_dictionary, dict):
            return 1
        for i in n_grams_dictionary.items():
            if isinstance(i[0], tuple) and isinstance(i[1], float):
                self.n_gram_log_probabilities[i[0]] = i[1]
        return 0

    # 10
    def calculate_log_probabilities(self) -> int:
        """
        Gets log-probabilities of n-grams, fills the field n_gram_log_probabilities
        :return: 0 if succeeds, 1 if not
        """
        if not self.n_gram_frequencies:
            return 1

        for n_gram in self.n_gram_frequencies:
            probability = self.n_gram_frequencies[n_gram] / \
                          sum([self.n_gram_frequencies[other_n_gram]
                               for other_n_gram in self.n_gram_frequencies
                               if n_gram[:self.size - 1] == other_n_gram[:self.size - 1]])
            self.n_gram_log_probabilities[n_gram] = log(probability)
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
        :param letters: a tuple of encoded letters
        :param ngram_sizes: a tuple of ngram sizes,
            e.g. (1, 2, 3) will indicate the function to create 1,2,3-grams
        :return: 0 if succeeds, 1 if not
        e.g.
        encoded_corpus = (((1, 2, 3, 1), (1, 4, 5, 1), (1, 2, 6, 7, 7, 8, 1)),)
        _sizes = (2, 3)
        self.tries --> [<__main__.NGramTrie object at 0x09DB9BB0>,
         <__main__.NGramTrie object at 0x09DB9A48>]
        self.n_words --> [11, 9]
        self.tries[0].n_grams --> (
            (((1, 2), (2, 3), (3, 1)), ((1, 4), (4, 5),
            (5, 1)), ((1, 2), (2, 6), (6, 7), (7, 7), (7, 8), (8, 1))),
        )
        """
        if not isinstance(encoded_corpus, tuple) or not isinstance(ngram_sizes, tuple):
            return 1
        for size in ngram_sizes:
            n_gramm = NGramTrie(size, self.storage)
            self.tries.append(n_gramm)
            n_gramm.extract_n_grams(encoded_corpus)
            n_gramm.get_n_grams_frequencies()
            self.n_words.append(len(n_gramm.n_gram_frequencies))
        return 0

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
        if not isinstance(k, int) or not isinstance(trie_level, int) or k <= 0:
            return ()
        some_ngram = ''
        for i in self.tries:
            if i.size == trie_level:
                some_ngram = i
        if some_ngram == '':
            return ()
        some_ngram.get_n_grams_frequencies()
        dict_freq = dict(sorted(some_ngram.n_gram_frequencies.items(),
                                key=lambda x: x[1], reverse=True)[:k])
        top_k_ngrams = tuple(dict_freq.keys())
        return top_k_ngrams

    # 8
    def save(self, file_name: str) -> int:
        """
        Saves language profile into json file
        :param file_name: name of the json file with .json format
        :return: 0 if profile saves, 1 if any errors occurred
        """
        if not isinstance(file_name, str):
            return 1
        with open(file_name, 'w', encoding="utf-8") as file:
            data = {"name": self.language, "n_words": self.n_words}
            formatted_freq = {}
            for trie in self.tries:
                for ngram in trie.n_gram_frequencies:
                    new_ngram = ''
                    for letter_id in ngram:
                        new_ngram += self.storage.get_letter_by_id(letter_id)
                    formatted_freq[new_ngram] = trie.n_gram_frequencies[ngram]
            data["freq"] = formatted_freq
            json.dump(data, file)
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

        with open(file_name, "r", encoding="utf-8") as file:
            data = json.load(file)
            self.language = data['name']
            self.n_words = data['n_words']
            decoded_ngrams = []
            for ngram in data['freq']:
                decoded_ngram = []
                for letter in ngram:
                    self.storage.update_letter(letter)
                    decoded_ngram.append(self.storage.get_id_by_letter(letter))
                decoded_ngrams.append((tuple(decoded_ngram), data['freq'][ngram]))
            ngram_sizes_dict = {}
            for ngram in decoded_ngrams:
                size = len(ngram[0])
                if size not in ngram_sizes_dict:
                    ngram_sizes_dict[size] = {}
                ngram_sizes_dict[size][ngram[0]] = ngram[1]
            for size, group in ngram_sizes_dict.items():
                trie = NGramTrie(size, self.storage)
                trie.n_gram_frequencies = group
                self.tries.append(trie)
        return 0


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
    Например, первый набор N-грамм для неизвестного профиля
     - first_n_grams = ((1, 2), (4, 5), (2, 3)),
    второй набор N-грамм для известного профиля – second_n_grams = ((1, 2), (2, 3), (4, 5)).
    Расстояние для (1, 2) равно 0, так как индекс в первом наборе – 0, во втором – 0, |0 – 0| = 0.
    Расстояние для (4, 5) равно 1, расстояние для (2, 3) равно 1.
    Соответственно расстояние между наборами равно 2.
    """
    if not isinstance(unknown_profile, LanguageProfile) \
            or not isinstance(known_profile, LanguageProfile) \
            or not isinstance(k, int) or not isinstance(trie_level, int):
        return -1
    unknown_k_n_grams = unknown_profile.get_top_k_n_grams(k, trie_level)
    known_k_n_grams = known_profile.get_top_k_n_grams(k, trie_level)
    distance = 0
    for i in enumerate(unknown_k_n_grams):
        for element in enumerate(known_k_n_grams):
            if i[1] not in known_k_n_grams:
                distance += len(known_k_n_grams)
                break
            if i[1] == element[1]:
                distance += fabs(i[0] - element[0])
    return int(distance)


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

    def detect(self, unknown_profile: LanguageProfile,
               k: int, trie_levels: Tuple[int]) -> Dict[str, int] or int:
        """
        Detects the language of an unknown profile and its score
        :param unknown_profile: a dictionary
        :param k: a number of the most common n-grams
        :param trie_levels: N-gram size - tuple with one int for score 8
        :return: a dictionary with language labels
        and their scores if input is correct, otherwise -1
        """
        if not isinstance(unknown_profile, LanguageProfile) or not isinstance(k, int) or \
                not isinstance(trie_levels, Tuple):
            return -1
        return_dict = {}
        for i in self.language_profiles.values():
            distance = calculate_distance(unknown_profile, i, k, trie_levels[0])
            return_dict[i.language] = distance
        return return_dict


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
    if not isinstance(unknown_profile, LanguageProfile) \
            or not isinstance(known_profile, LanguageProfile) \
            or not isinstance(k, int) or not isinstance(trie_level, int):
        return -1
    known_trie = NGramTrie
    for trie in known_profile.tries:
        if trie.size == trie_level:
            known_trie = trie
            break
    common_probability = 0
    known_trie.calculate_log_probabilities()
    unk_k_gramms = unknown_profile.get_top_k_n_grams(k, trie_level)
    for i in unk_k_gramms:
        if i in known_trie.n_gram_log_probabilities:
            common_probability += known_trie.n_gram_log_probabilities[i]
    return common_probability


# 10
class ProbabilityLanguageDetector(LanguageDetector):
    """
    Detects profile language using probabilities
    """

    def detect(self, unknown_profile: LanguageProfile,
               k: int, trie_levels: tuple) -> Dict[Tuple[str, int], int or float] or int:
        """
        Detects the language of an unknown profile and its probability score
        :param unknown_profile: an instance of LanguageDetector
        :param k: a number of the most common n-grams
        :param trie_levels: N-gram size
        :return: sorted language labels with corresponding
          size and their prob scores if input is correct, otherwise -1
        """
        if not isinstance(unknown_profile, LanguageProfile) \
                or not isinstance(k, int) or not isinstance(trie_levels, tuple):
            return -1
        detected_dict = {}
        for language_profile in self.language_profiles.values():
            for language_trie in language_profile.tries:
                for trie_level in trie_levels:
                    if trie_level == language_trie.size:
                        detected_dict[(language_profile.language, language_trie.size)] = \
                            calculate_probability(unknown_profile, language_profile, k, trie_level)
        return detected_dict
