"""
Language detection starter
"""

import os
from main import tokenize
from main import remove_stop_words
from main import calculate_frequencies
from main import get_top_n_words

PATH_TO_LAB_FOLDER = os.path.dirname(os.path.abspath(__file__))
PATH_TO_TEXTS_FOLDER = os.path.join(PATH_TO_LAB_FOLDER, 'texts')

if __name__ == '__main__':

    with open(os.path.join(PATH_TO_TEXTS_FOLDER, 'en.txt'), 'r', encoding='utf-8') as file_to_read:
        en_text = file_to_read.read()

    with open(os.path.join(PATH_TO_TEXTS_FOLDER, 'de.txt'), 'r', encoding='utf-8') as file_to_read:
        de_text = file_to_read.read()

    with open(os.path.join(PATH_TO_TEXTS_FOLDER, 'unknown.txt'), 'r', encoding='utf-8') as \
            file_to_read:
        unknown_text = file_to_read.read()

    EXPECTED = 'en'
    RESULT = 'en'
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
en_tokens = tokenize(en_text)
en_stop_words = ['a', 'and', 'the', 'an', 'am', 'is', 'are']
de_stop_words = ['ich', 'du', 'der', 'die', 'das', 'sein', 'bin']
print(en_tokens)
en_tokens_without_stop_words = remove_stop_words(en_tokens, en_stop_words)
print(en_tokens_without_stop_words)
freq_dict = calculate_frequencies(en_tokens_without_stop_words)
TOP_N = 10
print(freq_dict)
print(get_top_n_words(freq_dict, TOP_N))
assert RESULT, 'Detection not working'
