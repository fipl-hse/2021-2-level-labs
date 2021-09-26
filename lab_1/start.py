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

    de_profile = main.load_profile(os.path.join(PATH_TO_LAB_FOLDER, r'profiles\de.json'))
    en_profile = main.load_profile(os.path.join(PATH_TO_LAB_FOLDER, r'profiles\en.json'))
    la_profile = main.load_profile(os.path.join(PATH_TO_LAB_FOLDER, r'profiles\la.json'))
    profiles = [de_profile, en_profile, la_profile]

    unknown_profile = main.create_language_profile('unk', unknown_text, [])
    comparison = main.compare_profiles_advanced(unknown_profile, en_profile, 3)
    detection = main.detect_language_advanced(unknown_profile, profiles, [], 3)

    print('Comparison result:', comparison)
    print('Detection result:', detection)

    EXPECTED = 'en'
    RESULT = ''
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT, 'Detection not working'
