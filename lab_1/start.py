"""
Language detection starter
"""

import os
from lab_1.main import create_language_profile, detect_language_advanced

PATH_TO_LAB_FOLDER = os.path.dirname(os.path.abspath(__file__))
PATH_TO_TEXTS_FOLDER = os.path.join(PATH_TO_LAB_FOLDER, 'texts')

if __name__ == '__main__':

    with open(os.path.join(PATH_TO_TEXTS_FOLDER, 'en.txt'), 'r', encoding='utf-8') as \
            file_to_read_en:
        en_text = file_to_read_en.read()

    with open(os.path.join(PATH_TO_TEXTS_FOLDER, 'de.txt'), 'r', encoding='utf-8') as \
            file_to_read_de:
        de_text = file_to_read_de.read()

    with open(os.path.join(PATH_TO_TEXTS_FOLDER, 'la.txt'), 'r', encoding='utf-8') as \
            file_to_read:
        la_text = file_to_read.read()

    with open(os.path.join(PATH_TO_TEXTS_FOLDER, 'unknown.txt'), 'r', encoding='utf-8') as \
            file_to_read_unk:
        unknown_text = file_to_read_unk.read()

    EXPECTED = 'en'
    RESULT = ''
    unknown_profile = create_language_profile('unknown', unknown_text, [])

    profile_en = create_language_profile("en", en_text, [])
    profile_de = create_language_profile("de", de_text, [])
    profile_la = create_language_profile("la", la_text, [])
    profiles = [profile_en, profile_de, profile_la]
    result = detect_language_advanced(unknown_profile, profiles, [], 5)

    if result == EXPECTED:
        RESULT = result

    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT, 'Detection not working'
