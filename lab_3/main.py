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
    sentences = re.split(r'[.!?]\s', text)
    umlauts = {'ö': 'oe', 'ü': 'ue', 'ä': 'ae', 'ß': 'ss'}
    symbols = """'!@#$%^&*()-_=+/|"№;%:?><,.`~’…—[]{}1234567890"""
    for index, sentence in enumerate(sentences):
        new_sentence = sentence.lower()
        for character in sentence:
            if character in umlauts:
                new_sentence = new_sentence.replace(character, umlauts.get(character))
            if character in symbols:
                new_sentence = new_sentence.replace(character, '')
        new_sentence = new_sentence.split()
        if not new_sentence:
            return ()
        for word_index, word in enumerate(new_sentence):
            new_word = '_' + word + '_'
            new_sentence[word_index] = tuple(new_word)
        sentences[index] = tuple(new_sentence)
    return tuple(sentences)


# 4
class LetterStorage:
    """
    Stores and manages letters
    """

    def __init__(self):
        self.storage = {}
        self.letter_id = 1

    def _put_letter(self, letter: str) -> int:
        """
        Puts a letter into storage, assigns a unique id
        :param letter: a letter
        :return: 0 if succeeds, 1 if not
        """
        if not letter or not isinstance(letter, str):
            return -1
        if letter not in self.storage:
            self.storage[letter] = self.letter_id
            self.letter_id += 1
        return 0

    def get_id_by_letter(self, letter: str) -> int:
        """
        Gets a unique id by a letter
        :param letter: a letter
        :return: an id
        """
        if letter not in self.storage:
            return -1
        return self.storage.get(letter)

    def get_letter_by_id(self, letter_id: int) -> str or int:
        """
        Gets a letter by a unique id
        :param letter_id: a unique id
        :return: letter
        """
        if letter_id not in self.storage.values():
            return -1
        return [key for key, value in self.storage.items() if letter_id == value][0]

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
    corpus_id = []
    for sentence in corpus:
        sentence_id = []
        for word in sentence:
            word_id = []
            for letter in word:
                if letter in storage.storage:
                    word_id.append(storage.get_id_by_letter(letter))
            sentence_id.append(tuple(word_id))
        corpus_id.append(tuple(sentence_id))
    return tuple(corpus_id)


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
    storage.update(corpus)
    text_corpus = []
    for sentence_id in corpus:
        sentence = []
        for word_id in sentence_id:
            word = []
            for letter_id in word_id:
                if letter_id in storage.storage.values():
                    word.append(storage.get_letter_by_id(letter_id))
            sentence.append(tuple(word))
        text_corpus.append(tuple(sentence))
    return tuple(text_corpus)


