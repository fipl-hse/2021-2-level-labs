"""
Lab 3
Language classification using n-grams
"""

from typing import Dict, Tuple
import json
import math


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

    invaluable_trash = ['`', '~', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '-', '+',
                        '=', '{', '[', ']', '}', '|', '\\', ':', ';', '"', "'", '<', ',', '>',
                        '/', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
    text = text.lower()

    for symbols in invaluable_trash:
        text = text.replace(symbols, '')

    if not text:
        return ()

    if text:
        last_character = text[-1]
        if last_character == '.' or last_character == '!' or last_character == '?':
            text = text[:-1]

    text = text.replace('.', '<stop>')
    text = text.replace('?', '<stop>')
    text = text.replace('!', '<stop>')

    #text = text.replace('ü', 'ue')
    #text = text.replace('ö', 'oe')
    #text = text.replace('ä', 'ae')
    #text = text.replace('ß', 'ss')

    sentences = text.split('<stop>')

    processed_sentences = []

    for sentence in sentences:
        tokens = sentence.split()

        processed_tokens = []

        for token in tokens:
            processed_characters = ['_']

            for character in token:
                processed_characters.append(character)

            processed_characters.append('_')

            processed_tokens.append(tuple(processed_characters))

        processed_sentences.append(tuple(processed_tokens))

    return tuple(processed_sentences)


# 4
class LetterStorage:
    """
    Stores and manages letters
    """

    free_id = 1

    def __init__(self):
        self.storage = {}

    def _put_letter(self, letter: str) -> int:
        """
        Puts a letter into storage, assigns a unique id
        :param letter: a letter
        :return: 0 if succeeds, 1 if not
        """

        if not isinstance(letter, str):
            return -1

        if letter not in self.storage:
            self.storage[letter] = self.free_id
            self.free_id += 1

        return 0

    def get_id_by_letter(self, letter: str) -> int:
        """
        Gets a unique id by a letter
        :param letter: a letter
        :return: an id
        """

        if not isinstance(letter, str):
            return -1

        if letter in self.storage:
            return self.storage[letter]

        return -1

    def get_letter_by_id(self, letter_id: int) -> str or int:
        """
        Gets a letter by a unique id
        :param letter_id: a unique id
        :return: letter
        """

        if not isinstance(letter_id, int):
            return -1

        for letter, character_id in self.storage.items():
            if character_id == letter_id:
                return letter

        return -1

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
                for character in token:
                    self._put_letter(character)

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

    encoded_corpus = []

    for sentence in corpus:
        encoded_sentence = []

        for token in sentence:
            encoded_token = []

            for character in token:
                encoded_token.append(storage.get_id_by_letter(character))

            encoded_sentence.append(tuple(encoded_token))

        encoded_corpus.append(tuple(encoded_sentence))

    return tuple(encoded_corpus)


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

    encoded_corpus = []

    for sentence in corpus:
        encoded_sentence = []

        for token in sentence:
            encoded_token = []

            for character in token:
                encoded_token.append(storage.get_letter_by_id(character))

            encoded_sentence.append(tuple(encoded_token))

        encoded_corpus.append(tuple(encoded_sentence))

    return tuple(encoded_corpus)


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
            return -1

        processed_corpus = []

        for encoded_sentence in encoded_corpus:
            processed_sentence = []
            for encoded_token in encoded_sentence:
                processed_token = []
                start_index = 0
                end_index = start_index + self.size

                while end_index <= len(encoded_token):
                    n_gram = []

                    for index in range(start_index, end_index):
                        n_gram.append(encoded_token[index])

                    start_index += 1
                    end_index += 1

                    processed_token.append(tuple(n_gram))

                if processed_token:
                    processed_sentence.append(tuple(processed_token))

            if processed_sentence:
                processed_corpus.append(tuple(processed_sentence))

        self.n_grams = tuple(processed_corpus)

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

        n_gram_frequencies = {}

        for processed_sentence in self.n_grams:
            for processed_token in processed_sentence:
                for n_gram in processed_token:
                    if n_gram not in n_gram_frequencies:
                        n_gram_frequencies[n_gram] = 1
                    else:
                        n_gram_frequencies[n_gram] += 1

        self.n_gram_frequencies = n_gram_frequencies

        return 0

    # 8
    def extract_n_grams_frequencies(self, n_grams_dictionary: dict) -> int:
        """
        Extracts n_grams frequencies from given dictionary.
        Fills self.n_gram_frequency field.
        """

        if not isinstance(n_grams_dictionary, dict):
            return 1

        for n_gram in n_grams_dictionary:
            if isinstance(n_gram, tuple):
                self.n_gram_frequencies[n_gram] = n_grams_dictionary[n_gram]

        return 0

    # 10
    def extract_n_grams_log_probabilities(self, n_grams_dictionary: dict) -> int:
        """
        Extracts n_grams log-probabilities from given dictionary.
        Fills self.n_gram_log_probabilities field.
        """
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

        if not self.n_gram_frequencies:
            return 1

        log_probabilities = {}

        for ngram in self.n_gram_frequencies:
            number = 0

            for other_ngram in self.n_gram_frequencies:
                if other_ngram[0:len(other_ngram) - 1] == ngram[0:len(ngram) - 1]:
                    number += self.n_gram_frequencies[other_ngram]

            probability = self.n_gram_frequencies[ngram] / number

            log_probabilities[ngram] = math.log(probability)

        self.n_gram_log_probabilities = log_probabilities

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

        self.tries --> [<__main__.NGramTrie object at 0x09DB9BB0>, <__main__.NGramTrie object at 0x09DB9A48>]
        self.n_words --> [11, 9]
        self.tries[0].n_grams --> (
            (((1, 2), (2, 3), (3, 1)), ((1, 4), (4, 5), (5, 1)), ((1, 2), (2, 6), (6, 7), (7, 7), (7, 8), (8, 1))),
        )
        """

        if not isinstance(encoded_corpus, tuple) or not isinstance(ngram_sizes, tuple):
            return 1

        for ngram_size in ngram_sizes:
            self.tries.append(NGramTrie(ngram_size, self.storage))

        for trie in self.tries:
            trie.extract_n_grams(encoded_corpus)
            trie.get_n_grams_frequencies()
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

        if not isinstance(k, int) or not isinstance(trie_level, int):
            return ()

        if k < 1 or trie_level < 1:
            return ()

        for trie in self.tries:
            if trie.size == trie_level:
                most_common_ngrams_freqs = sorted(trie.n_gram_frequencies.items(), key=lambda x: -x[1])
                most_common_ngrams, _ = zip(*most_common_ngrams_freqs)
                return tuple(most_common_ngrams[:k])

        return ()

    # 8
    def save(self, file_name: str) -> int:
        """
        Saves language profile into json file
        :param file_name: name of the json file with .json format
        :return: 0 if profile saves, 1 if any errors occurred
        """

        if not isinstance(file_name, str):
            return 1

        with open(file_name, 'w') as file:
            data = {"name": self.language, "n_words": self.n_words}

            formatted_freq = {}

            for trie in self.tries:
                for ngram in trie.n_gram_frequencies:
                    formatted_ngram = ''

                    for letter_id in ngram:
                        formatted_ngram += self.storage.get_letter_by_id(letter_id)

                    formatted_freq[formatted_ngram] = trie.n_gram_frequencies[ngram]

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

        with open(file_name, "r") as file:
            data = json.load(file)

            self.language = data['name']
            self.n_words = data['n_words']

            decoded_ngrams = []

            for ngram in data['freq']:
                decoded_ngram = []

                for letter in ngram:
                    self.storage._put_letter(letter)
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

    # my code
    def get_trie(self, trie_level: int):
        for trie in self.tries:
            if trie_level == trie.size:
                return trie

        return None


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

    if not isinstance(unknown_profile, LanguageProfile) or not isinstance(known_profile, LanguageProfile)\
            or not isinstance(k, int) or not isinstance(trie_level, int):
        return -1

    unknown_top_ngrams = unknown_profile.get_top_k_n_grams(k, trie_level)
    known_top_ngrams = known_profile.get_top_k_n_grams(k, trie_level)

    distance = 0

    known_top_ngrams_len = len(known_top_ngrams)

    for ngram in unknown_top_ngrams:
        if ngram in known_top_ngrams:
            distance += abs(known_top_ngrams.index(ngram) - unknown_top_ngrams.index(ngram))
        else:
            distance += known_top_ngrams_len

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

    def detect(self, unknown_profile: LanguageProfile, k: int, trie_levels: Tuple[int]) -> Dict[str, int] or int:
        """
        Detects the language of an unknown profile and its score
        :param unknown_profile: a dictionary
        :param k: a number of the most common n-grams
        :param trie_levels: N-gram size - tuple with one int for score 8
        :return: a dictionary with language labels and their scores if input is correct, otherwise -1
        """

        if not isinstance(unknown_profile, LanguageProfile) or not isinstance(k, int)\
                or not isinstance(trie_levels, tuple):
            return -1

        result_dict = {}

        for language in self.language_profiles:
            result_dict[language] = calculate_distance(unknown_profile,
                                                       self.language_profiles[language],
                                                       k,
                                                       trie_levels[0])

        return result_dict


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

    if not isinstance(unknown_profile, LanguageProfile) or not isinstance(known_profile, LanguageProfile)\
            or not isinstance(k, int) \
            or not isinstance(trie_level, int):
        return -1

    result = 0

    unknown_top_n_grams = unknown_profile.get_top_k_n_grams(k, trie_level)

    known_trie = known_profile.get_trie(trie_level)
    known_trie.calculate_log_probabilities()

    for unknown_ngram in unknown_top_n_grams:
        if unknown_ngram in known_trie.n_gram_frequencies:
            result += known_trie.n_gram_log_probabilities[unknown_ngram]

    return result


# 10
class ProbabilityLanguageDetector(LanguageDetector):
    """
    Detects profile language using probabilities
    """

    def detect(self, unknown_profile: LanguageProfile, k: int, trie_levels: tuple)\
            -> Dict[Tuple[str, int], int or float] or int:
        """
        Detects the language of an unknown profile and its probability score
        :param unknown_profile: an instance of LanguageDetector
        :param k: a number of the most common n-grams
        :param trie_levels: N-gram size
        :return: sorted language labels with corresponding ngram size and their prob scores if input is correct,
         otherwise -1
        """

        if not isinstance(unknown_profile, LanguageProfile) or not isinstance(k, int)\
                or not isinstance(trie_levels, tuple):
            return -1

        result_dict = {}

        for language in self.language_profiles:
            for trie_level in trie_levels:
                result_dict[(language, trie_level)] = calculate_probability(unknown_profile,
                                                                            self.language_profiles[language],
                                                                            k,
                                                                            trie_level)

        return result_dict
