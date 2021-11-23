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
    if not isinstance(text, str):
        return ()
    patterns = ('ö', 'ü', 'ä', 'ß')
    replacements = ('oe', 'ue', 'ae', 'ss')
    sentences = re.split(r"[.!?] ?", text)
    if '' in sentences:
        sentences.remove('')
    lst_of_sentences = [sentence.lower() for sentence in sentences]
    new_sentence_tuple = []
    for sentence in lst_of_sentences:
        sentence = sentence.split()
        new_words_lst = []
        for word in sentence:
            for pattern, replacement in zip(patterns, replacements):
                word.replace(pattern, replacement)
            lst_of_letters = [letter for letter in word if letter.isalpha()]
            if len(lst_of_letters):
                lst_of_letters.insert(0, '_')
                lst_of_letters.append('_')
                new_words_lst.append(tuple(lst_of_letters))
            if not len(new_words_lst):
                return ()
        new_sentence_tuple.append(tuple(new_words_lst))
    return tuple(new_sentence_tuple)


# 4
class LetterStorage:
    """
    Stores and manages letters
    """

    def __init__(self):
        self.storage = {}
        self.count = 1

    def _put_letter(self, letter: str) -> int:
        """
        Puts a letter into storage, assigns a unique id
        :param letter: a letter
        :return: 0 if succeeds, 1 if not
        """
        if not isinstance(letter, str):
            return -1
        if letter not in self.storage:
            self.storage[letter] = self.count
            self.count += 1
        return 0

    def get_id_by_letter(self, letter: str) -> int:
        """
        Gets a unique id by a letter
        :param letter: a letter
        :return: an id
        """
        if not isinstance(letter, str) or (letter not in self.storage.keys()):
            return -1
        return self.storage[letter]
        pass

    def get_letter_by_id(self, letter_id: int) ->str or int:
        """
        Gets a letter by a unique id
        :param letter_id: a unique id
        :return: letter
        """
        if not isinstance(letter_id, int) or (letter_id not in self.storage.values()):
            return -1
        for letter, new_letter_id in self.storage.items():
            if new_letter_id == letter_id:
                return letter
        pass

    def update(self, corpus: tuple) -> int:
        """
        Fills a storage by letters from the corpus
        :param corpus: a tuple of sentences
        :return: 0 if succeeds, 1 if not
        """
        if not isinstance(corpus, tuple):
            return -1
        for sentence in corpus:
            for word in sentence:
                for letter in word:
                    if self._put_letter(letter) == -1:
                        return -1
                    else:
                        self._put_letter(letter)
        return 0
        pass


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
    if not storage.update(corpus):
        encode = tuple(tuple(tuple(storage.get_id_by_letter(letter) for letter in word)
                             for word in sentence) for sentence in corpus)
        return encode
    pass


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
    decode = tuple(tuple(tuple(storage.get_letter_by_id(letter_id) for letter_id in word)
                                    for word in sentence) for sentence in corpus)
    return decode
    pass