# 6
class NGramTrie:
    """
    Stores and manages ngrams
    """

    def __init__(self, n: int, letter_storage: LetterStorage):
        self.size = n
        self.storage = letter_storage.storage
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
        n_gram_corpus = []
        for encoded_sentence in encoded_corpus:
            n_gram_sentence = []
            for encoded_word in encoded_sentence:
                n_gram_word = []
                for id_index, letter_id in enumerate(encoded_word):
                    if id_index + self.size <= len(encoded_word):
                        n_gram_word.append(tuple(encoded_word[id_index:id_index + self.size]))
                if n_gram_word:
                    n_gram_sentence.append(tuple(n_gram_word))
            n_gram_corpus.append(tuple(n_gram_sentence))
        self.n_grams = tuple(n_gram_corpus)
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
        if not isinstance(n_grams_dictionary, dict):
            return 1
        for n_gram, frequency in n_grams_dictionary.items():
            if isinstance(n_gram, tuple) and isinstance(frequency, int):
                for letter_id in n_gram:
                    if isinstance(letter_id, int):
                        self.n_gram_frequencies[n_gram] = frequency
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
        :param encoded_corpus: a tuple of encoded letters
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
        for n_gram_size in ngram_sizes:
            n_gram = NGramTrie(n_gram_size, self.storage)
            n_gram.extract_n_grams(encoded_corpus)
            self.tries.append(n_gram)
            n_gram.get_n_grams_frequencies()
        for n_gram_trie in self.tries:
            n_gram_frequency = 0
            for unique_n_gram in n_gram_trie.n_gram_frequencies:
                n_gram_frequency += 1
            self.n_words.append(n_gram_frequency)
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
        if (not isinstance(k, int) or k < 0) or not isinstance(trie_level, int):
            return ()
        top_n_grams = []
        for trie in self.tries:
            if trie.size == trie_level:
                trie.get_n_grams_frequencies()
                sorted_n_grams = sorted(trie.n_gram_frequencies,
                                        key=trie.n_gram_frequencies.get,
                                        reverse=True)
                top_n_grams.extend(sorted_n_grams[:k])
        return tuple(top_n_grams)

    # 8
    def save(self, name: str) -> int:
        """
        Saves language profile into json file
        :param name: name of the json file with .json format
        :return: 0 if profile saves, 1 if any errors occurred
        """
        if not isinstance(name, str):
            return 1
        language_profile = {}
        freq_dict = {}
        for trie in self.tries:
            for n_gram, freq in trie.n_gram_frequencies.items():
                decoded_n_gram = ''.join([self.storage.get_letter_by_id(letter_id)
                                          for letter_id in n_gram])
                freq_dict[decoded_n_gram] = freq
        language_profile['freq'] = freq_dict
        language_profile['n_words'] = self.n_words
        language_profile['name'] = self.language
        with open(name, 'w', encoding='utf-8') as file_to_save:
            json_string = json.dumps(language_profile)
            file_to_save.write(json_string)
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
        n_grams = []
        # 1
        with open(file_name, 'r', encoding='utf-8') as lang_profile_file:
            profile_dict = json.load(lang_profile_file)
            self.language = profile_dict['name']
            self.n_words = profile_dict['n_words']
            # 2
            sep_index = 0
            for n_gram_index, n_gram in enumerate(profile_dict['freq']):
                if n_gram_index < len(list(profile_dict['freq'])) - 1:
                    if len(n_gram) != len(list(profile_dict['freq'])[n_gram_index + 1]):
                        n_grams.append(list(profile_dict['freq'])[sep_index:n_gram_index])
                        sep_index = n_gram_index
            n_grams.append(list(profile_dict['freq'])[sep_index:n_gram_index])
            n_grams_tuple = tuple(tuple(tuple(n_grams)))
            # 3
            self.storage.update(n_grams_tuple)
            # 4
            n_grams_dict = {}
            for n_gram, freq in profile_dict['freq'].items():
                encoded_n_gram = []
                for letter in n_gram:
                    encoded_n_gram.append(self.storage.get_id_by_letter(letter))
                if len(tuple(encoded_n_gram)) not in n_grams_dict:
                    n_grams_dict[len(tuple(encoded_n_gram))] = {tuple(encoded_n_gram): freq}
                else:
                    n_grams_dict[len(tuple(encoded_n_gram))] |= {tuple(encoded_n_gram): freq}
            # 5
            for group, frequency in n_grams_dict.items():
                trie = NGramTrie(group, self.storage)
                trie.extract_n_grams_frequencies(frequency)
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
    Например, первый набор N-грамм для неизвестного профиля - first_n_grams = ((1, 2),
                                                                               (4, 5),
                                                                               (2, 3)),
    второй набор N-грамм для известного профиля – second_n_grams = ((1, 2), (2, 3), (4, 5)).
    Расстояние для (1, 2) равно 0, так как индекс в первом наборе – 0, во втором – 0, |0 – 0| = 0.
    Расстояние для (4, 5) равно 1, расстояние для (2, 3) равно 1.
    Соответственно расстояние между наборами равно 2.
    """
    if not isinstance(unknown_profile, LanguageProfile) or not \
        isinstance(known_profile, LanguageProfile) or (not isinstance(k, int) or k < 0) \
            or not isinstance(trie_level, int):
        return -1
    unknown_n_grams = unknown_profile.get_top_k_n_grams(k, trie_level)
    known_n_grams = known_profile.get_top_k_n_grams(k, trie_level)
    distance = 0
    for unknown_n_gram_index, unknown_n_gram in enumerate(unknown_n_grams):
        if unknown_n_gram in known_n_grams:
            distance += abs(unknown_n_gram_index - known_n_grams.index(unknown_n_gram))
        else:
            distance += len(known_n_grams)
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
        if language_profile not in self.language_profiles:
            self.language_profiles[language_profile.language] = language_profile
        return 0

    def detect(self, unknown_profile: LanguageProfile, k: int, trie_levels: Tuple[int]) -> \
            Dict[str, int] or int:
        """
        Detects the language of an unknown profile and its score
        :param unknown_profile: a dictionary
        :param k: a number of the most common n-grams
        :param trie_levels: N-gram size - tuple with one int for score 8
        :return: a dictionary with language labels and their scores if input is correct,
                                                                            otherwise -1
        """
        if not isinstance(unknown_profile, LanguageProfile) or not isinstance(k, int) \
                or not isinstance(trie_levels, tuple):
            return -1
        freq_dict = {}
        for language, trie in self.language_profiles.items():
            for trie_level in trie_levels:
                distance = calculate_distance(unknown_profile, trie, k, trie_level)
            freq_dict[language] = distance
        return freq_dict


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
        pass
