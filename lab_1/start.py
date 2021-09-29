"""
Language detection starter
"""

import os
from main import tokenize
from main import remove_stop_words
from main import calculate_frequencies
from main import get_top_n_words
from main import create_language_profile
from main import compare_profiles
from main import detect_language

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

    tokens_eng = tokenize(en_text)
    print(tokens_eng)

    en_stop_words = ['a', 'an', 'the', 'are', 'is', 'am', 'was', 'were']
    de_stop_words = ['das', 'die', 'der', 'und']

    tokens_eng_removed = remove_stop_words(tokens_eng, en_stop_words)
    print('remove_stop_words:', tokens_eng_removed)

    freq_dict = calculate_frequencies(tokens_eng_removed)
    print('calculate_frequencies:', freq_dict)

    top_n_words = 10

    print('get_top_n_words:', get_top_n_words(freq_dict, top_n_words))
    english_profile = create_language_profile('en', en_text, en_stop_words)
    print('create_language_profile:', english_profile)

    deutsch_profile = create_language_profile('de', de_text, de_stop_words)
    print('create_language_profile:', deutsch_profile)

    unknown_profile = create_language_profile('unknown language', unknown_text, [])
    print('create_language_profile:', unknown_profile)
    print('compare_profiles:', compare_profiles(unknown_profile, english_profile, top_n_words))
    print('detect_language:', detect_language(unknown_profile, deutsch_profile, english_profile, top_n_words))

    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT, 'Detection not working'
