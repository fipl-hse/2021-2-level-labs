"""
Language detection starter
"""

import os

from lab_1.main import create_language_profile, detect_language, detect_language_advanced, load_profile

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

<<<<<<< HEAD
    with open(os.path.join(PATH_TO_TEXTS_FOLDER, 'la.txt'), 'r', encoding='utf-8') as \
            file_to_read:
        la_text = file_to_read.read()
    unknown_profile = create_language_profile('unknown', unknown_text, [])
    en_profile = create_language_profile('en', en_text, [])
    de_profile = create_language_profile('de', de_text, [])
    la_profile = create_language_profile('la', la_text, [])
    all_profiles = [en_profile, de_profile, la_profile]
    name = detect_language_advanced(unknown_profile, all_profiles, [], 7)

    en_profile_json = load_profile(os.path.join(PATH_TO_PROFILES_FOLDER, 'en.json'))
    de_profile_json = load_profile(os.path.join(PATH_TO_PROFILES_FOLDER, 'de.json'))
    la_profile_json = load_profile(os.path.join(PATH_TO_PROFILES_FOLDER, 'la.json'))
    all_profiles_json = [en_profile_json, de_profile_json, la_profile_json]
    name_json = detect_language_advanced(unknown_profile, all_profiles_json, [], 7)
    if name == name_json:
        EXPECTED = 'en'
        RESULT = name

=======
    unknown_profile = create_language_profile ('unknown', unknown_text, [])
    en_profile = create_language_profile ('en', en_text, [])
    de_profile = create_language_profile ('de', de_text, [])
    name = detect_language(unknown_profile, en_profile, de_profile)

    EXPECTED = 'en'
    RESULT = ''
>>>>>>> 626fb8a2d89185f8664d4748ebe4aa9d261e7741

    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    # assert RESULT, 'Detection not working'
    assert EXPECTED == RESULT, 'Detection not working'
