"""
Language detection starter
"""

import os
from main import create_language_profile
from main import detect_language

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

    en_profile = create_language_profile('en', en_text, ['a', 'the', 'is'])
    print(en_profile)
    de_profile = create_language_profile('de', de_text, ['und', 'ich', 'du'])
    print(de_profile)
    unknown_profile = create_language_profile('unknown', unknown_text, [])
    print(unknown_profile)

    EXPECTED = 'en'
    RESULT = ''
    RESULT = detect_language(unknown_profile, en_profile, de_profile, 3)
    print(RESULT)
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT, 'Detection not working'
