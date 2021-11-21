import re
from typing import Dict, Tuple


def tokenize_by_sentence(text: str) -> tuple:
    if isinstance(text, str):
        text = text.lower()
        sentences = re.split(
            r"[.!?]", text
        )  # разбиение текста на список предложений, которые заканчиваются символами(".", "!", "?")
        if "" in sentences:
            sentences.remove("")  # очистка от пустой строки в конце списка

        result = []
        for sentence in sentences:
            sentence_list = sentence.split()
            sentence_letters_list = []
            for word in sentence_list:
                word.replace("ö", "oe")
                word.replace("ü", "ue")
                word.replace("ä", "ae")
                word.replace("ß", "ss")
                letters_list = [letter for letter in word if letter.isalpha()]
                if letters_list:
                    letters_list.insert(0, "_")
                    letters_list.append("_")
                    sentence_letters_list.append(tuple(letters_list))
                if not sentence_letters_list:
                    return ()
            result.append(tuple(sentence_letters_list))
        return tuple(result)
    else:
        return ()


class LetterStorage:
    def __init__(self):
        self.storage = {}
        self.counter = 0

    def _put_letter(self, letter: str) -> int:
        if isinstance(letter, str):
            if letter not in self.storage:
                self.storage[letter] = len(self.storage) + 1
            return 0
        else:
            return -1

    def get_id_by_letter(self, letter: str) -> int:
        if isinstance(letter, str) and letter in self.storage:
            return self.storage[letter]
        else:
            return -1

    def get_letter_by_id(self, letter_id: int) -> str or int:
        if isinstance(letter_id, int):
            for k, v in self.storage.items():
                if letter_id == v:
                    return k
            return -1
        else:
            return -1

    def update(self, corpus: tuple) -> int:
        if isinstance(corpus, tuple):
            for sentence in corpus:
                for word in sentence:
                    for letter in word:
                        self._put_letter(letter)
            return 0
        else:
            return -1

# 4
def encode_corpus(storage: LetterStorage, corpus: tuple) -> tuple:
    """
    Encodes sentences by replacing letters with their ids
    :param storage: an instance of the LetterStorage class
    :param corpus: a tuple of sentences
    :return: a tuple of the encoded sentences
    """
    pass


# 4
def decode_corpus(storage: LetterStorage, corpus: tuple) -> tuple:
    """
    Decodes sentences by replacing letters with their ids
    :param storage: an instance of the LetterStorage class
    :param corpus: an encoded tuple of sentences
    :return: a tuple of the decoded sentences
    """
    pass


# 6
class NGramTrie:
    """
    Stores and manages ngrams
    """
    
    def __init__(self, n: int, letter_storage: LetterStorage):
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
        pass

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
    """
    Stores and manages language profile information
    """
    
    def __init__(self, letter_storage: LetterStorage, language_name: str):
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

        self.tries --> [<__main__.NGramTrie object at 0x09DB9BB0>, <__main__.NGramTrie object at 0x09DB9A48>]
        self.n_words --> [11, 9]
        self.tries[0].n_grams --> (
            (((1, 2), (2, 3), (3, 1)), ((1, 4), (4, 5), (5, 1)), ((1, 2), (2, 6), (6, 7), (7, 7), (7, 8), (8, 1))),
        )
        """
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
        pass

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
def calculate_distance(unknwon_profile: LanguageProfile, known_profile: LanguageProfile,
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
    pass


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

    def detect(self, unknown_profile: LanguageProfile, k: int, trie_levels: tuple) -> Dict[Tuple[str, int], int or float] or int:
        """
        Detects the language of an unknown profile and its probability score
        :param unknown_profile: an instance of LanguageDetector
        :param k: a number of the most common n-grams
        :param trie_levels: N-gram size
        :return: sorted language labels with corresponding ngram size and their prob scores if input is correct, otherwise -1
        """
        pass
