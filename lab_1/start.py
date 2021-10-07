"""
Language detection starter
"""

import os

from lab_1.main import tokenize, remove_stop_words, calculate_frequencies, get_top_n_words, create_language_profile, \
    compare_profiles, detect_language, compare_profiles_advanced, detect_language_advanced

PATH_TO_LAB_FOLDER = os.path.dirname(os.path.abspath(__file__))
PATH_TO_TEXTS_FOLDER = os.path.join(PATH_TO_LAB_FOLDER, 'texts')

if __name__ == '__main__':

    with open(os.path.join(PATH_TO_TEXTS_FOLDER, 'en.txt'), 'r', encoding='utf-8') as file_to_read:
        en_text = file_to_read.read()
        tokenize('en.txt')
        remove_stop_words('en.txt')
        calculate_frequencies('en.txt')
        get_top_n_words('en.txt')
        create_language_profile('en.txt')
        compare_profiles('en.txt')
        detect_language('en.txt')
        compare_profiles_advanced('en.txt')
        detect_language_advanced('en.txt')




    with open(os.path.join(PATH_TO_TEXTS_FOLDER, 'de.txt'), 'r', encoding='utf-8') as file_to_read:
        de_text = file_to_read.read()
        tokenize('de.txt')
        remove_stop_words('de.txt')
        calculate_frequencies('de.txt')
        get_top_n_words('de.txt')
        create_language_profile('de.txt')
        compare_profiles('de.txt')
        detect_language('de.txt')
        compare_profiles_advanced('de.txt')
        detect_language_advanced('de.txt')

    with open(os.path.join(PATH_TO_TEXTS_FOLDER, 'unknown.txt'), 'r', encoding='utf-8') as \
            file_to_read:
        unknown_text = file_to_read.read()
        tokenize('unknown.txt')
        remove_stop_words('unknown.txt')
        calculate_frequencies('unknown.txt')
        get_top_n_words('unknown.txt')
        create_language_profile('unknown.txt')
        compare_profiles('unknown.txt')
        detect_language('unknown.txt')
        compare_profiles_advanced('unknown.txt')
        detect_language_advanced('unknown.txt')

    with open(os.path.join(PATH_TO_TEXTS_FOLDER, 'la.txt'), 'r', encoding='utf-8') as file_to_read:
        unknown_text = file_to_read.read()
        tokenize('la.txt')
        remove_stop_words('la.txt')
        calculate_frequencies('la.txt')
        get_top_n_words('la.txt')
        create_language_profile('la.txt')
        compare_profiles('la.txt')
        detect_language('la.txt')
        compare_profiles_advanced('la.txt')
        detect_language_advanced('la.txt')

    EXPECTED = 'en'
    RESULT = ''
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT, 'Detection not working'
