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
    unknown_profile = main.create_language_profile("unknown_text", unknown_text, [])
    profile_1 = main.create_language_profile("la", la_text, [])
    profile_2 = main.create_language_profile("de", de_text, [])
    profile_3 = main.create_language_profile("en", en_text, [])
    top_n = 7
    profiles = [profile_1, profile_2, profile_3]
    RESULT = main.detect_language_advanced(unknown_profile, profiles, [], top_n)



    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    #assert RESULT, 'Detection not working'
    assert EXPECTED == RESULT, 'Detection not working'
    #print(RESULT)
    #print(EXPECTED)