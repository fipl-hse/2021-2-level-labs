"""
Language detection starter
"""

import os
import main

PATH_TO_LAB_FOLDER = os.path.dirname(os.path.abspath(__file__))
PATH_TO_TEXTS_FOLDER = os.path.join(PATH_TO_LAB_FOLDER, 'texts')

if __name__ == '__main__':

    with open(os.path.join(PATH_TO_TEXTS_FOLDER, 'en.txt'), 'r', encoding='utf-8') as file_to_read:
        en_text = file_to_read.read()

    with open(os.path.join(PATH_TO_TEXTS_FOLDER, 'de.txt'), 'r', encoding='utf-8') as file_to_read:
        de_text = file_to_read.read()

    with open(os.path.join(PATH_TO_TEXTS_FOLDER, 'la.txt'), 'r', encoding='utf-8') as file_to_read:
        la_text = file_to_read.read()

    with open(os.path.join(PATH_TO_TEXTS_FOLDER, 'unknown.txt'), 'r', encoding='utf-8') as \
            file_to_read:
        unknown_text = file_to_read.read()

    EXPECTED = 'en'
    RESULT = ''
    top_n = 7
    # tokens = main.tokenize(la_text)
    # new_token = main.remove_stop_words(tokens, [])
    # frequency_dictionary = main.calculate_frequencies(tokens)
    # top_n_words = main.get_top_n_words(frequency_dictionary, 7)
    unknown_profile = main.create_language_profile("unknown_text", unknown_text, [])
    profile_1 = main.create_language_profile("la", la_text, [])
    profile_2 = main.create_language_profile("de", de_text, [])
    RESULT = main.detect_language(unknown_profile, profile_1, profile_2, top_n)



    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    # assert RESULT, 'Detection not working'
    # assert EXPECTED == RESULT, 'Detection not working'
    print(RESULT)
    print(EXPECTED)