"""
Lab 3
Language classification using n-grams
"""
import json
from typing import Dict, Tuple


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
    text = text.lower()

    symbols = ['`', '~', '@', '*', '#', '$', '%', '^', '&', '(', ')', '_', '-', '+',
               '=', '{', '[', ']', '}', '|', '\\', ':', ';', '"', "'", '<', ',', '>',
               '/', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']

    if text:
        last_letter = text[-1]
        if last_letter in ('.', '!', '?'):
            text = text[:-1]
    else:
        return ()
    for symbol in symbols:
        text = text.replace(symbol, '')
    # if not text:
    #     return ()
    text = text.replace('!', '*end*')
    text = text.replace('?', '*end*')
    text = text.replace('.', '*end*')
    sentences = text.split('*end*')
    new_sentences = []
    for sentence in sentences:
        new_tokens = []

        tokens = sentence.split()
        for token in tokens:
            letters = []
            letters.insert(0, '_')
            for letter in token:
                letters.append(letter)
            letters.append('_')
            new_tokens.append(tuple(letters))
        new_sentences.append(tuple(new_tokens))
    new_sentences = tuple(new_sentences)
    return new_sentences


# 4
class LetterStorage:
    """
    Stores and manages letters
    """

    def __init__(self):
        self.storage = {}
        self.count = 0

    def put_letter(self, letter):
        """
        Puts a letter into storage, assigns a unique id
        :param letter: a letter
        :return: 0 if succeeds, 1 if not
        """
        if not isinstance(letter, str):
            return -1
        if letter not in self.storage:
            self.count += 1
            self.storage[letter] = self.count

        return 0

    def _put_letter(self, letter: str) -> int:
        """
        Puts a letter into storage, assigns a unique id
        :param letter: a letter
        :return: 0 if succeeds, 1 if not
        """

        if not isinstance(letter, str):
            return -1
        if letter not in self.storage:
            self.count += 1
            self.storage[letter] = self.count

        return 0

    def get_id_by_letter(self, letter: str) -> int:
        """
        Gets a unique id by a letter
        :param letter: a letter
        :return: an id
        """
        if not isinstance(letter, str):
            return -1
        if letter not in self.storage.keys():
            return -1
        letter_id = self.storage[letter]
        return letter_id

    def get_letter_by_id(self, letter_id: int) -> str or int:
        """
        Gets a letter by a unique id
        :param letter_id: a unique id
        :return: letter
        """
        if not isinstance(letter_id, int):
            return -1
        if letter_id not in self.storage.values():
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
    if not isinstance(corpus, tuple) \
            or not isinstance(storage, LetterStorage):
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
    if not isinstance(corpus, tuple) \
            or not isinstance(storage, LetterStorage):
        return ()
    storage.update(corpus)
    encoded_corpus = []
    for sentence in corpus:
        encoded_sentences = []
        for token in sentence:
            encoded_tokens = []
            for letter in token:
                encoded_tokens.append(storage.get_letter_by_id(letter))
            encoded_sentences.append(tuple(encoded_tokens))
        encoded_corpus.append(tuple(encoded_sentences))
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
        bigramms_corpus = []

        for sentence in encoded_corpus:
            bigramms_sentence = []
            for token in sentence:
                bigramms_token = []
                first_index = 0

                last_index = first_index + self.size
                while last_index <= len(token):
                    bigramm = token[first_index:last_index]
                    first_index += 1
                    last_index += 1
                    bigramms_token.append(tuple(bigramm))
                bigramms_sentence.append(tuple(bigramms_token))
            bigramms_corpus.append(tuple(bigramms_sentence))
        self.n_grams = tuple(bigramms_corpus)
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
        for bigramms_sentence in self.n_grams:
            for bigramms_token in bigramms_sentence:
                for bigramm in bigramms_token:
                    if bigramm not in self.n_gram_frequencies:
                        self.n_gram_frequencies[bigramm] = 1
                    else:
                        self.n_gram_frequencies[bigramm] += 1
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
        # self.tries = NGramTrie.n_grams
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

        self.tries -->
        [<__main__.NGramTrie object at 0x09DB9BB0>, <__main__.NGramTrie object at 0x09DB9A48>]
        self.n_words --> [11, 9]
        self.tries[0].n_grams --> (
            (((1, 2), (2, 3), (3, 1)), ((1, 4), (4, 5), (5, 1)),
            ((1, 2), (2, 6), (6, 7), (7, 7), (7, 8), (8, 1))),
        )
        """
        if not isinstance(encoded_corpus, tuple) or not isinstance(ngram_sizes, tuple):
            return 1
        for size in ngram_sizes:
            self.tries.append(NGramTrie(size, self.storage))
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
        if trie_level < 1 or k < 1:
            return ()
        for trie in self.tries:
            if trie.size == trie_level:
                dict_n_grams = sorted(trie.n_gram_frequencies.items(), key=lambda x: -x[1])
                top_common_n_grams = []
                for element in dict_n_grams:
                    top_common_n_grams.append(element[0])
                top_common_n_grams = tuple(top_common_n_grams[:k])
                return top_common_n_grams

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
        freq = {}
        profile = {}
        with open(name, 'w', encoding="utf-8") as file:
            profile['name'] = self.language
            profile['n_words'] = self.n_words
            for trie in self.tries:

                for n_gram in trie.n_gram_frequencies:
                    new_n_gram = ''
                    for letter_id in n_gram:
                        new_n_gram += self.storage.get_letter_by_id(letter_id)
                    freq[new_n_gram] = trie.n_gram_frequencies[n_gram]
            profile['freq'] = freq
            file.write(json.dumps(profile))
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
        with open(file_name, 'r', encoding="utf-8") as file:
            profile = json.load(file)
            self.n_words = profile['n_words']
            self.language = profile['name']
            self.tries = []
            decoded_n_grams = []
            for n_gram in profile['freq']:
                new_n_gram = []
                for letter in n_gram:
                    self.storage.put_letter(letter)
                    new_n_gram.append(self.storage.get_id_by_letter(letter))
                decoded_n_grams.append((tuple(new_n_gram), profile['freq'][n_gram]))
            sizes = {}

            for n_gram in decoded_n_grams:
                size = len(n_gram[0])
                if size not in sizes:
                    sizes[size] = {n_gram[0]: n_gram[1]}
                else:
                    sizes[size][n_gram[0]] = n_gram[1]
            for size, freq_dict in sizes.items():
                tries = NGramTrie(size, self.storage)
                tries.n_gram_frequencies = freq_dict
                self.tries.append(tries)
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
    Например, первый набор N-грамм для неизвестного
    профиля - first_n_grams = ((1, 2), (4, 5), (2, 3)),
    второй набор N-грамм для известного профиля – second_n_grams = ((1, 2), (2, 3), (4, 5)).
    Расстояние для (1, 2) равно 0, так как индекс в первом наборе – 0, во втором – 0, |0 – 0| = 0.
    Расстояние для (4, 5) равно 1, расстояние для (2, 3) равно 1.
    Соответственно расстояние между наборами равно 2.
    """
    if not isinstance(unknwon_profile, LanguageProfile) \
            or not isinstance(known_profile, LanguageProfile) \
            or not isinstance(k, int) or not isinstance(trie_level, int):
        return -1
    unknown_top_k_n_grams = unknwon_profile.get_top_k_n_grams(k, trie_level)
    known_top_k_n_grams = known_profile.get_top_k_n_grams(k, trie_level)
    distance = 0
    for index, value in enumerate(unknown_top_k_n_grams):
        if value in known_top_k_n_grams:
            distance += abs(index - known_top_k_n_grams.index(value))
        else:
            distance += len(known_top_k_n_grams)
    return distance


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

    def detect(self, unknown_profile: LanguageProfile, k: int, trie_levels: Tuple[int]) \
            -> Dict[str, int] or int:
        """
        Detects the language of an unknown profile and its score
        :param unknown_profile: a dictionary
        :param k: a number of the most common n-grams
        :param trie_levels: N-gram size - tuple with one int for score 8
        :return: a dictionary with language labels
        and their scores if input is correct, otherwise -1
        """
        if not isinstance(unknown_profile, LanguageProfile) \
                or not isinstance(k, int) or not isinstance(trie_levels, tuple):
            return -1
        detection = {}
        for language, profile in self.language_profiles.items():
            detection[language] = calculate_distance(unknown_profile, profile, k, trie_levels[0])
            # print(detection)
        return detection


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
        :return: sorted language labels with corresponding
        ngram size and their prob scores if input is correct, otherwise -1
        """
        pass
