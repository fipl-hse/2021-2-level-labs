"""
Lab 4
Language generation algorithm based on language profiles
"""

import json
from typing import Tuple
from lab_4.storage import Storage
from lab_4.language_profile import LanguageProfile
from lab_4.language_profile import NGramTrie


# 4
def tokenize_by_letters(text: str) -> Tuple or int:
    """
    Tokenizes given sequence by letters
    """

    if not isinstance(text, str):
        return -1

    invaluable_trash = ['`', '~', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '-', '+',
                        '=', '{', '[', ']', '}', '|', '\\', ':', ';', '"', "'", '<', ',', '>',
                        '/', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
    text = text.lower()

    for symbols in invaluable_trash:
        text = text.replace(symbols, '')

    if not text:
        return ()

    if text:
        last_character = text[-1]
        if last_character in ('.', '!', '?'):
            text = text[:-1]

    text = text.replace('.', '<stop>')
    text = text.replace('?', '<stop>')
    text = text.replace('!', '<stop>')

    sentences = text.split('<stop>')

    processed_tokens = []

    for sentence in sentences:
        tokens = sentence.split()

        for token in tokens:
            processed_characters = ['_']

            for character in token:
                processed_characters.append(character)

            processed_characters.append('_')

            processed_tokens.append(tuple(processed_characters))

    return tuple(processed_tokens)


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

        for sentence in elements:
            for token in sentence:
                for letter in token:
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

    if not isinstance(storage, LetterStorage) or not isinstance(corpus, tuple):
        return ()

    encoded_corpus = []

    for token in corpus:
        encoded_token = []

        for character in token:
            encoded_token.append(storage.get_id(character))

        encoded_corpus.append(tuple(encoded_token))

    return tuple(encoded_corpus)


# 4
def decode_sentence(storage: LetterStorage, sentence: tuple) -> tuple:
    """
    Decodes sentence by replacing letters with their ids
    :param storage: an instance of the LetterStorage class
    :param sentence: a tuple of tuples-encoded words
    :return: a tuple of the decoded sentence
    """

    if not isinstance(storage, LetterStorage) or not isinstance(sentence, tuple):
        return ()

    decoded_corpus = []

    for token in sentence:
        decoded_token = []

        for character in token:
            decoded_token.append(storage.get_element(character))

        decoded_corpus.append(tuple(decoded_token))

    return tuple(decoded_corpus)


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

        if not isinstance(context, tuple) or not self.language_profile.tries:
            return -1

        available_next_ngrams = {}
        no_used_ngrams_next_ngrams = {}
        all_ngrams_from_trie = {}

        context_length = len(context)

        for trie in self.language_profile.tries:
            for ngram in trie.n_gram_frequencies:
                if len(ngram) != context_length + 1:
                    continue

                all_ngrams_from_trie[ngram] = trie.n_gram_frequencies[ngram]

                if ngram[:-1] != context:
                    continue

                no_used_ngrams_next_ngrams[ngram] = trie.n_gram_frequencies[ngram]

                if ngram in self._used_n_grams:
                    continue

                available_next_ngrams[ngram] = trie.n_gram_frequencies[ngram]

        if available_next_ngrams:
            next_ngram = max(available_next_ngrams, key=available_next_ngrams.get)
        elif no_used_ngrams_next_ngrams:
            self._used_n_grams = []
            next_ngram = max(no_used_ngrams_next_ngrams, key=no_used_ngrams_next_ngrams.get)
        elif all_ngrams_from_trie:
            next_ngram = max(all_ngrams_from_trie, key=all_ngrams_from_trie.get)
        else:
            return -1

        self._used_n_grams.append(next_ngram)

        return next_ngram[-1]

    def _generate_word(self, context: tuple, word_max_length=15) -> tuple:
        """
        Generates full word for the context given.
        """

        if not isinstance(context, tuple) or not isinstance(word_max_length, int):
            return ()

        word = []
        word_length = 0
        last_character_id = -1

        context_length = len(context)

        if context_length > 1 \
                and context[-1] == self.language_profile.storage.get_special_token_id():
            context = (self.language_profile.storage.get_special_token_id(),)

        for character in context:
            word.append(character)
            word_length += 1

        special_character_id = self.language_profile.storage.get_special_token_id()

        while last_character_id != special_character_id:
            if word:
                context = tuple(word[-context_length:])

            if word_length >= word_max_length:
                generated_character_id = special_character_id
            else:
                generated_character_id = self._generate_letter(context)

            word_length += 1
            last_character_id = generated_character_id
            word.append(generated_character_id)

        return tuple(word)

    def generate_sentence(self, context: tuple, word_limit: int) -> tuple:
        """
        Generates full sentence with fixed number of words given.
        """

        if not isinstance(context, tuple) or not isinstance(word_limit, int):
            return ()

        context_length = len(context)

        sentence = [self._generate_word(context)]

        all_generated_characters = []

        for _ in range(word_limit - 1):
            for word in sentence:
                for character in word:
                    all_generated_characters.append(character)

            new_context = tuple(all_generated_characters[-context_length:])

            # Start with the last generated context of context length
            sentence.append(self._generate_word(new_context))

            # #Start with special token
            # special_token_id = self.language_profile.storage.get_special_token_id()
            # sentence.append(self._generate_word((special_token_id,)))

            # #Start with the last generated context of context length of the last word
            # sentence.append(self._generate_word(sentence[len(sentence) - 1][-context_length:]))

        return tuple(sentence)

    def generate_decoded_sentence(self, context: tuple, word_limit: int) -> str:
        """
        Generates full sentence and decodes it
        """

        if not isinstance(context, tuple):
            return ()

        sentence = self.generate_sentence(context, word_limit)

        return translate_sentence_to_plain_text(decode_sentence(self.language_profile.storage,
                                                                sentence))


# 6
def translate_sentence_to_plain_text(decoded_corpus: tuple) -> str:
    """
    Converts decoded sentence into the string sequence
    """

    if not isinstance(decoded_corpus, tuple) or not decoded_corpus:
        return ''

    decoded_string = ""

    for word in decoded_corpus:
        added_character = False

        for character in word:
            if character == '_':
                if decoded_string and not added_character:
                    decoded_string += " "
            else:
                if decoded_string:
                    decoded_string += character
                else:
                    decoded_string += character.upper()

            added_character = True

    decoded_string += '.'

    return decoded_string


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

        if not isinstance(letter, int) or not isinstance(context, tuple) or not context:
            return -1

        required_letter_context_frequency = 0.0
        all_appropriate_context_frequency = 0.0

        for trie in self.language_profile.tries:
            for ngram in trie.n_gram_frequencies:
                ngram_without_closing_character = ngram[:-1]
                closing_ngram_character = ngram[-1]

                if ngram_without_closing_character == context:
                    ngram_frequency = trie.n_gram_frequencies[ngram]

                    all_appropriate_context_frequency += ngram_frequency

                    if closing_ngram_character == letter:
                        required_letter_context_frequency += ngram_frequency

        if all_appropriate_context_frequency != 0.0:
            return required_letter_context_frequency / all_appropriate_context_frequency

        return 0.0

    def _generate_letter(self, context: tuple) -> int:
        """
        Generates the next letter.
            Takes the letter with highest
            maximum likelihood frequency.
        """

        if not isinstance(context, tuple) or not self.language_profile.tries or not context:
            return -1

        letters_likelihood = {}

        for letter in self.language_profile.storage.storage.values():
            likelihood = self._calculate_maximum_likelihood(letter, context)

            if likelihood > 0.0:
                letters_likelihood[letter] = likelihood

        if letters_likelihood:
            return max(letters_likelihood, key=letters_likelihood.get)

        special_character_id = self.language_profile.storage.get_special_token_id()

        for trie in self.language_profile.tries:
            unigrams = {}

            if trie.size == 1:
                for ngram in trie.n_gram_frequencies:
                    if context[-1] == special_character_id and ngram[0] == special_character_id:
                        continue

                    unigrams[ngram] = trie.n_gram_frequencies[ngram]

                next_ngram = max(unigrams, key=unigrams.get)
                return next_ngram[-1]

        return -1


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

        if not isinstance(context, tuple) or not self.language_profile.tries or not context:
            return -1

        context_size = len(context)

        tries_sorted_by_size_in_reverse = sorted(self.language_profile.tries,
                                                 key=lambda ngram_trie: -ngram_trie.size)

        for trie in tries_sorted_by_size_in_reverse:
            if trie.size <= context_size + 1:
                available_next_ngrams = {}

                for ngram in trie.n_gram_frequencies:
                    if ngram in self._used_n_grams:
                        continue

                    if trie.size != 1:
                        if ngram[:-1] != context[-trie.size + 1:]:
                            continue

                    available_next_ngrams[ngram] = trie.n_gram_frequencies[ngram]

                if available_next_ngrams:
                    next_ngram = max(available_next_ngrams, key=available_next_ngrams.get)
                    self._used_n_grams.append(next_ngram)

                    return next_ngram[-1]

        return -1


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

        if not isinstance(file_name, str):
            return 1

        with open(file_name, "r", encoding="utf-8") as file:
            data = json.load(file)

            self.language = data['name']
            self.n_words = data['n_words']

            decoded_ngrams = {}

            for ngram in data['freq']:
                decoded_ngram = []
                for letter in ngram:

                    if letter == ' ':
                        processed_letter = '_'
                    elif letter.isupper():
                        processed_letter = letter.lower()
                    else:
                        processed_letter = letter

                    self.storage.update((((processed_letter,),),))
                    decoded_ngram.append(self.storage.get_id(processed_letter))

                if tuple(decoded_ngram) in decoded_ngrams:
                    decoded_ngrams[tuple(decoded_ngram)] += data['freq'][ngram]
                else:
                    decoded_ngrams[tuple(decoded_ngram)] = data['freq'][ngram]

            ngram_sizes_dict = {}

            for ngram, freq in decoded_ngrams.items():
                size = len(ngram)

                if size not in ngram_sizes_dict:
                    ngram_sizes_dict[size] = {}

                ngram_sizes_dict[size][ngram] = freq

            for size, group in ngram_sizes_dict.items():
                trie = NGramTrie(size, self.storage)
                trie.n_gram_frequencies = group
                self.tries.append(trie)

        return 0
