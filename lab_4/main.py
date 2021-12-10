"""
Lab 4
Language generation algorithm based on language profiles
"""

from typing import Tuple
from lab_4.storage import Storage
from lab_4.language_profile import LanguageProfile


# 4
def tokenize_by_letters(text: str) -> Tuple or int:
    """
    Tokenizes given sequence by letters
    """
    if not isinstance(text, str):
        return -1

    text = "".join(char for char in text if char.isalpha() or char.isspace())
    text_tupled = tuple(tuple("_" + word + "_") for word in text.lower().strip().split())

    return text_tupled


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

        for word in elements:
            for letter in word:
                self._put(letter)
        return 0

    def get_letter_count(self) -> int:
        """
        Gets the number of letters in the storage
        """
        if not self.storage:
            return -1

        return len(self.storage)


# 4
def encode_corpus(storage: LetterStorage, corpus: tuple) -> tuple:
    """
    Encodes corpus by replacing letters with their ids
    :param storage: an instance of the LetterStorage class
    :param corpus: a tuple of tuples
    :return: a tuple of the encoded letters
    """
    if not (isinstance(corpus, tuple) and isinstance(storage, LetterStorage)):
        return ()

    storage.update(corpus)
    encoded = tuple(tuple(storage.get_id(letter)
                          for letter in word)
                    for word in corpus)

    return encoded


# 4
def decode_sentence(storage: LetterStorage, sentence: tuple) -> tuple:
    """
    Decodes sentence by replacing letters with their ids
    :param storage: an instance of the LetterStorage class
    :param sentence: a tuple of tuples-encoded words
    :return: a tuple of the decoded sentence
    """
    if not (isinstance(sentence, tuple) and isinstance(storage, LetterStorage)):
        return ()

    decoded = tuple(tuple(storage.get_element(letter)
                          for letter in word)
                    for word in sentence)

    return decoded


# 6
class NGramTextGenerator:
    """
    Language model for basic text generation
    """

    def __init__(self, language_profile: LanguageProfile):
        self.profile = language_profile
        self._used_n_grams = []

    def _generate_letter(self, context: tuple) -> int:
        """
        Generates the next letter.
            Takes the letter from the most
            frequent ngram corresponding to the context given.
        """
        if not isinstance(context, tuple) or len(context) > 1:
            return -1

        best_choice = [(), 0]
        check_choice = True
        check_update = True
        while check_update and check_choice:
            for n_gram, freq in profile.n_gram_frequencies.items():
                if len(self._used_n_grams) >= len(profile.n_gram_frequencies):
                    self._used_n_grams = []
                    check_update = False

                if n_gram[0] == context[0]:
                    self._used_n_grams.append(n_gram)
                    if freq > best_choice[0]:
                        if n_gram[0] not in list(zip(*self._used_n_grams))[0]:
                            best_choice = [n_gram, freq]
                            check_choice = False

        if best_choice[0] == ():
            best_choice = sorted(profile.n_gram_frequencies.items(),
                                 key=lambda x: x[1], reverse=True)[0]

        length_tuple = len(best_choice[0])
        return best_choice[0][length_tuple - 1]

    def _generate_word(self, context: tuple, word_max_length=15) -> tuple:
        """
        Generates full word for the context given.
        """
        if not isinstance(context, tuple):
            return ()

        underscore_id = generator.profile.storage.get_special_token_id())
        symbol = 0
        counter = 0
        word = ()
        while symbol != underscore_id and counter < word_max_length:
            word += (symbol,)

        return word

    def generate_sentence(self, context: tuple, word_limit: int) -> tuple:
        """
        Generates full sentence with fixed number of words given.
        """
        if not isinstance(context, tuple):
            return ()

        sentence = ()
        context_cur = context
        for i in range(word_limit):
            sentence += ((self._generate_word(context_cur)),)
            context_cur = (sentence[i][len(sentence[i]-1)],)

        return sentence


    def generate_decoded_sentence(self, context: tuple, word_limit: int) -> str:
        """
        Generates full sentence and decodes it
        """
        if not isinstance(context, tuple):
            return -1

        result = ""
        for (index, word) in enumerate(context):
            for symbol in word:
                tmp_str = profile.letter_storage.get_element(symbol)
                if tmp_str.isalnum():
                    result += tmp_str
                if tmp_str == "_":
                    if result[i-1] == "_":
                        result += " "
                    if len(result) - len(context) == 1:
                        result += "."

        return result

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
