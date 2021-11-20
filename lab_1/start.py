"""
Language detection starter
"""

import os
from lab_1.main import create_language_profile, load_profile, detect_language_advanced, save_profile

PATH_TO_LAB_FOLDER = os.path.dirname(os.path.abspath(__file__))
PATH_TO_TEXTS_FOLDER = os.path.join(PATH_TO_LAB_FOLDER, 'texts')
PATH_TO_PROFILES_FOLDER = os.path.join(PATH_TO_LAB_FOLDER, 'profiles')

if __name__ == '__main__':

    with open(os.path.join(PATH_TO_TEXTS_FOLDER, 'en.txt'), 'r', encoding='utf-8') as file_to_read_en:
        en_text = file_to_read_en.read()

    with open(os.path.join(PATH_TO_TEXTS_FOLDER, 'de.txt'), 'r', encoding='utf-8') as file_to_read_de:
        de_text = file_to_read_de.read()

    with open(os.path.join(PATH_TO_TEXTS_FOLDER, 'la.txt'), 'r', encoding='utf-8') as \
            file_to_read:
        la_text = file_to_read.read()

    with open(os.path.join(PATH_TO_TEXTS_FOLDER, 'unknown.txt'), 'r', encoding='utf-8') as \
            file_to_read_unk:
        unknown_text = file_to_read_unk.read()

    EXPECTED = 'en'
    RESULT = ''
    profile_en_json = load_profile(os.path.join(PATH_TO_PROFILES_FOLDER, 'en.json'))
    profile_de_json = load_profile(os.path.join(PATH_TO_PROFILES_FOLDER, 'de.json'))
    profile_la_json = load_profile(os.path.join(PATH_TO_PROFILES_FOLDER, 'la.json'))
    profiles_json = [profile_en_json, profile_de_json, profile_la_json]
    unknown_profile = create_language_profile('unknown', unknown_text, [])
    result_json = detect_language_advanced(unknown_profile, profiles_json, [], 5)
    save_profile(unknown_profile)

    profile_en = create_language_profile("en", en_text, [])
    profile_de = create_language_profile("de", de_text, [])
    profile_la = create_language_profile("la", la_text, [])
    profiles = [profile_en, profile_de, profile_la]
    result = detect_language_advanced(unknown_profile, profiles, [], 5)

    if result_json == result:
        EXPECTED = 'en'
        RESULT = result
    else:
        print(result)
        print(result_json)


    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT, 'Detection not working'