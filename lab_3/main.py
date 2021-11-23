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
    for symbol in invaluable_trash:
        text = text.replace(symbol, '')
    for key, value in {'ö': 'oe', 'ü': 'ue', 'ä': 'ae', 'ß': 'ss'}.items():
        text = text.replace(key, value)
    sentence = ''
    all_sentences = []
    for number, symbol in enumerate(text):
        if symbol not in ['.', '?', '!', '…'] and number + 1 != len(text):
            sentence += symbol
        elif number + 1 == len(text) and symbol not in ['.', '?', '!', '…']:
            sentence += symbol
            all_sentences.append(sentence.lower())
        else:
            all_sentences.append(sentence.lower())
            sentence = ''
    for i, sentence in enumerate(all_sentences):
        all_sentences[i] = sentence.split()
    new_word = ['_']
    for sentence in all_sentences:
        for i, word in enumerate(sentence):
            new_word.extend(word)
            new_word.append('_')
            sentence[i] = new_word
            new_word = ['_']
    for i, sentence in enumerate(all_sentences):
        for j, word in enumerate(sentence):
            sentence[j] = tuple(word)
        all_sentences[i] = tuple(sentence)
    all_sentences = tuple(all_sentences)
    return all_sentences

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
        if not isinstance(letter, str) or not letter:
            return -1
        if letter not in self.storage:
            self.storage[letter] = self.id_number
            self.id_number += 1
        return 0

    def get_id_by_letter(self, letter: str) -> int:
        """
        Gets a unique id by a letter
        :param letter: a letter
        :return: an id
        """
        if letter not in self.storage:
            return -1
        return self.storage[letter]

    def get_letter_by_id(self, letter_id: int) ->str or int:
        """
        Gets a letter by a unique id
        :param letter_id: a unique id
        :return: letter
        """
        if letter_id not in self.storage.values():
            return -1
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
    encoded_corpus = tuple(
                     tuple(tuple(storage.get_id_by_letter(letter) for letter in word)
                           for word in sentence) for sentence in corpus)
    return encoded_corpus


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
    encoded_corpus = tuple(
                     tuple(tuple(storage.get_letter_by_id(number) for number in word)
                           for word in sentence) for sentence in corpus)
    return encoded_corpus


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
        word = []
        sentence = []
        all_sentences = []
        for sentence_tuple in encoded_corpus:
            for word_tuple in sentence_tuple:
                if len(word_tuple) >= self.size:
                    for i in range(len(word_tuple)-self.size+1):
                        word.append(tuple([word_tuple[i+j] for j in range(self.size)]))
                    sentence.append(tuple(word))
                    word = []
            all_sentences.append(tuple(sentence))
            sentence = []
        self.n_grams = tuple(all_sentences)
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
        if not isinstance(self.n_grams, tuple) or self.n_grams == ():
            return 1
        for sentence in self.n_grams:
            for word in sentence:
                for ngram in word:
                    if ngram not in self.n_gram_frequencies.keys():
                        self.n_gram_frequencies[ngram] = 1
                    else:
                        self.n_gram_frequencies[ngram] += 1
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
            if isinstance(key, tuple):
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
        for key, value in n_grams_dictionary.items():
            if isinstance(key, tuple) and isinstance(value, float):
                self.n_gram_log_probabilities[key] = value
        return 0
    # 10
    def calculate_log_probabilities(self) -> int:
        """
        Gets log-probabilities of n-grams, fills the field n_gram_log_probabilities
        :return: 0 if succeeds, 1 if not
        """
        if self.n_gram_frequencies == {}:
            return 1
        summa = 0
        for current_key, current_value in self.n_gram_frequencies.items():
            for key, value in self.n_gram_frequencies.items():
                if list(current_key)[:-1] == list(key)[:-1]:
                    summa += value
            self.n_gram_log_probabilities[current_key] = math.log(current_value/summa)
            summa = 0
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
        if not isinstance(encoded_corpus, tuple) or not isinstance(ngram_sizes, tuple):
            return 1

        for size in ngram_sizes:
            trie = NGramTrie(size, self.storage)
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
        if not isinstance(k, int) or not isinstance(trie_level, int) or k < 1 or trie_level < 1:
            return ()
        for trie in self.tries:
            if trie.size == trie_level:
                sorted_keys = tuple(sorted(trie.n_gram_frequencies,
                                 key=trie.n_gram_frequencies.get, reverse=True)[:k])
                return sorted_keys
        return ()

    # 8
    def save(self, name: str) -> int:
        """
        Saves language profile into json file
        :param name: name of the json file with .json format
        :return: 0 if profile saves, 1 if any errors occurred
        """
        if not isinstance(name, str):
            return 1
        profile_as_dict = {}
        freq_dict = {}
        new_key = ''
        for trie in self.tries:
            for key, value in trie.n_gram_frequencies.items():
                for element in key:
                    new_key += self.storage.get_letter_by_id(element)
                freq_dict[new_key] = value
                new_key = ''
        profile_as_dict["freq"] = freq_dict
        profile_as_dict['n_words'] = self.n_words
        profile_as_dict['name'] = self.language
        with open(name, 'w', encoding="utf-8") as lang_profile_file:
            json.dump(profile_as_dict, lang_profile_file)
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
        with open(file_name, 'r', encoding="utf-8") as lang_profile_file:
            profile_dict = json.load(lang_profile_file)
        self.language = profile_dict['name']
        self.n_words = profile_dict['n_words']
        for key in profile_dict['freq'].keys():
            for letter in key:
                if letter not in self.storage.storage:
                    self.storage._put_letter(letter)
        n_gram_dict = {}
        n_gram_tuple = ()
        for n_gram, frequency in profile_dict['freq'].items():
            if len(n_gram) not in n_gram_dict:
                n_gram_dict[len(n_gram)] = {}
            for letter in n_gram:
                    n_gram_tuple += (self.storage.get_id_by_letter(letter),)
            n_gram_dict[len(n_gram)][n_gram_tuple] = frequency
            n_gram_tuple = ()
        for number, freq_dict in n_gram_dict.items():
            trie = NGramTrie(number, self.storage)
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
    Например, первый набор N-грамм для неизвестного профиля -
    first_n_grams = ((1, 2), (4, 5), (2, 3)),
    второй набор N-грамм для известного профиля – second_n_grams = ((1, 2), (2, 3), (4, 5)).
    Расстояние для (1, 2) равно 0, так как индекс в первом наборе – 0, во втором – 0, |0 – 0| = 0.
    Расстояние для (4, 5) равно 1, расстояние для (2, 3) равно 1.
    Соответственно расстояние между наборами равно 2.
    """
    if not (isinstance(unknown_profile, LanguageProfile)
            and isinstance(known_profile, LanguageProfile)
            and isinstance(k, int)
            and isinstance(trie_level, int)):
        return -1
    frequency_unknown = unknown_profile.get_top_k_n_grams(k, trie_level)
    frequency_known = known_profile.get_top_k_n_grams(k, trie_level)
    distance = 0
    for ind, element in enumerate(frequency_unknown):
        if element in frequency_known:
            distance += abs(ind-frequency_known.index(element))
        else:
            distance += len(frequency_known)
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

    def detect(self, unknown_profile: LanguageProfile, k: int, trie_levels: Tuple[int])\
            -> Dict[str, int] or int:
        """
        Detects the language of an unknown profile and its score
        :param unknown_profile: a dictionary
        :param k: a number of the most common n-grams
        :param trie_levels: N-gram size - tuple with one int for score 8
        :return: a dictionary with language labels and their scores
        if input is correct, otherwise -1
        """
        if not (isinstance(unknown_profile, LanguageProfile)
                and isinstance(k, int)
                and isinstance(trie_levels, tuple)
                and isinstance(trie_levels[0], int)):
            return -1
        dictionary = {}
        for name, kn_profile in self.language_profiles.items():
            dictionary[name] = calculate_distance(unknown_profile, kn_profile, k, trie_levels[0])
        return dictionary


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
    if not (isinstance(unknown_profile, LanguageProfile)
            and isinstance(known_profile, LanguageProfile)
            and isinstance(k, int)
            and isinstance(trie_level, int)):
        return -1
    frequency_unknown = unknown_profile.get_top_k_n_grams(k, trie_level)
    for trie in known_profile.tries:
        if trie.size == trie_level:
            known_profile_n_grams = trie.n_gram_frequencies
    probability = 0
    for element in frequency_unknown:
        if element in known_profile_n_grams.keys():
            for trie in known_profile.tries:
                if trie.size == trie_level:
                    trie.calculate_log_probabilities()
                    probability += trie.n_gram_log_probabilities[element]
    return probability



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
        :return: sorted language labels with corresponding ngram size and their
        prob scores if input is correct, otherwise -1
        """
        if not (isinstance(unknown_profile, LanguageProfile)
                and isinstance(k, int)
                and isinstance(trie_levels, tuple)):
            return -1
        dictionary = {}
        for name, kn_profile in self.language_profiles.items():
            for level in trie_levels:
                dictionary[(name, level)] = calculate_probability(unknown_profile,
                                                                  kn_profile, k, level)
        return dictionary
