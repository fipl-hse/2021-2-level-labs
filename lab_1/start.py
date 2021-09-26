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

    with open(os.path.join(PATH_TO_TEXTS_FOLDER, 'unknown.txt'), 'r', encoding='utf-8') as \
            file_to_read:
        unknown_text = file_to_read.read()

    en_profile = main.load_profile(os.path.join(PATH_TO_LAB_FOLDER, r'profiles/en.json'))
    de_profile = main.load_profile(os.path.join(PATH_TO_LAB_FOLDER, r'profiles/de.json'))
    la_profile = main.load_profile(os.path.join(PATH_TO_LAB_FOLDER, r'profiles/la.json'))
    profiles = [en_profile, de_profile, la_profile]

    unknown_profile = main.create_language_profile('unk', unknown_text, [])
    detection = main.detect_language_advanced(unknown_profile, profiles, [], 7)

    print('The text language is', detection)
    main.save_profile(unknown_profile)

    EXPECTED = 'en'
    RESULT = detection
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT == EXPECTED, 'Detection not working'
