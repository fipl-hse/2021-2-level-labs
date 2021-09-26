"""
Language detection starter
"""

import os
import main

PATH_TO_LAB_FOLDER = os.path.dirname(os.path.abspath(__file__))
PATH_TO_TEXTS_FOLDER = os.path.join(PATH_TO_LAB_FOLDER, 'texts')
PATH_TO_PROFILES_FOLDER = os.path.join(PATH_TO_LAB_FOLDER, 'profiles')

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
    TOP_N = 7
    profile_en = main.load_profile(os.path.join(PATH_TO_PROFILES_FOLDER, 'en.json'))
    profile_de = main.load_profile(os.path.join(PATH_TO_PROFILES_FOLDER, 'de.json'))
    profile_la = main.load_profile(os.path.join(PATH_TO_PROFILES_FOLDER, 'la.json'))
    profiles = [profile_en, profile_de, profile_la]
    unknown_profile = main.create_language_profile('unknown_text', unknown_text, [])
    RESULT_10 = main.detect_language_advanced(unknown_profile, profiles, [], TOP_N)

    main.save_profile(unknown_profile)

    profile_en = main.create_language_profile("en", en_text, [])
    profile_de = main.create_language_profile("de", de_text, [])
    profile_la = main.create_language_profile("la", la_text, [])
    RESULT_8 = main.detect_language_advanced(unknown_profile, profiles, [], TOP_N)
    if RESULT_10 == RESULT_8:
        print("Great")
        print(RESULT_10, RESULT_8)
    else:
        print("Wrong")
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    # assert RESULT, 'Detection not working'
    # assert EXPECTED == RESULT, 'Detection not working'