# 6
class NGramTrie:
    """
    Stores and manages ngrams
    """
    def __init__(self, n: int, letter_storage: LetterStorage):
        self.storage = LetterStorage()
        self.size = n
        self.n_grams = []
        self.n_gram_frequencies = {}
        pass

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
        self.n_grams = tuple(tuple(tuple(tuple(word[i:i + self.size])
                                         for i in range(len(word) - (self.size - 1)))
                                   for word in sentence) for sentence in encoded_corpus)
        return 0
        pass

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
                for tpl in word:
                    if tpl not in self.n_gram_frequencies:
                        self.n_gram_frequencies[tpl] = 1
                    else:
                        self.n_gram_frequencies[tpl] += 1
        return 0

        pass

    # 8
    def extract_n_grams_frequencies(self, n_grams_dictionary: dict) -> int:
        """
        Extracts n_grams frequencies from given dictionary.
        Fills self.n_gram_frequency field.
        """
        if not isinstance(n_grams_dictionary, dict):
            return 1
        for key, value in n_grams_dictionary.items():
            if not isinstance(key, tuple) or not isinstance(value, int):
                return 1
            else:
                self.n_gram_frequencies[key] = value
        return 0
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
        self.language = language_name
        self.tries = []
        self.n_words = []
        pass

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
        if not isinstance(encoded_corpus, tuple) or not isinstance(ngram_sizes, tuple):
            return 1
        for trie_level in ngram_sizes:
            ngrams = NGramTrie(trie_level, self.storage)
            self.tries.append(ngrams)
            ngrams.extract_n_grams(encoded_corpus)
            ngrams.get_n_grams_frequencies()
            self.n_words.append(len(ngrams.n_gram_frequencies))
        return 0
        pass

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
        if not (isinstance(k, int) and isinstance(trie_level, int)):
            return ()
        if k < 1:
            return ()
        for trie in self.tries:
            if trie.size == trie_level:
                frequency = trie.n_gram_frequencies
                top_k_ngrams = tuple([key for key, value in
                                      sorted(frequency.items(), key=lambda i: -i[1])][:k])
                return top_k_ngrams
        return ()
        pass

    # 8
    def save(self, name: str) -> int:
        """
        Saves language profile into json file
        :param name: name of the json file with .json format
        :return: 0 if profile saves, 1 if any errors occurred
        """
        if not isinstance(name, str):
            return 1
        profile = {}
        freq_dict = {}
        new_key = ''
        with open(name, 'w') as file:
            for trie in self.tries:
                for key, value in trie.n_gram_frequencies.items():
                    for letter_id in key:
                        new_key += self.storage.get_letter_by_id(letter_id)
                    freq_dict[new_key] = value
                    new_key = ''
            profile['freq'] = freq_dict
            profile['n_words'] = self.n_words
            profile['name'] = self.language
            json_string = json.dumps(profile)
            file.write(json_string)
        return 0
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
        if not isinstance(file_name, str):
            return 1

        with open(file_name, 'r', encoding="UTF-8") as file:
            profile = json.load(file)
        self.language = profile["name"]
        self.n_words = profile["n_words"]
        decoded_ngrams = []
        first_length = 0
        list_with_length = []
        list_of_some_n_gram_frequencies = []
        n_gram_frequencies = {}
        for ngram in profile['freq']:
            encode = []
            for letter in ngram:
                self.storage._put_letter(letter)
                encode.append(self.storage.get_id_by_letter(letter))
            decoded_ngrams.append((tuple(encode), profile['freq'][ngram]))
        for ngram in decoded_ngrams:
            length = len(ngram[0])
            if first_length == 0:
                first_length = length
                list_with_length.append(first_length)
            elif first_length != length:
                first_length = length
                list_with_length[0] = first_length
                list_of_some_n_gram_frequencies.append(n_gram_frequencies)
                n_gram_frequencies = {}
            n_gram_frequencies[ngram[0]] = ngram[1]
        else:
            list_of_some_n_gram_frequencies.append(n_gram_frequencies)
        for n_gram_frequencies in list_of_some_n_gram_frequencies:
            trie = NGramTrie(list_with_length[0], self.storage)
            trie.n_gram_frequencies = n_gram_frequencies
            self.tries.append(trie)
        return 0
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
    Например, первый набор N-грамм для неизвестного профиля - first_n_grams =
    = ((1, 2), (4, 5), (2, 3)),
    второй набор N-грамм для известного профиля – second_n_grams =
    = ((1, 2), (2, 3), (4, 5)).
    Расстояние для (1, 2) равно 0, так как индекс в первом наборе – 0, во втором – 0, |0 – 0| = 0.
    Расстояние для (4, 5) равно 1, расстояние для (2, 3) равно 1.
    Соответственно расстояние между наборами равно 2.
    """
    if not isinstance(unknown_profile, LanguageProfile) or not isinstance(known_profile, LanguageProfile)\
            or not isinstance(k, int) or not isinstance(trie_level,int):
        return -1
    distance = 0
    frequency_unknown_profile = unknown_profile.get_top_k_n_grams(k, trie_level)
    frequency_known_profile = known_profile.get_top_k_n_grams(k, trie_level)
    for first_index, first_n_grams in enumerate(frequency_unknown_profile):
        for second_index, second_n_grams in enumerate(frequency_known_profile):
            if first_n_grams == second_n_grams:
                distance += abs(first_index - second_index)
        if first_n_grams not in frequency_known_profile:
            distance += len(frequency_known_profile)
    return distance
    pass


# 8
class LanguageDetector:
    """
    Detects profile language using distance
    """
    def __init__(self):
        self.language_profiles = {}
        pass

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
        pass

    def detect(self, unknown_profile: LanguageProfile, k: int,
               trie_levels: Tuple[int]) -> Dict[str, int] or int:
        """
        Detects the language of an unknown profile and its score
        :param unknown_profile: a dictionary
        :param k: a number of the most common n-grams
        :param trie_levels: N-gram size - tuple with one int for score 8
        :return: a dictionary with language labels and their scores if
        input is correct, otherwise -1
        """
        if not isinstance(unknown_profile, LanguageProfile) or \
                not isinstance(k, int) or not isinstance(trie_levels, tuple):
            return -1
        dict_with_language_and_distance = {}
        for language, language_profile in self.language_profiles.items():
            dict_with_language_and_distance[language] = \
                calculate_distance(unknown_profile, language_profile, k, trie_levels[0])
        return dict_with_language_and_distance
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
    def detect(self, unknown_profile: LanguageProfile, k: int, trie_levels: tuple) \
            -> Dict[Tuple[str, int], int or float] or int:
        """
        Detects the language of an unknown profile and its probability score
        :param unknown_profile: an instance of LanguageDetector
        :param k: a number of the most common n-grams
        :param trie_levels: N-gram size
        :return: sorted language labels with corresponding ngram size
        and their prob scores if input is correct, otherwise -1
        """
        pass
