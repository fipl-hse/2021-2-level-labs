"""
Lab 3
Language classification using n-grams
"""

from typing import Dict, Tuple
import re


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
    """
    Stores and manages letters
    """

    def __init__(self):
        self.storage = {}

    def _put_letter(self, letter: str) -> int:
        """
        Puts a letter into storage, assigns a unique id
        :param letter: a letter
        :return: 0 if succeeds, 1 if not
        """
        if isinstance(letter, str):
            if letter not in self.storage:
                self.storage[letter] = len(self.storage) + 1
            return 0
        else:
            return -1

    def get_id_by_letter(self, letter: str) -> int:
        """
        Gets a unique id by a letter
        :param letter: a letter
        :return: an id
        """
        if isinstance(letter, str) and letter in self.storage:
            return self.storage[letter]
        else:
            return -1

    def get_letter_by_id(self, letter_id: int) -> str or int:
        """
        Gets a letter by a unique id
        :param letter_id: a unique id
        :return: letter
        """
        if isinstance(letter_id, int):
            for k, v in self.storage.items():
                if letter_id == v:
                    return k
            return -1
        else:
            return -1

    def update(self, corpus: tuple) -> int:
        """
        Fills a storage by letters from the corpus
        :param corpus: a tuple of sentences
        :return: 0 if succeeds, 1 if not
        """
        if isinstance(corpus, tuple):
            for sentence in corpus:
                for word in sentence:
                    for letter in word:
                        self._put_letter(letter)
            return 0
        else:
            return -1


def encode_corpus(storage: LetterStorage, corpus: tuple) -> tuple:
    """
    Decodes sentences by replacing letters with their ids
    :param storage: an instance of the LetterStorage class
    :param corpus: an encoded tuple of sentences
    :return: a tuple of the decoded sentences
    """
    if isinstance(storage, LetterStorage) and isinstance(corpus, tuple):
        storage.update(corpus)
        result = []
        for c in corpus:
            enc_c = []
            for word in c:
                id_word = []
                for letter in word:
                    id_word.append(storage.get_id_by_letter(letter))
                enc_c.append(tuple(id_word))
            result.append(tuple(enc_c))
        return tuple(result)
    else:
        return ()


def decode_corpus(storage: LetterStorage, corpus: tuple) -> tuple:
    """
    Decodes sentences by replacing letters with their ids
    :param storage: an instance of the LetterStorage class
    :param corpus: an encoded tuple of sentences
    :return: a tuple of the decoded sentences
    """
    if isinstance(storage, LetterStorage) and isinstance(corpus, tuple):
        storage.update(corpus)
        result = []
        for encoded_sent in corpus:
            enc_c = []
            for id_word in encoded_sent:
                word = []
                for id_letter in id_word:
                    word.append(storage.get_letter_by_id(id_letter))
                enc_c.append(tuple(word))
            result.append(tuple(enc_c))
        return tuple(result)
    else:
        return ()
