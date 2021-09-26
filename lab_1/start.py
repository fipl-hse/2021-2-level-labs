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
    TOP_N = 6

    unknown_profile = main.create_language_profile('unk', unknown_text, [])

    # detect_language_external_profiles
    en_profile_external = main.load_profile(os.path.join(PATH_TO_PROFILES_FOLDER, 'en.json'))
    la_profile_external = main.load_profile(os.path.join(PATH_TO_PROFILES_FOLDER, 'la.json'))
    de_profile_external = main.load_profile(os.path.join(PATH_TO_PROFILES_FOLDER, 'de.json'))
    compare_profiles_external = [en_profile_external, la_profile_external, de_profile_external]
    RESULT_EXTERNAL = main.detect_language_advanced(unknown_profile,
                                                    compare_profiles_external,
                                                    [],
                                                    TOP_N)

    # detect_language_internal_profiles
    en_profile_internal = main.create_language_profile('en', en_text, [])
    la_profile_internal = main.create_language_profile('la', la_text, [])
    de_profile_internal = main.create_language_profile('de', de_text, [])
    compare_profiles_internal = [en_profile_internal, la_profile_internal, de_profile_internal]
    RESULT_INTERNAL = main.detect_language_advanced(unknown_profile,
                                                    compare_profiles_internal,
                                                    [],
                                                    TOP_N)

    # verification
    if RESULT_EXTERNAL == RESULT_INTERNAL:
        RESULT = RESULT_EXTERNAL
        print('RESULT: ', RESULT)
    else:
        print('The code is not working')

    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT, 'Detection not working'
