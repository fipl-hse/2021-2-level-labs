"""
Language detection starter
"""

import os
import main

PATH_TO_LAB_FOLDER = os.path.dirname(os.path.abspath(__file__))
PATH_TO_TEXTS_FOLDER = os.path.join(PATH_TO_LAB_FOLDER, 'texts')
PATH_TO_PROFILES = os.path.join(PATH_TO_LAB_FOLDER, 'profiles')

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

    top_n = 9
    unknown_profile = main.create_language_profile('unk', unknown_text, [])

    de_profile_1 = main.load_profile(os.path.join(PATH_TO_PROFILES, 'de.json'))
    en_profile_1 = main.load_profile(os.path.join(PATH_TO_PROFILES, 'en.json'))
    la_profile_1 = main.load_profile(os.path.join(PATH_TO_PROFILES, 'la.json'))
    profiles_1 = [de_profile_1, en_profile_1, la_profile_1]

    detection_1 = main.detect_language_advanced(unknown_profile, profiles_1, [], top_n)
    print('External detection result:', detection_1)

    de_profile_2 = main.create_language_profile('de', de_text, [])
    en_profile_2 = main.create_language_profile('en', en_text, [])
    la_profile_2 = main.create_language_profile('la', la_text, [])
    profiles_2 = [de_profile_2, en_profile_2, la_profile_2]

    detection_2 = main.detect_language_advanced(unknown_profile, profiles_2, [], top_n)
    print('Internal detection result:', detection_2)

    if detection_1 == detection_2:
        print('External result = internal result')
    else:
        print('Different results')

    main.save_profile(unknown_profile)

    EXPECTED = 'en'
    RESULT = ''
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT, 'Detection not working'
