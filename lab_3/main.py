"""
Lab 3
Language classification using n-grams
"""

from typing import Dict, Tuple
import re
import json
import math


# 4
def tokenize_by_sentence(text: str) -> tuple:
    """
    -->  (
         (('_', 's', 'h', 'e', '_'), ('_', 'i', 's', '_'), ('_', 'h', 'a', 'p', 'p', 'y', '_')),
         (('_', 'h', 'e', '_'), ('_', 'i', 's', '_'), ('_', 'h', 'a', 'p', 'p', 'y', '_'))
         )
    """
    pass

    if not isinstance(text, str):
        return ()
    useless_symbols = ['`', '~', '@', '*', '#', '$', '%', '^', '&', '(', ')', '_', '-', '+',
                       '=', '{', '[', ']', '}', '|', '\\', ':', ';', '"', "'", '<', ',', '>',
                       '/', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
    patterns = ('ö', 'ü', 'ä', 'ß')
    replacements = ('oe', 'ue', 'ae', 'ss')
    if text:
        last_letter = text[-1]
        if last_letter in ('.', '!', '?'):
            text = text[:-1]
    for symbol in useless_symbols:
        text = text.replace(symbol, '')
    if not text:
        return ()
    sentences = re.split(r'[.!?] ?', text.lower())
    text_output = []
    for sentence in sentences:
        new_tokens = []
        tokens = sentence.split()
        for token in tokens:
            for pattern, replacement in zip(patterns, replacements):
                token.replace(pattern, replacement)
            letters = []
            letters.insert(0, '_')
            for letter in token:
                letters.append(letter)
            letters.append('_')
            new_tokens.append(tuple(letters))
        text_output.append(tuple(new_tokens))
    return tuple(text_output)


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
        pass

        if not isinstance(letter, str):
            return -1
        if letter not in self.storage:
            self.storage[letter] = len(self.storage) + 1
        return 0

    def get_id_by_letter(self, letter: str) -> int:
        """
        Gets a unique id by a letter
        :param letter: a letter
        :return: an id
        """
        pass

        if not isinstance(letter, str) \
                or letter not in self.storage.keys():
            return -1
        letter_id = self.storage[letter]
        return letter_id

    def get_letter_by_id(self, letter_id: int) -> str or int:
        """
        Gets a letter by a unique id
        :param letter_id: a unique id
        :return: letter
        """
        pass

        if not isinstance(letter_id, int) \
                or letter_id not in self.storage.values():
            return -1
        for letter, id_letter in self.storage.items():
            if id_letter == letter_id:
                return letter

    def update(self, corpus: tuple) -> int:
        """
        Fills a storage by letters from the corpus
        :param corpus: a tuple of sentences
        :return: 0 if succeeds, 1 if not
        """
        pass

        if not isinstance(corpus, tuple):
            return -1
        for sentence in corpus:
            for token in sentence:
                for letter in token:
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
    pass

    if not isinstance(storage, LetterStorage) or not isinstance(corpus, tuple):
        return ()
    storage.update(corpus)
    encoded_corpus = []
    for sentence in corpus:
        encoded_sentences = []
        for token in sentence:
            encoded_tokens = []
            for letter in token:
                encoded_tokens.append(storage.get_id_by_letter(letter))
            encoded_sentences.append(tuple(encoded_tokens))
        encoded_corpus.append(tuple(encoded_sentences))
    return tuple(encoded_corpus)


# 4
def decode_corpus(storage: LetterStorage, corpus: tuple) -> tuple:
    """
    Decodes sentences by replacing letters with their ids
    :param storage: an instance of the LetterStorage class
    :param corpus: an encoded tuple of sentences
    :return: a tuple of the decoded sentences
    """
    pass

    if not isinstance(storage, LetterStorage) or not isinstance(corpus, tuple):
        return ()
    storage.update(corpus)
    decoded_corpus = []
    for sentence in corpus:
        decoded_sentences = []
        for token in sentence:
            decoded_tokens = []
            for letter in token:
                decoded_tokens.append(storage.get_letter_by_id(letter))
            decoded_sentences.append(tuple(decoded_tokens))
        decoded_corpus.append(tuple(decoded_sentences))
    return tuple(decoded_corpus)


# 6
class NGramTrie:
    """
    Stores and manages ngrams
    """

    def __init__(self, n: int, letter_storage: LetterStorage):

        # 6 - biGrams
        # 8 - threeGrams
        # 10 - nGrams

        self.size = n
        self.storage = letter_storage
        self.n_grams = []
        self.n_gram_frequencies = {}
        self.n_gram_log_probabilities = {}

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
        pass

        if not isinstance(encoded_corpus, tuple):
            return 1
        n_grams = []
        for encoded_sentence in encoded_corpus:
            n_gram_sentence = []
            for encoded_word in encoded_sentence:
                n_gram_word = []
                for i in range(len(encoded_word) - self.size + 1):
                    n_gram_word.append(tuple(encoded_word[i:i + self.size]))
                n_gram_sentence.append(tuple(n_gram_word))
            n_grams.append(tuple(n_gram_sentence))
        self.n_grams = tuple(n_grams)
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
        pass

        if not self.n_grams:
            return 1
        for n_gram_sentence in self.n_grams:
            for n_gram_word in n_gram_sentence:
                for n_gram in n_gram_word:
                    if n_gram not in self.n_gram_frequencies:
                        self.n_gram_frequencies[n_gram] = 1
                    else:
                        self.n_gram_frequencies[n_gram] += 1
        return 0

    # 8
    def extract_n_grams_frequencies(self, n_grams_dictionary: dict) -> int:
        """
        Extracts n_grams frequencies from given dictionary.
        Fills self.n_gram_frequency field.
        """
        pass

        if not isinstance(n_grams_dictionary, dict):
            return 1
        for n_gram, freq in n_grams_dictionary.items():
            if isinstance(n_gram, tuple) and isinstance(freq, int):
                self.n_gram_frequencies[n_gram] = freq
        return 0

    # 10
    def extract_n_grams_log_probabilities(self, n_grams_dictionary: dict) -> int:
        """
        Extracts n_grams log-probabilities from given dictionary.
        Fills self.n_gram_log_probabilities field.
        """
        pass
        if not isinstance(n_grams_dictionary, dict):
            return 1
        for n_gram in n_grams_dictionary:
            if isinstance(n_gram, tuple) and isinstance(n_grams_dictionary[n_gram], (int, float)):
                self.n_gram_log_probabilities[n_gram] = n_grams_dictionary[n_gram]
        return 0

    # 10
    def calculate_log_probabilities(self) -> int:
        """
        Gets log-probabilities of n-grams, fills the field n_gram_log_probabilities
        :return: 0 if succeeds, 1 if not
        """
        pass

        if not self.n_gram_frequencies:
            return 1
        for n_gram in self.n_gram_frequencies:
            amount = 0
            for other_n_gram in self.n_gram_frequencies:
                if n_gram[:self.size - 1] == other_n_gram[:self.size - 1]:
                    amount += self.n_gram_frequencies[other_n_gram]
            probability = self.n_gram_frequencies[n_gram] / amount
            self.n_gram_log_probabilities[n_gram] = math.log(probability)
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
        ngram_sizes = (2, 3)
        self.tries --> [<__main__.NGramTrie object at 0x09DB9BB0>,
        <__main__.NGramTrie object at 0x09DB9A48>]
        self.n_words --> [11, 9]
        self.tries[0].n_grams --> (
            (((1, 2), (2, 3), (3, 1)), ((1, 4), (4, 5), (5, 1)),
            ((1, 2), (2, 6), (6, 7), (7, 7), (7, 8), (8, 1))),
        )
        """
        pass

        if not isinstance(encoded_corpus, tuple) or not isinstance(ngram_sizes, tuple):
            return 1
        for ngram_size in ngram_sizes:
            trie = NGramTrie(ngram_size, self.storage)
            trie.extract_n_grams(encoded_corpus)
            trie.get_n_grams_frequencies()
            self.tries.append(trie)
            self.n_words.append(len(trie.n_gram_frequencies))
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
        pass

        if not isinstance(k, int) or not isinstance(trie_level, int):
            return ()
        if k < 1 or trie_level < 1:
            return ()
        for trie in self.tries:
            if trie.size == trie_level:
                sorted_n_grams_frequencies = sorted(trie.n_gram_frequencies.items(),
                                                    key=lambda x: x[1], reverse=True)
                sorted_n_grams = [i[0] for i in sorted_n_grams_frequencies]
                return tuple(sorted_n_grams[:k])
        return ()

    # 8
    def save(self, name: str) -> int:
        """
        Saves language profile into json file
        :param name: name of the json file with .json format
        :return: 0 if profile saves, 1 if any errors occurred
        """
        pass

        if not isinstance(name, str):
            return 1
        profile_dict = {}
        freq_dict = {}
        for trie in self.tries:
            for n_gram, freq in trie.n_gram_frequencies.items():
                decoded_n_grams = ''.join(self.storage.get_letter_by_id(letter_id)
                                          for letter_id in n_gram)
                freq_dict.update({decoded_n_grams: freq})
        profile_dict['freq'] = freq_dict
        profile_dict['n_words'] = self.n_words
        profile_dict['name'] = self.language
        with open(name, 'w', encoding='utf-8') as file:
            json.dump(profile_dict, file)
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
        pass

        if not isinstance(file_name, str):
            return 1
        with open(file_name, 'r', encoding='utf-8') as lang_profile_file:
            profile_dict = json.load(lang_profile_file)
        self.language = profile_dict['name']
        self.n_words = profile_dict['n_words']
        for key in profile_dict['freq'].keys():
            for letter in key:
                if letter not in self.storage.storage:
                    self.storage.storage[letter] = len(self.storage.storage) + 1
        n_gram_dict = {}
        n_gram_tuple = ()
        for n_gram, freq in profile_dict['freq'].items():
            if len(n_gram) not in n_gram_dict:
                n_gram_dict[len(n_gram)] = {}
            for letter in n_gram:
                n_gram_tuple += (self.storage.get_id_by_letter(letter),)
            n_gram_dict[len(n_gram)][n_gram_tuple] = freq
        for size, freq_dict in n_gram_dict.items():
            trie = NGramTrie(size, self.storage)
            trie.extract_n_grams_frequencies(freq_dict)
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
    pass

    if not isinstance(unknown_profile, LanguageProfile) \
            or not isinstance(known_profile, LanguageProfile) \
            or not isinstance(k, int) \
            or not isinstance(trie_level, int):
        return -1
    unknown_top_n_grams = unknown_profile.get_top_k_n_grams(k, trie_level)
    known_top_n_grams = known_profile.get_top_k_n_grams(k, trie_level)
    distance = 0
    len_known_top_n_grams = len(known_top_n_grams)
    for n_gram in unknown_top_n_grams:
        if n_gram in known_top_n_grams:
            distance += abs(known_top_n_grams.index(n_gram) - unknown_top_n_grams.index(n_gram))
        else:
            distance += len_known_top_n_grams
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
        pass

        if not isinstance(language_profile, LanguageProfile):
            return 1
        if language_profile not in self.language_profiles:
            self.language_profiles[language_profile.language] = language_profile
        return 0

    def detect(self, unknown_profile: LanguageProfile, k: int,
               trie_levels: Tuple[int]) -> Dict[str, int] or int:
        """
        Detects the language of an unknown profile and its score
        :param unknown_profile: a dictionary
        :param k: a number of the most common n-grams
        :param trie_levels: N-gram size - tuple with one int for score 8
        :return: a dictionary with language labels and their scores
        if input is correct, otherwise -1
        """
        pass

        if not isinstance(unknown_profile, LanguageProfile) \
                or not isinstance(k, int) \
                or not isinstance(trie_levels, tuple) \
                or not all(isinstance(i, int) for i in trie_levels):
            return -1
        lang_distance = {}
        for lang_name, lang_profile in self.language_profiles.items():
            distance = calculate_distance(unknown_profile, lang_profile, k, trie_levels[0])
            lang_distance[lang_name] = distance
        return lang_distance


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
    if not isinstance(unknown_profile, LanguageProfile) \
            or not isinstance(known_profile, LanguageProfile) \
            or not isinstance(k, int) \
            or not isinstance(trie_level, int):
        return -1
    probability = 0
    for known_trie in known_profile.tries:
        if known_trie.size == trie_level:
            known_trie.calculate_log_probabilities()
            unknown_k_n_grams = unknown_profile.get_top_k_n_grams(k, trie_level)
            for n_gram in unknown_k_n_grams:
                if n_gram in known_trie.n_gram_log_probabilities:
                    probability += known_trie.n_gram_log_probabilities[n_gram]
    return probability


# 10
class ProbabilityLanguageDetector(LanguageDetector):
    """
    Detects profile language using probabilities
    """

    def detect(self, unknown_profile: LanguageProfile, k: int,
               trie_levels: tuple) -> Dict[Tuple[str, int], int or float] or int:
        """
        Detects the language of an unknown profile and its probability score
        :param unknown_profile: an instance of LanguageDetector
        :param k: a number of the most common n-grams
        :param trie_levels: N-gram size
        :return: sorted language labels with corresponding ngram size
        and their prob scores if input is correct, otherwise -1
        """
        pass
        if not isinstance(unknown_profile, LanguageProfile) \
                or not isinstance(k, int) \
                or not isinstance(trie_levels, tuple):
            return -1
        detected_dict = {}
        for language, profile in self.language_profiles.items():
            for trie_level in trie_levels:
                detected_dict[(language, trie_level)] = calculate_probability(unknown_profile,
                                                                              profile,
                                                                              k,
                                                                              trie_level)
        return detected_dict
