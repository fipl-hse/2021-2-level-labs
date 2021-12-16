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

    changed_text = ''
    for letter in text.lower():
        if letter.isalpha() or letter.isspace():
            changed_text += letter

    tokenized_words = []
    text = changed_text.lower()
    text = text.split()
    for word in text:
        words = []
        for letter in word:
            words.append(letter)
        words.append('_')
        words.insert(0, '_')
        tokenized_words.append(tuple(words))
    return tuple(tokenized_words)


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

        else:
            super().update(elements)
            return 0


    def get_letter_count(self) -> int:
        """
        Gets the number of letters in the storage
        """

        if not self.storage:
            return -1
        else:
            return len(self.storage)


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

    storage.update(corpus)
    encoded_corpus = tuple(tuple(storage.get_id(letter) for letter in word) for word in corpus)
    return encoded_corpus


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

    decoded_corpus = tuple(tuple(storage.get_element(letter) for letter in word) for word in sentence)
    return decoded_corpus


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

        if not isinstance(context, tuple):
            return -1

        predicted_letters = {}

        for trie in self.profile.tries:
            if trie.size == len(context) + 1:

                for key, value in trie.n_gram_frequencies.items():
                    if self._used_n_grams == list(trie.n_gram_frequencies.keys()):
                        self._used_n_grams = []
                    elif key[:len(context)] == context and key not in self._used_n_grams:
                        predicted_letters[key] = value

                if predicted_letters:
                    prediction = max(predicted_letters.keys(), key=predicted_letters.get)
                    self._used_n_grams.append(prediction)
                else:
                    prediction = max(trie.n_gram_frequencies.keys(), key=trie.n_gram_frequencies.get)
                return prediction[-1]

            else:
                return -1


    def _generate_word(self, context: tuple, word_max_length=15) -> tuple:
        """
        Generates full word for the context given.
        """

        if not (isinstance(context, tuple) and isinstance(word_max_length, int)):
            return ()

        generated_word = list(context)

        if word_max_length == 1:
            generated_word.append(self.profile.storage.get_special_token_id())
            return tuple(generated_word)

        while generated_word != word_max_length:
            letter = self._generate_letter(context)
            generated_word.append(letter)
            if letter == self.profile.storage.get_special_token_id():
                break
            context = tuple(generated_word[-len(context):])
        return tuple(generated_word)


    def generate_sentence(self, context: tuple, word_limit: int) -> tuple:
        """
        Generates full sentence with fixed number of words given.
        """

        if not (isinstance(context, tuple) and isinstance(word_limit, int)):
            return ()

        generated_sentence = []

        while len(generated_sentence) != word_limit:
            generated_word = self._generate_word(context, word_max_length=15)
            generated_sentence.append(generated_word)
            context = tuple(generated_word[-len(context):])
        return tuple(generated_sentence)


    def generate_decoded_sentence(self, context: tuple, word_limit: int) -> str:
        """
        Generates full sentence and decodes it
        """

        if not (isinstance(context, tuple) and isinstance(word_limit, int)):
            return ''

        generated_sentence = self.generate_sentence(context, word_limit)
        decoded_sentence = ''

        for word in generated_sentence:
            for letter_id in word:
                letter = self.profile.storage.get_element(letter_id)
                decoded_sentence += letter
        result = decoded_sentence.replace('__', ' ')
        result = result.replace('_', '')
        result = result.capitalize() + '.'
        return result


# 6
def translate_sentence_to_plain_text(decoded_corpus: tuple) -> str:
    """
    Converts decoded sentence into the string sequence
    """

    if not (isinstance(decoded_corpus, tuple) and decoded_corpus):
        return ''

    decoded_sentence = ''
    for element in decoded_corpus:
        for symbol in element:
            decoded_sentence += symbol
    result = decoded_sentence.replace('__', ' ')
    result = result.replace('_', '')
    result = result.capitalize() + '.'
    return result
