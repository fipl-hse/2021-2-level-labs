"""
Lab 3
Language classification using n-grams
"""

from typing import Dict, Tuple
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
    # if isinstance(text,str) is False:
    # return None
    if not isinstance(text, str):
        return ()
    stop_symbols = "1234567890@#$%^&*()_-+=~`\"':;\\|/,><{}[]"
    list_text = []
    tupled_text = []
    text = text.replace('ö','oe')
    text = text.replace('ü','ue')
    text = text.replace('ä','ae')
    text = text.replace('ß','ss')
    for stop_symbol in stop_symbols:
        text = text.replace(stop_symbol, '')
    for symbol in text:
        list_text.append(symbol)
    for index, symbol in enumerate(list_text):
        if symbol == '\n':
            list_text[index] = '!!!'
        if symbol in "!?.":
            if not (index == len(list_text) - 1 or (list_text[index + 1] == ' ' and
                                                     list_text[index + 2].isupper() is True)):
                list_text[index] = ''
            else:
                list_text[index] = '!!!'

    cleared_text = ''.join(list_text)
    cleared_text = cleared_text.lower()
    cleared_text = cleared_text.split('!!!')
    if not  cleared_text[-1]:
        cleared_text.pop(-1)
    for sentence in cleared_text:
        list_sentence = sentence.split()
        splitted_sentence = []
        for word in list_sentence:
            splitted_word = ['_']
            for letter in word:
                splitted_word.append(letter)
            splitted_word.append('_')
            splitted_sentence.append(tuple(splitted_word))
        tupled_text.append(tuple(splitted_sentence))
    return tuple(tupled_text)


# 4
class LetterStorage:
    """
    Stores and manages letters
    """

    def __init__(self):
        self.storage = {}
        self.l_id = 1

    def _put_letter(self, letter: str) -> int:
        """
        Puts a letter into storage, assigns a unique id
        :param letter: a letter
        :return: 0 if succeeds, 1 if not
        """
        if not isinstance(letter, str):
            return -1
        if letter.isalpha() is False and letter != '_':
            return -1
        if letter not in self.storage:
            self.storage[letter] = self.l_id
            self.l_id += 1
        return 0

    def get_id_by_letter(self, letter: str) -> int:
        """
        Gets a unique id by a letter
        :param letter: a letter
        :return: an id
        """
        if not isinstance(letter, str):
            return -1
        if letter not in self.storage:
            return -1
        return self.storage[letter]

    def get_letter_by_id(self, letter_id: int) -> str or int:
        """
        Gets a letter by a unique id
        :param letter_id: a unique id
        :return: letter
        """
        for letter, l_id in self.storage.items():
            if letter_id == l_id:
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
            for word in sentence:
                for letter in word:
                    result = self._put_letter(letter)
                    if result == -1:
                        return -1
        return 0

# 4
def encode_corpus(storage: LetterStorage, corpus: tuple) -> tuple:
    """
    Encodes sentences by replacing letters with their ids
    :param storage: an instance of the LetterStorage class
    :param corpus: a tuple of sentences
    :return: a tuple of the encoded sentences
    """
    if not (isinstance(storage, LetterStorage) and isinstance(corpus, tuple)):
        return()
    coded_corpus = []
    for sentence in corpus:
        if not isinstance(sentence, tuple):
            return ()
        coded_sentence = []
        for word in sentence:
            if not isinstance(word, tuple):
                return ()
            coded_word = []
            for letter in word:
                code_letter = storage.get_id_by_letter(letter)
                coded_word.append(code_letter)
            coded_sentence.append(tuple(coded_word))
        coded_corpus.append(tuple(coded_sentence))
    return tuple(coded_corpus)


# 4
def decode_corpus(storage: LetterStorage, corpus: tuple) -> tuple:
    """
    Decodes sentences by replacing letters with their ids
    :param storage: an instance of the LetterStorage class
    :param corpus: an encoded tuple of sentences
    :return: a tuple of the decoded sentences
    """
    if not (isinstance(corpus, tuple) and isinstance(storage, LetterStorage)):
        return ()
    decoded_corpus = []
    for sentence in corpus:
        if not isinstance(sentence, tuple):
            return ()
        decoded_sentence = []
        for word in sentence:
            if not isinstance(word, tuple):
                return ()
            decoded_word = []
            for letter in word:
                if not isinstance(letter, int):
                    return ()
                decoded_letter = storage.get_letter_by_id(letter)
                if decoded_letter == -1:
                    return ()
                decoded_word.append(decoded_letter)
            decoded_sentence.append(tuple(decoded_word))
        decoded_corpus.append(tuple(decoded_sentence))
    return tuple(decoded_corpus)


