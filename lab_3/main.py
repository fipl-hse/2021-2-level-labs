"""
Lab 3
Language classification using n-grams
"""

from typing import Dict, Tuple
import re
import json


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

    # split text by sentence
    text = text.lower()
    text = re.split(r'[.!?] |\n', text)

    # tokenization of sentence
    deutsch_letters = {'ö': 'oe', 'ü': 'ue', 'ä': 'ae', 'ß': 'ss'}
    clean_text = []
    clean_sentence = ''
    for sentence in text:
        for symbol in sentence:
            if symbol in deutsch_letters:  # replace umlauts and ß
                clean_sentence += deutsch_letters[symbol]
            elif symbol.isalpha() or symbol.isspace():
                clean_sentence += symbol
        clean_text.append(clean_sentence.split())
        clean_sentence = ''

    # split words by letters
    ready_text = []
    for sentence in clean_text:
        split_tokens = []  # list for sentence
        for word in sentence:
            token = []  # list for word
            token += '_'
            for letter in word:
                token += letter
            token += '_'
            split_tokens.append(tuple(token))
        if split_tokens:  # check for not creating tuple with empty tuples
            ready_text.append(tuple(split_tokens))

    return tuple(ready_text)


# 4
class LetterStorage:
    """
    Stores and manages letters
    """

    def __init__(self):
        self.counter = 1
        self.storage = {}

    def _put_letter(self, letter: str) -> int:
        """
        Puts a letter into storage, assigns a unique id
        :param letter: a letter
        :return: 0 if succeeds, 1 if not
        """
        if not isinstance(letter, str) or not letter:
            return -1
        if letter not in self.storage:
            self.storage[letter] = self.counter
            self.counter += 1
        return 0

    def get_id_by_letter(self, letter: str) -> int:
        """
        Gets a unique id by a letter
        :param letter: a letter
        :return: an id
        """
        if not isinstance(letter, str) or letter not in self.storage:
            return -1
        return self.storage[letter]

    def get_letter_by_id(self, letter_id: int) ->str or int:
        """
        Gets a letter by a unique id
        :param letter_id: a unique id
        :return: letter
        """
        inverted_storage = {value: key for key, value in self.storage.items()}
        if not isinstance(letter_id, int) or letter_id not in inverted_storage:
            return -1
        return inverted_storage[letter_id]

    def update(self, corpus: tuple) -> int:
        """
        Fills a storage by letters from the corpus
        :param corpus: a tuple of sentences
        :return: 0 if succeeds, 1 if not
        """
        if not isinstance(corpus, tuple):
            return -1
        for text in corpus:
            for sentence in text:
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
    encoded_text = tuple(tuple(tuple(storage.get_id_by_letter(letter)
                                     for letter in word)
                               for word in sentence)
                         for sentence in corpus)
    return encoded_text


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

    decoded_text = tuple(tuple(tuple(storage.get_letter_by_id(letter_id)
                                     for letter_id in enc_word)
                               for enc_word in enc_sentence)
                         for enc_sentence in corpus)
    return decoded_text


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
        if not isinstance(encoded_corpus, tuple):
            return 1

        n_grams = []
        counter = 0

        for enc_sentence in encoded_corpus:
            n_grams_sentence = []
            for word in enc_sentence:
                n_grams_word = []
                while counter < len(word)-self.size+1:
                    n_grams_word.append(tuple(word[counter:counter+self.size]))
                    counter += 1
                counter = 0
                if n_grams_word:  # check for not adding an empty tuple
                    n_grams_sentence.append(tuple(n_grams_word))
            n_grams.append(tuple(n_grams_sentence))

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
        if not self.n_grams:
            return 1

        for enc_sentence in self.n_grams:
            for enc_word in enc_sentence:
                for n_gram in enc_word:
                    if n_gram in self.n_gram_frequencies:
                        self.n_gram_frequencies[n_gram] += 1
                    else:
                        self.n_gram_frequencies[n_gram] = 1
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
            else:
                return 1
        return 0

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

        for size in ngram_sizes:
            trie = NGramTrie(size, self.storage)
            trie.extract_n_grams(encoded_corpus)
            trie.get_n_grams_frequencies()
            self.tries.append(trie)  # adding n_grams
            self.n_words.append(len(trie.n_gram_frequencies))  # counting n_grams
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
        if not isinstance(k, int) or not isinstance(trie_level, int) or k <= 0 or trie_level <= 1:
            return ()

        for trie in self.tries:
            if trie.size == trie_level:
                top_k_n_grams = tuple(sorted(trie.n_gram_frequencies,
                                             key=trie.n_gram_frequencies.get, reverse=True)[:k])
                return top_k_n_grams

    # 8
    def save(self, name: str) -> int:
        """
        Saves language profile into json file
        :param name: name of the json file with .json format
        :return: 0 if profile saves, 1 if any errors occurred
        """
        if not isinstance(name, str):
            return 1

        freq = {}
        for trie in self.tries:
            for n_gram in trie.n_gram_frequencies.keys():
                freq[''.join(map(self.storage.get_letter_by_id,
                                 n_gram))] = trie.n_gram_frequencies[n_gram]
        profile = {'freq': freq, 'n_words': self.n_words, 'name': self.language}

        with open(name, 'w') as file:
            json_string = json.dumps(profile)
            file.write(json_string)
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

        with open(file_name, 'r') as lang_profile_file:
            profile_dict = json.load(lang_profile_file)

        self.language = profile_dict['name']
        self.n_words = profile_dict['n_words']

        for letter in ''.join(profile_dict['freq'].keys()):
            self.storage._put_letter(letter)

        n_grams = []
        frequencies = tuple(profile_dict['freq'].values())
        for n_gram in profile_dict['freq'].keys():
            n_grams.append(tuple(map(self.storage.get_id_by_letter, list(n_gram))))

        for i, number in enumerate(self.n_words):
            new_freq = dict(zip(tuple(n_grams[:number]), frequencies[:number]))
            n_grams = n_grams[number:]
            frequencies = frequencies[number:]

            trie = NGramTrie(i+1, self.storage)
            trie.extract_n_grams_frequencies(new_freq)
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
    Например, первый набор N-грамм для неизвестного профиля - first_n_grams = ((1, 2), (4, 5), (2, 3)),
    второй набор N-грамм для известного профиля – second_n_grams = ((1, 2), (2, 3), (4, 5)).
    Расстояние для (1, 2) равно 0, так как индекс в первом наборе – 0, во втором – 0, |0 – 0| = 0.
    Расстояние для (4, 5) равно 1, расстояние для (2, 3) равно 1.
    Соответственно расстояние между наборами равно 2.
    """
    if not isinstance(k, int) or not isinstance(trie_level, int) \
            or not isinstance(unknown_profile, LanguageProfile) \
            or not isinstance(known_profile, LanguageProfile):
        return -1

    top_k_unknown = unknown_profile.get_top_k_n_grams(k, trie_level)
    top_k_known = known_profile.get_top_k_n_grams(k, trie_level)
    distance = 0

    for n_gram in top_k_unknown:
        if n_gram in top_k_known:
            distance += abs(top_k_unknown.index(n_gram) - top_k_known.index(n_gram))
        else:
            distance += len(top_k_known)
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
        if not isinstance(k, int) or not isinstance(trie_levels, tuple) \
                or not isinstance(unknown_profile, LanguageProfile)\
                or not isinstance(trie_levels[0], int):
            return -1

        distance_dict = {}
        for known_profile in self.language_profiles.values():
            distance_dict[known_profile.language] = \
                calculate_distance(unknown_profile, known_profile, k, trie_levels[0])
        return distance_dict


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

    def detect(self, unknown_profile: LanguageProfile, k: int, trie_levels: tuple) -> Dict[Tuple[str, int], int or float] or int:
        """
        Detects the language of an unknown profile and its probability score
        :param unknown_profile: an instance of LanguageDetector
        :param k: a number of the most common n-grams
        :param trie_levels: N-gram size
        :return: sorted language labels with corresponding ngram size and their prob scores if input is correct, otherwise -1
        """
        pass
