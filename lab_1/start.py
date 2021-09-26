"""
Language detection starter
"""

import os
import main

PATH_TO_LAB_FOLDER = os.path.dirname(os.path.abspath(__file__))
PATH_TO_TEXTS_FOLDER = os.path.join(PATH_TO_LAB_FOLDER, 'texts')
PATH_TO_LANG_PROFILES = os.path.join(PATH_TO_LAB_FOLDER, 'profiles')

if __name__ == '__main__':

    with open(os.path.join(PATH_TO_TEXTS_FOLDER, 'en.txt'), 'r', encoding='utf-8') as file_to_read:
        en_text = file_to_read.read()

    with open(os.path.join(PATH_TO_TEXTS_FOLDER, 'de.txt'), 'r', encoding='utf-8') as file_to_read:
        de_text = file_to_read.read()

    with open(os.path.join(PATH_TO_TEXTS_FOLDER, 'la.txt'), 'r', encoding='utf-8') as file_to_read:
        la_text = file_to_read.read()

    with open(os.path.join(PATH_TO_TEXTS_FOLDER, 'unknown.txt'), 'r', encoding='utf-8') as file_to_read:
        unknown_text = file_to_read.read()

    unk_profile = main.create_language_profile("unk", unknown_text, [])
    #detection from my profiles
    profile_en = main.create_language_profile("en", en_text, [])
    profile_de = main.create_language_profile("de", de_text, [])
    profile_la = main.create_language_profile("la", la_text, [])
    profiles_my = [profile_en, profile_de, profile_la]
    det_from_my_profiles = main.detect_language_advanced(unknown_profile, profiles_my, [], 5)

    #detection from external profiles
    en_profile = main.load_profile(os.path.join(PATH_TO_LANG_PROFILES, "en.json"))
    de_profile = main.load_profile(os.path.join(PATH_TO_LANG_PROFILES, "en.json"))
    la_profile = main.load_profile(os.path.join(PATH_TO_LANG_PROFILES, "la.json"))
    profiles_extrnl = [en_profile, de_profile, la_profile]
    det_from_extrnl_profiles = main.detect_language_advanced(unknown_profile, profiles_extrnl, [], 5)

    print('According to detection from my profiles, it\'s probably', det_from_my_profiles)
    print('According to detection from external profiles, it\'s probably', det_from_extrnl_profiles)

    EXPECTED = 'en'
    RESULT = ''
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT, 'Detection not working'