# 6
class NGramTrie:
    """
    Stores and manages ngrams
    """

    def __init__(self, n: int, letter_storage: LetterStorage):
        self.size = n
        self.storage = letter_storage
        self.n_grams = None
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

        ngrammed_text = []
        if not isinstance(encoded_corpus, tuple):
            return 1
        for sentence in encoded_corpus:
            if not isinstance(sentence, tuple):
                return 1
            ngrams_in_sentence = []
            for word in sentence:
                if not isinstance(word, tuple):
                    return 1
                ngram_word = []
                idk_but_helped = self.size
                ngrams_per_word = len(word) - self.size + 1
                while ngrams_per_word != 0:
                    n_gram = word[idk_but_helped - self.size:idk_but_helped]
                    ngram_word.append(tuple(n_gram))
                    idk_but_helped += 1
                    ngrams_per_word -= 1
                if ngram_word:
                    ngrams_in_sentence.append(tuple(ngram_word))
            if ngrams_in_sentence:
                ngrammed_text.append(tuple(ngrams_in_sentence))
            self.n_grams = tuple(ngrammed_text)
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
        if not isinstance(self.n_grams, tuple):
            return 1
        for n_sent in self.n_grams:
            if not isinstance(n_sent, tuple):
                return 1
            for n_word in n_sent:
                if not isinstance(n_word, tuple):
                    return 1
                for ngram in n_word:
                    if ngram not in self.n_gram_frequencies:
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
        for n_gramma, freq in n_grams_dictionary.items():
            if isinstance(n_gramma, tuple) and isinstance(freq, int):
                self.n_gram_frequencies[n_gramma] = freq
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

        self.tries --> [<__main__.NGramTrie object at 0x09DB9BB0>,
        <__main__.NGramTrie object at 0x09DB9A48>]
        self.n_words --> [11, 9]
        self.tries[0].n_grams --> (
            (((1, 2), (2, 3), (3, 1)), ((1, 4), (4, 5), (5, 1)),
            ((1, 2), (2, 6), (6, 7), (7, 7), (7, 8), (8, 1))),
        )
        """
        if not (isinstance(encoded_corpus, tuple) and isinstance(ngram_sizes, tuple)):
            return 1
        for n_n in ngram_sizes:
            trie = NGramTrie(n_n, self.storage)
            checker_1 = trie.extract_n_grams(encoded_corpus)
            checker_2 = trie.get_n_grams_frequencies()
            if checker_1 or checker_2:
                return 1
            self.tries.append(trie)
            summa = len(trie.n_gram_frequencies)
            self.n_words.append(summa)
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
        if not (isinstance(k, int) and isinstance(trie_level, int)):
            return ()
        if k < 1:
            return ()
        for trie in self.tries:
            if trie.size == trie_level:
                freq_dict = trie.n_gram_frequencies
                sorted_freq = sorted(freq_dict, key=freq_dict.get, reverse=True)[:k]
                return tuple(sorted_freq)
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
        decoded_freq_dict = {}
        for trie in self.tries:
            for key in trie.n_gram_frequencies():
                n_gramma = []
                for coded_letter in key:
                    letter = self.storage.get_letter_by_id(coded_letter)
                    n_gramma.append(letter)
                decoded_freq_dict[''.join(n_gramma)] = trie.n_gram_frequencies[key]

        profile_as_dict = {'freq': decoded_freq_dict, 'n_words': self.n_words,
                           'name': self.language}

        with open(name, 'w', encoding="utf-8") as file:
            json_string = json.dumps(profile_as_dict)
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
        with open(file_name, 'r',encoding="utf-8") as lang_profile_file:
            profile_dict = json.load(lang_profile_file)
            self.language = profile_dict['name']
            self.n_words = profile_dict['n_words']
            for n_gramma, freq in profile_dict['freq'].items():
                coded_ngramma = []
                exist_counter = 0
                for letter in n_gramma:
                    self.storage.update(tokenize_by_sentence(letter))
                    coded_ngramma.append(self.storage.get_id_by_letter(letter))
                coded_ngramma = tuple(coded_ngramma)
                n_2 = len(coded_ngramma)
                for trie in self.tries:
                    if n_2 == trie.size:
                        trie.n_gram_frequencies[coded_ngramma] = freq
                        exist_counter += 1
                if not exist_counter:
                    new_trie = NGramTrie(n_2, self.storage)
                    new_trie.n_gram_frequencies[coded_ngramma] = freq
                    self.tries.append(new_trie)
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
    второй набор N-грамм для известного профиля – second_n_grams =
    ((1, 2), (2, 3), (4, 5)).
    Расстояние для (1, 2) равно 0, так как индекс в первом наборе –
     0, во втором – 0, |0 – 0| = 0.
    Расстояние для (4, 5) равно 1, расстояние для (2, 3) равно 1.
    Соответственно расстояние между наборами равно 2.
    """
    if not (isinstance(unknown_profile, LanguageProfile) and
            isinstance(known_profile, LanguageProfile) and isinstance(k, int)
            and isinstance(trie_level, int)):
        return -1
    distance = 0
    unknown_top_ngram = unknown_profile.get_top_k_n_grams(k, trie_level)
    known_top_ngram = known_profile.get_top_k_n_grams(k, trie_level)
    known_ng_len = len(known_top_ngram)
    for n_g in unknown_top_ngram:
        if n_g in known_top_ngram:
            length = known_top_ngram.index(n_g) - unknown_top_ngram.index(n_g)
            if length < 0:
                length = length * (-1)
            distance += length
        else:
            distance += known_ng_len
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
        if not (isinstance(unknown_profile, LanguageProfile) and
                isinstance(k, int) and isinstance(trie_levels, tuple)):
            return -1
        if k < 1 or len(trie_levels) != 1 or not isinstance(trie_levels[0], int):
            return -1
        result_dictionary = {}
        for name, profile in self.language_profiles.items():
            distance = calculate_distance(unknown_profile, profile, k, trie_levels[0])
            result_dictionary[name] = distance
        return result_dictionary



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
               k: int, trie_levels: tuple) -> \
            Dict[Tuple[str, int], int or float] or int:
        """
        Detects the language of an unknown profile and its probability score
        :param unknown_profile: an instance of LanguageDetector
        :param k: a number of the most common n-grams
        :param trie_levels: N-gram size
        :return: sorted language labels with corresponding ngram
         size and their prob scores if input is correct, otherwise -1
        """
        pass
