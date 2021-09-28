"""
Language detection starter
"""

import os

from lab_1.main import tokenize, remove_stop_words, calculate_frequencies, get_top_n_words

PATH_TO_LAB_FOLDER = os.path.dirname(os.path.abspath(__file__))
PATH_TO_TEXTS_FOLDER = os.path.join(PATH_TO_LAB_FOLDER, 'texts')git

if __name__ == '__main__':

    with open(os.path.join(PATH_TO_TEXTS_FOLDER, 'en.txt'), 'r', encoding='utf-8') as file_to_read:
        en_text = file_to_read.read()
        tokenize('en.txt')
        remove_stop_words('en.txt')
        calculate_frequencies('en.txt')
        get_top_n_words('en.txt')


    with open(os.path.join(PATH_TO_TEXTS_FOLDER, 'de.txt'), 'r', encoding='utf-8') as file_to_read:
        de_text = file_to_read.read()
        tokenize('de.txt')
        remove_stop_words('de.txt')
        calculate_frequencies('de.txt')
        get_top_n_words('de.txt')

    with open(os.path.join(PATH_TO_TEXTS_FOLDER, 'unknown.txt'), 'r', encoding='utf-8') as \
            file_to_read:
        unknown_text = file_to_read.read()
        tokenize('unknown.txt')
        remove_stop_words('unknown.txt')
        calculate_frequencies('unknown.txt')
        get_top_n_words('unknown.txt')

    EXPECTED = 'en'
    RESULT = ''
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT, 'Detection not working'
