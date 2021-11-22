"""
Lab 3
Language classification using n-grams
"""

from typing import Dict, Tuple
import re


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

    changed_letters = {'ö': 'oe', 'ü': 'ue', 'ä': 'ae', 'ß': 'ss'}

    text = text.lower()

    for wrong_letter, changed_letter in changed_letters.items():
        text = text.replace(wrong_letter, changed_letter)

    without_digits = re.split(r"[\d]", text)
    text = ''.join(without_digits)
    changed_text = re.split(r"[.!?] *", text)

    if '' in changed_text:
        changed_text.remove('')

    sentences_tuple = []

    for sentence in changed_text:
        sentence = sentence.split()
        new_words = []

        for word in sentence:
            letters = [letter for letter in word if letter.isalpha()]
            if len(letters) != 0:
                letters.insert(0, '_')
                letters.append('_')
                new_words.append(tuple(letters))
            if len(new_words) == 0:
                return ()

        sentences_tuple.append(tuple(new_words))
    return tuple(sentences_tuple)


# 4
class LetterStorage:
    """
    Stores and manages letters
    """

    def __init__(self):
        self.storage = {}
        self.id = 0


    def _put_letter(self, letter: str) -> int:
        """
        Puts a letter into storage, assigns a unique id
        :param letter: a letter
        :return: 0 if succeeds, 1 if not
        """

        if not isinstance(letter, str):
            return -1

        if letter not in self.storage:
            self.storage[letter] = self.id
            self.id += 1
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
        return self.storage[letter]


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

        for letter, id in self.storage.items():
            if id == letter_id:
                return letter


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


# 4
def encode_corpus(storage: LetterStorage, corpus: tuple) -> tuple:
    """
    Encodes sentences by replacing letters with their ids
    :param storage: an instance of the LetterStorage class
    :param corpus: a tuple of sentences
    :return: a tuple of the encoded sentences
    """

    if not (isinstance(storage, LetterStorage) and isinstance(corpus, tuple)):
        return ()

    storage.update(corpus)
    encoded_corpus = []

    for sentence in corpus:
        encoded_sentences = []

        for word in sentence:
            encoded_words = []

            for letter in word:
                encoded_words.append(storage.get_id_by_letter(letter))
            encoded_sentences.append(tuple(encoded_words))
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

    if not (isinstance(storage, LetterStorage) and isinstance(corpus, tuple)):
        return ()

    storage.update(corpus)
    decoded_corpus = []

    for sentence in corpus:
        decoded_sentences = []

        for word in sentence:
            decoded_words = []

            for letter in word:
                decoded_words.append(storage.get_letter_by_id(letter))
            decoded_sentences.append(tuple(decoded_words))
        decoded_corpus.append(tuple(decoded_sentences))
    return tuple(decoded_corpus)


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

        n_grams_list = []

        for sentence in encoded_corpus:
            n_grams_sentence = []

            for word in sentence:
                n_gram_word = []

                for index in range(len(word) - (self.size - 1)):
                    n_gram_word.append(tuple(word[index:(index + self.size)]))
                n_grams_sentence.append(tuple(n_gram_word))
            n_grams_list.append(tuple(n_grams_sentence))
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
                for n_gram in word:
                    if n_gram in self.n_gram_frequencies:
                        self.n_gram_frequencies[n_gram] += 1
                    else:
                        self.n_gram_frequencies[n_gram] = 1
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

        if not (isinstance(encoded_corpus, tuple) and isinstance(ngram_sizes, tuple)):
            return 1

        for size in ngram_sizes:
            n_gram = NGramTrie(size, self.storage)
            self.tries.append(n_gram)
            n_gram.extract_n_grams(encoded_corpus)
            n_gram.get_n_grams_frequencies()
            self.n_words.append(len(n_gram.n_gram_frequencies))
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

        if not (isinstance(k, int) and isinstance(trie_level, int)) or k < 1:
            return ()

        for n_gram in self.tries:
            if n_gram.size == trie_level:
                frequency = n_gram.n_gram_frequencies
                top_k_ngrams = tuple(sorted(frequency, key=frequency.get, reverse=True)[:k])
                return top_k_ngrams
        else:
            return ()


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

    if not (isinstance(unknown_profile, LanguageProfile) and isinstance(known_profile, LanguageProfile) and
            isinstance(k, int) and isinstance(trie_level, int)):
        return -1

    distance = 0
    unknown_profile = unknown_profile.get_top_k_n_grams(k, trie_level)
    known_profile = known_profile.get_top_k_n_grams(k, trie_level)
    for unknown_index, unknown_n_gram in enumerate(unknown_profile):
        for known_index, known_n_gram in enumerate(known_profile):
            if unknown_n_gram == known_n_gram:
                distance += unknown_index - known_index
        if unknown_n_gram not in known_profile:
            distance += len(known_profile)
    return distance
