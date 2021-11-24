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
    # lower the letters and split the text
    text = text.lower()
    text = re.split(r'[.!?]', text)
    # tokenize the sentence
    new_sentence = ''
    new_text = []
    german_letters = {'ß': 'ss', 'ö': 'oe', 'ü': 'ue', 'ä': 'ae'}
    for sentence in text:
        for letter in sentence:
            if letter in german_letters:
                new_sentence += german_letters.get(letter)
            elif letter.isalpha() or letter.isspace():
                new_sentence += letter
        new_text.append(new_sentence.split())
        new_sentence = ''

    tokens = ''
    new_tokens = []
    final_text = []
    for sentence in new_text:
        for word in sentence:
            tokens += '_'
            for letter in word:
                tokens += letter
            tokens += '_'
            new_tokens.append(tuple(tokens))
            tokens = ''
        if new_tokens:
            final_text.append(tuple(new_tokens))
        new_tokens = []
    return tuple(final_text)


# 4
class LetterStorage:
    """
    Stores and manages letters
    """

    def __init__(self):
        self.storage = {}
        self.counter = 1

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
        if not isinstance(letter, str) or not letter or letter not in self.storage:
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
        for letter, id_num in self.storage.items():
            if letter_id == id_num:
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
    encoded_text = ()
    for sentence in corpus:
        word_tuple = ()
        for word in sentence:
            letter_tuple = ()
            for letter in word:
                letter_tuple += (storage.get_id_by_letter(letter),)
            word_tuple += (letter_tuple,)
        encoded_text += (word_tuple,)
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
    decoded_text = ()
    for sentence in corpus:
        word_tuple = ()
        for word in sentence:
            letter_tuple = ()
            for letter_id in word:
                letter_tuple += (storage.get_letter_by_id(letter_id),)
            word_tuple += (letter_tuple,)
        decoded_text += (word_tuple,)
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
        n_grams_list = []
        for sentence in encoded_corpus:
            sentence_list = []
            for word in sentence:
                word_list = []
                for num in range(len(word) - self.size + 1):
                    word_list.append(tuple(word[num:num + self.size]))
                sentence_list.append(tuple(word_list))
            n_grams_list.append(tuple(sentence_list))
        self.n_grams = tuple(n_grams_list)
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
                for letter in word:
                    if letter in self.n_gram_frequencies:
                        self.n_gram_frequencies[letter] += 1
                    else:
                        self.n_gram_frequencies[letter] = 1
        return 0

    # 8
    def extract_n_grams_frequencies(self, n_grams_dictionary: dict) -> int:
        """
        Extracts n_grams frequencies from given dictionary.
        Fills self.n_gram_frequency field.
        """
        if not isinstance(n_grams_dictionary, dict):
            return 1
        for n_gram, freq in n_grams_dictionary.items():
            if not isinstance(n_gram, tuple):
                return 1
            self.n_gram_frequencies[n_gram] = freq
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

        self.tries --> [<__main__.NGramTrie object at 0x09DB9BB0>,
        <__main__.NGramTrie object at 0x09DB9A48>]
        self.n_words --> [11, 9]
        self.tries[0].n_grams --> (
            (((1, 2), (2, 3), (3, 1)), ((1, 4), (4, 5), (5, 1)), ((1, 2),
            (2, 6), (6, 7), (7, 7), (7, 8), (8, 1))),
        )
        """
        if not isinstance(encoded_corpus, tuple) \
                or not isinstance(ngram_sizes, tuple):
            return 1
        for size in ngram_sizes:
            n_gram_trie = NGramTrie(size, self.storage)
            n_gram_trie.extract_n_grams(encoded_corpus)
            n_gram_trie.get_n_grams_frequencies()
            self.tries.append(n_gram_trie)
            self.n_words.append(len(n_gram_trie.n_gram_frequencies))
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
        for n_gram_trie in self.tries:
            n_gram_trie.get_n_grams_frequencies()
            if n_gram_trie.size == trie_level:
                sorted_frequencies = sorted(n_gram_trie.n_gram_frequencies,
                                            key=n_gram_trie.n_gram_frequencies.get,
                                            reverse=True)[:k]
                return tuple(sorted_frequencies)
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
        freq = {}
        word = ''
        for trie in self.tries:
            for n_gram, frequency in trie.n_gram_frequencies.items():
                for element in n_gram:
                    word += self.storage.get_letter_by_id(element)
                freq[word] = frequency
                word = ''
        profile_as_dict['freq'] = freq
        profile_as_dict['n_words'] = self.n_words
        profile_as_dict['name'] = self.language
        with open(name, 'w', encoding='UTF-8') as file:
            json.dump(profile_as_dict, file)
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
        with open(file_name, 'r', encoding='UTF-8') as lang_profile_file:
            profile_dict = json.load(lang_profile_file)
        self.language = profile_dict['name']
        self.n_words = profile_dict['n_words']
        freq = profile_dict['freq']
        n_gram_size = 0
        counter = -1
        for n_gram, frequency in freq.items():
            n_grams_list = []
            for letter in n_gram:
                self.storage.update(tokenize_by_sentence(letter))
                n_grams_list.append(self.storage.get_id_by_letter(letter))
            if len(n_gram) != n_gram_size:
                n_gram_size = len(n_gram)
                counter += 1
                self.tries.append(NGramTrie(n_gram_size, self.storage))
                self.tries[counter].n_gram_frequencies[tuple(n_grams_list)] = frequency
            else:
                self.tries[counter].n_gram_frequencies[tuple(n_grams_list)] = frequency
        return 0


# 6

def calculate_distance(unknwon_profile: LanguageProfile, known_profile: LanguageProfile,
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
    if not isinstance(unknwon_profile, LanguageProfile) \
            or not isinstance(known_profile, LanguageProfile) \
            or not isinstance(k, int) or not isinstance(trie_level, int):
        return -1
    unknown_frequency = unknwon_profile.get_top_k_n_grams(k, trie_level)
    known_frequency = known_profile.get_top_k_n_grams(k, trie_level)
    distance = 0
    for n_gram in unknown_frequency:
        if n_gram in known_frequency:
            distance += abs(unknown_frequency.index(n_gram) - known_frequency.index(n_gram))
        else:
            distance += len(known_frequency)
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
        self.language_profiles[language_profile.language] \
            = language_profile
        return 0

    def detect(self, unknown_profile: LanguageProfile,
               k: int, trie_levels: Tuple[int]) -> Dict[str, int] or int:
        """
        Detects the language of an unknown profile and its score
        :param unknown_profile: a dictionary
        :param k: a number of the most common n-grams
        :param trie_levels: N-gram size - tuple with one int for score 8
        :return: a dictionary with language labels and
        their scores if input is correct, otherwise -1
        """
        if not isinstance(unknown_profile, LanguageProfile) or not isinstance(k, int) \
                or not isinstance(trie_levels, tuple) \
                or not isinstance(trie_levels[0], int):
            return -1
        distance_dictionary = {}
        for label, lang_profile in self.language_profiles.items():
            distance_dictionary[label] = \
                calculate_distance(unknown_profile, lang_profile, k, trie_levels[0])
        return distance_dictionary

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

    def detect(self, unknown_profile: LanguageProfile,
               k: int, trie_levels: tuple) -> Dict[Tuple[str, int], int or float] or int:
        """
        Detects the language of an unknown profile and its probability score
        :param unknown_profile: an instance of LanguageDetector
        :param k: a number of the most common n-grams
        :param trie_levels: N-gram size
        :return: sorted language labels with corresponding ngram
        size and their prob scores if input is correct, otherwise -1
        """
        pass
