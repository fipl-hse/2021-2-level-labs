"""
Lab 3
Language classification using n-grams
"""

from typing import Dict, Tuple
import re


# 4
def tokenize_by_sentence(text: str):
    if not isinstance(text, str):
        return ()
    useless_symbols = ['`', '~', '@', '*', '#', '$', '%', '^', '&', '(', ')', '_', '-', '+',
                       '=', '{', '[', ']', '}', '|', '\\', ':', ';', '"', "'", '<', ',', '>',
                       '/', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
    patterns = ('ö', 'ü', 'ä', 'ß')
    replacements = ('oe', 'ue', 'ae', 'ss')
    if text:
        last_letter = text[-1]
        if last_letter == '.' or last_letter == '!' or last_letter == '?':
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
    def __init__(self):
        self.storage = {}
        self.count = 0

    def _put_letter(self, letter: str) -> int:
        if not isinstance(letter, str):
            return -1
        if letter not in self.storage:
            self.count += 1
            self.storage[letter] = self.count
        return 0

    def get_id_by_letter(self, letter: str) -> int:
        if not isinstance(letter, str):
            return -1
        if letter not in self.storage.keys():
            return -1
        letter_id = self.storage[letter]
        return letter_id

    def get_letter_by_id(self, letter_id: int) -> str or int:
        if not isinstance(letter_id, int):
            return -1
        if letter_id not in self.storage.values():
            return -1
        for letter, id_letter in self.storage.items():
            if id_letter == letter_id:
                return letter

    def update(self, corpus: tuple) -> int:
        if not isinstance(corpus, tuple):
            return -1
        for sentence in corpus:
            for token in sentence:
                for letter in token:
                    self._put_letter(letter)
        return 0


# 4
def encode_corpus(storage: LetterStorage, corpus: tuple) -> tuple:
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
    def __init__(self, n: int, letter_storage: LetterStorage):
        self.size = n
        self.storage = letter_storage
        self.n_grams = []
        self.n_gram_frequencies = {}

    def extract_n_grams(self, encoded_corpus: tuple) -> int:
        if not isinstance(encoded_corpus, tuple):
            return 1
        ngrams = []
        for encoded_sentence in encoded_corpus:
            ngram_sentence = []
            for encoded_word in encoded_sentence:
                ngram_word = []
                for i in range(len(encoded_word) - self.size + 1):
                    ngram_word.append(tuple(encoded_word[i:i + self.size]))
                ngram_sentence.append(tuple(ngram_word))
            ngrams.append(tuple(ngram_sentence))
        self.n_grams = tuple(ngrams)
        return 0

    def get_n_grams_frequencies(self) -> int:
        if not self.n_grams:
            return 1
        for ngram_sentence in self.n_grams:
            for ngram_word in ngram_sentence:
                for n_gram in ngram_word:
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
    def __init__(self, letter_storage: LetterStorage, language_name: str):
        self.storage = letter_storage
        self.language = language_name
        self.tries = []
        self.n_words = []

    def create_from_tokens(self, encoded_corpus: tuple, ngram_sizes: tuple) -> int:
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
        if not isinstance(k, int) or not isinstance(trie_level, int):
            return ()
        if k < 1 or trie_level < 1:
            return ()
        for trie in self.tries:
            if trie.size == trie_level:
                sorted_n_grams_frequencies = sorted(trie.n_gram_frequencies.items(), key=lambda x: -x[1])
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
    if not isinstance(unknown_profile, LanguageProfile) or not isinstance(known_profile, LanguageProfile) \
            or not isinstance(k, int) or not isinstance(trie_level, int):
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
