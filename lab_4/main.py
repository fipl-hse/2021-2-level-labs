"""
Lab 4
Language generation algorithm based on language profiles
"""

from typing import Tuple
from lab_4.storage import Storage
from lab_4.language_profile import LanguageProfile, NGramTrie

# 4
def tokenize_by_letters(text: str) -> Tuple or int:
    """
    Tokenizes given sequence by letters
    """
    if not isinstance(text,str):
        return -1
    not_letters = ['`', '~', '!', '@', '#', '$', '%', '^', '&', '*',
                   '(', ')', '_', '-', '+', '=', '{', '[', ']', '}',
                   '|', '\\', ':', ';', '"', "'", '<', ',', '>','.',
                   '?', '/', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
    for not_letter in not_letters:
        text = text.replace(not_letter, "")
    text = text.lower()
    text_list = text.split()
    tokenized_text = []
    for word in text_list:
        word_by_letter = ['_']
        for letter in word:
            word_by_letter.append(letter)
        word_by_letter.append('_')
        tokenized_text.append(tuple(word_by_letter))
    return tuple(tokenized_text)

# 4
class LetterStorage(Storage):
    """
    Stores letters and their ids
    """

    def update(self, elements: tuple) -> int:
        """
        Fills a storage by letters from the tuple
        :param elements: a tuple of tuples of letters
        :return: 0 if succeeds, -1 if not
        """
        if not isinstance(elements, tuple):
            return -1
        indexes = list(self.storage.values())
        #if indexes != []:
            #index = max(indexes) + 1
        #else:
        index = 1
        for word in elements:
            for letter in word:
                if letter not in self.storage:
                    self.storage[letter] = index
                    index += 1
        return 0

    def get_letter_count(self) -> int:
        """
        Gets the number of letters in the storage
        """
        length = len(self.storage.keys())
        if length == 0:
            return -1
        return length


# 4
def encode_corpus(storage: LetterStorage, corpus: tuple) -> tuple:
    """
    Encodes corpus by replacing letters with their ids
    :param storage: an instance of the LetterStorage class
    :param corpus: a tuple of tuples
    :return: a tuple of the encoded letters
    """
    if not (isinstance(storage, LetterStorage) and isinstance(corpus, tuple)):
        return ()
    encoded_corpus = []
    for word in corpus:
        encoded_word = []
        for letter in word:
            encoded_word.append(storage.get_id(letter))
        encoded_corpus.append(tuple(encoded_word))
    return tuple(encoded_corpus)

# 4
def decode_sentence(storage: LetterStorage, sentence: tuple) -> tuple:
    """
    Decodes sentence by replacing letters with their ids
    :param storage: an instance of the LetterStorage class
    :param sentence: a tuple of tuples-encoded words
    :return: a tuple of the decoded sentence
    """
    if not (isinstance(storage, LetterStorage) and isinstance(sentence, tuple)):
        return ()
    decoded_sentence = []
    for word in sentence:
        encoded_word = []
        for id in word:
            encoded_word.append(storage.get_element(id))
        decoded_sentence.append(tuple(encoded_word))
    return tuple(decoded_sentence)


# 6
class NGramTextGenerator:
    """
    Language model for basic text generation
    """

    def __init__(self, language_profile: LanguageProfile):
        self.language_profile = language_profile
        self._used_n_grams = []

    def _generate_letter(self, context: tuple) -> int:
        """
        Generates the next letter.
            Takes the letter from the most
            frequent ngram corresponding to the context given.
        """
        if not (isinstance(context, tuple) and len(context) != 1):
            return -1
        possible_n_grams = {}
        all_is_possible = {}
        for trie in self.language_profile.tries:
            all_is_possible = sorted(trie.n_gram_frequencies, key=lambda x: x[1], reverse=True)
            if trie.n_grams in self._used_n_grams:
                self._used_n_grams = []
            for n_gram in trie.n_gram_frequencies:
                if n_gram not in self._used_n_grams and len(n_gram) > len(context):
                    counter = 0
                    for index, letter in enumerate(context):
                        if context[index] != n_gram[index]:
                            counter +=1
                            break
                    if counter == 0:
                        possible_n_grams[n_gram] = trie.n_gram_frequencies[n_gram]
        if possible_n_grams == {}:
            used_n_gram = all_is_possible[0]
        else:
            possible_n_grams_tuple = sorted(possible_n_grams, key=lambda x: x[1], reverse=True)
            used_n_gram = possible_n_grams_tuple[0]
        self._used_n_grams.append(used_n_gram)
        result = used_n_gram[len(context)]
        return result

    def _generate_word(self, context: tuple, word_max_length=15) -> tuple:
        """
        Generates full word for the context given.
        """
        if not (isinstance(context,tuple) and isinstance(word_max_length, int)):
            return ()
        generated_word = []
        for number in context:
            generated_word.append(number)
        while len(generated_word) < word_max_length:
            letter = self._generate_letter(context)
            generated_word.append(letter)
            if letter == 1:
                break
        return tuple(generated_word)


    def generate_sentence(self, context: tuple, word_limit: int) -> tuple:
        """
        Generates full sentence with fixed number of words given.
        """
        if not (isinstance(context,tuple) and isinstance(word_limit, int)):
            return ()
        generated_sentence = []
        while len(generated_sentence) < word_limit:
            generated_word = self._generate_word(context)
            generated_sentence.append(generated_word)
            context = generated_word[-1]
        return tuple(generated_sentence)


    def generate_decoded_sentence(self, context: tuple, word_limit: int) -> str:
        """
        Generates full sentence and decodes it
        """
        pass


# 6
def translate_sentence_to_plain_text(decoded_corpus: tuple) -> str:
    """
    Converts decoded sentence into the string sequence
    """
    pass


# 8
class LikelihoodBasedTextGenerator(NGramTextGenerator):
    """
    Language model for likelihood based text generation
    """

    def _calculate_maximum_likelihood(self, letter: int, context: tuple) -> float:
        """
        Calculates maximum likelihood for a given letter
        :param letter: a letter given
        :param context: a context for the letter given
        :return: float number, that indicates maximum likelihood
        """
        pass

    def _generate_letter(self, context: tuple) -> int:
        """
        Generates the next letter.
            Takes the letter with highest
            maximum likelihood frequency.
        """
        pass


# 10
class BackOffGenerator(NGramTextGenerator):
    """
    Language model for back-off based text generation
    """

    def _generate_letter(self, context: tuple) -> int:
        """
        Generates the next letter.
            Takes the letter with highest
            available frequency for the corresponding context.
            if no context can be found, reduces the context size by 1.
        """
        pass


# 10
class PublicLanguageProfile(LanguageProfile):
    """
    Language Profile to work with public language profiles
    """

    def open(self, file_name: str) -> int:
        """
        Opens public profile and adapts it.
        :return: o if succeeds, 1 otherwise
        """
        pass
