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
    invaluable_trash = ['`', '~', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-',
                        '+', '=', '{', '[', ']', '}', '|',
                        '\\', ':', ';', '"', "'", '<', ',', '>',
                        '/', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
    text = text.lower()
    special_letters = {'ü': 'ue', 'ö': 'oe', 'ä': 'ae', 'ß': 'ss'}
    for letter in text:
        for key, value in special_letters.items():
            if letter == key:
                text = text.replace(letter, value)
    for symbols in invaluable_trash:
        text = text.replace(symbols, '')
    regexp = re.compile('[.!?] ?')
    sents = re.split(regexp, text)
    cleaned_sents = []
    for sent in sents:
        cleaned_sent = sent.strip()
        if cleaned_sent:
            cleaned_sents.append([cleaned_sent])
    for ind, sent in enumerate(cleaned_sents):
        for words in sent:
            tokens = words.split()
            for i, token in enumerate(tokens):
                token = list(token)
                token.insert(0, '_')
                token.append('_')
                tokens[i] = tuple(token)
                cleaned_sents[ind] = tokens
    tuple_tokens = tuple((tuple(i) for i in cleaned_sents))
    return tuple_tokens



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
        if letter in self.storage:
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
        for key, value in self.storage.items():
            if value == letter_id:
                return key
        if letter_id not in self.storage.values():
            return -1


    def update(self, corpus: tuple) -> int:
        """
        Fills a storage by letters from the corpus
        :param corpus: a tuple of sentences
        :return: 0 if succeeds, 1 if not
        """
        if not isinstance(corpus, tuple):
            return -1
        if len(corpus) == 0:
            return 0
        for sent in corpus:
            for word in sent:
                for letter in word:
                    if self._put_letter(letter) == -1:
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
    if (not isinstance(corpus, tuple)) or (not isinstance(storage, LetterStorage)):
        return ()
    list_corpus = list((list(i) for i in corpus))
    for sent in list_corpus:
        for i, word in enumerate(sent):
            sent[i] = list(word)
    for sent in list_corpus:
        for ind_w, word in enumerate(sent):
            for ind, letter in enumerate(word):
                word[ind] = storage.get_id_by_letter(letter)
            sent[ind_w] = tuple(word)
    encoded_corpus = tuple((tuple(i) for i in list_corpus))
    return encoded_corpus



# 4
def decode_corpus(storage: LetterStorage, corpus: tuple) -> tuple:
    """
    Decodes sentences by replacing letters with their ids
    :param storage: an instance of the LetterStorage class
    :param corpus: an encoded tuple of sentences
    :return: a tuple of the decoded sentences
    """
    if (not isinstance(storage, LetterStorage)) or (not isinstance(corpus, tuple)):
        return ()
    list_corpus = list((list(i) for i in corpus))
    for sent in list_corpus:
        for i, word in enumerate(sent):
            sent[i] = list(word)
    for sent in list_corpus:
        for ind_w, word in enumerate(sent):
            for ind, number in enumerate(word):
                word[ind] = storage.get_letter_by_id(number)
            sent[ind_w] = tuple(word)
    decoded_corpus = tuple((tuple(i) for i in list_corpus))
    return decoded_corpus



# 6
class NGramTrie:
    """
    Stores and manages ngrams
    """
    def __init__(self, n: int, letter_storage: LetterStorage):
        if (not isinstance(n, int)) or (not isinstance(letter_storage, LetterStorage)):
            return None
        self.size = n
        self.storage = letter_storage
        self.n_gram_frequencies = {}
        self.n_grams = []


    # 6 - biGrams
    # 8 - threeGrams
    # 10 - nGrams
    def extract_n_grams(self, encoded_corpus: tuple) -> int:
        if not isinstance(encoded_corpus, tuple):
            return 1
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
        sentences = []
        if encoded_corpus == ():
            return 0
        list_corpus = list((list(i) for i in encoded_corpus))
        for sent in list_corpus:
            for i, word in enumerate(sent):
                sent[i] = list(word)
        for sent in list_corpus:
            for word in sent:
                word = [word[i:i + self.size] for i in range(len(word) - self.size + 1)]
                sentences.append(word)
        for ind, sent in enumerate(sentences):
            for index, word in enumerate(sent):
                sent[index] = tuple(word)
            sentences[ind] = tuple(sent)
        self.n_grams.append(sentences)
        self.n_grams = tuple((tuple(i) for i in self.n_grams))
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
        n_grams_list = []
        if len(self.n_grams) == 0:
            return 1
        for sent in self.n_grams:
            for word in sent:
                for n_gram in word:
                    n_grams_list.append(n_gram)
        for n_gram in n_grams_list:
            if n_gram not in self.n_gram_frequencies:
                self.n_gram_frequencies[n_gram] = n_grams_list.count(n_gram)
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
        if (not isinstance(encoded_corpus, tuple)) or (not isinstance(ngram_sizes, tuple)):
            return 1
        for size in ngram_sizes:
            trie = NGramTrie(size, self.storage)
            # trie.extract_n_grams(encoded_corpus)
            # trie.get_n_grams_frequencies()
            self.tries.append(trie)
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
        if (not isinstance(k, int)) or (not isinstance(trie_level, int))\
                or (k < 1) or (trie_level < 1):
            return ()
        for trie in self.tries:
            if trie.size == trie_level:
                top_n_grams = sorted(trie.n_gram_frequencies,
                                     key=trie.n_gram_frequencies.get, reverse=True)[:k]
                return tuple(top_n_grams)
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
        decoded_freq = {}
        profile_as_dict = {}
        # decode_ng = ''
        for trie in self.tries:
            for n_gram in trie.n_gram_frequencies:
                decode_ng = ''
                for id_letter in n_gram:
                    decode_ng += self.storage.get_letter_by_id(id_letter)
                decoded_freq[decode_ng] = trie.n_gram_frequencies[n_gram]
        profile_as_dict['name'] = self.language
        profile_as_dict['freq'] = decoded_freq
        profile_as_dict['n_words'] = self.n_words
        with open(name, 'w') as file:
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
        with open(file_name, 'r') as file:
            profile_dict = json.load(file)
            self.language = profile_dict['name']
            self.n_words = profile_dict['n_words']
            n_grams = []
            self.tries = []
            for n_gram in profile_dict['freq']:
                decoded_n_gram = []
                for letter in n_gram:
                    self.storage._put_letter(letter)
                    id_by_letter = self.storage.get_id_by_letter(letter)
                    decoded_n_gram.append(id_by_letter)
                n_grams.append((tuple(decoded_n_gram), profile_dict['freq'][n_gram]))
                sizes = {}
            for n_gram in n_grams:
                size = len(n_gram[0])
                if size not in sizes:
                    sizes[size] = {n_gram[0]:n_gram[1]}
                else:
                    sizes[size][n_gram[0]] = n_gram[1]
            for size, freq in sizes.items():
                tries = NGramTrie(size, self.storage)
                tries.n_gram_frequencies = freq
                self.tries.append(tries)
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
    Например, первый набор N-грамм для неизвестного профиля - first_n_grams =
    ((1, 2), (4, 5), (2, 3)),
    второй набор N-грамм для известного профиля – second_n_grams = ((1, 2), (2, 3), (4, 5)).
    Расстояние для (1, 2) равно 0, так как индекс в первом наборе – 0, во втором – 0, |0 – 0| = 0.
    Расстояние для (4, 5) равно 1, расстояние для (2, 3) равно 1.
    Соответственно расстояние между наборами равно 2.
    """
    if (not isinstance(unknown_profile, LanguageProfile)) \
            or (not isinstance(known_profile, LanguageProfile))\
        or (not isinstance(k, int)) or (not isinstance(trie_level, int)):
        return -1
    top_un = unknown_profile.get_top_k_n_grams(k, trie_level)
    top_kn = known_profile.get_top_k_n_grams(k, trie_level)
    distance = 0
    for ind_un, element_un in enumerate(top_un):
        if element_un not in top_kn:
            distance += len(top_kn)
        for ind_kn, element_kn in enumerate(top_kn):
            if element_kn == element_un:
                distance += abs(ind_un - ind_kn)
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
        :return: a dictionary with language labels and their scores if input is correct,otherwise -1
        """
        if (not isinstance(unknown_profile, LanguageProfile)) or (not isinstance(k, int))\
                or (not isinstance(trie_levels, Tuple)):
            return -1
        detected = {}
        for language in self.language_profiles:
            detected[language] = calculate_distance(unknown_profile,
                                                    self.language_profiles[language],
                                                    k, trie_levels[0])
        return detected



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
