"""
Language detection starter
"""

import os
import random
from main import create_language_profile, detect_language, detect_language_advanced

PATH_TO_LAB_FOLDER = os.path.dirname(os.path.abspath(__file__))
PATH_TO_TEXTS_FOLDER = os.path.join(PATH_TO_LAB_FOLDER, 'texts')

if __name__ == '__main__':
    with open(os.path.join(PATH_TO_TEXTS_FOLDER, 'en.txt'), 'r', encoding='utf-8') as file_to_read:
        en_text = file_to_read.read()

    with open(os.path.join(PATH_TO_TEXTS_FOLDER, 'de.txt'), 'r', encoding='utf-8') as file_to_read:
        de_text = file_to_read.read()

    with open(os.path.join(PATH_TO_TEXTS_FOLDER, 'la.txt'), 'r', encoding='utf-8') as \
            file_to_read:
        la_text = file_to_read.read()

    with open(os.path.join(PATH_TO_TEXTS_FOLDER, 'unknown.txt'), 'r', encoding='utf-8') as \
            file_to_read:
        unknown_text = file_to_read.read()

    unknown = create_language_profile("unk", unknown_text, [])

    english = create_language_profile("en", en_text, [])
    german = create_language_profile("de", de_text, [])
    latin = create_language_profile("la", la_text, [])

    all_languages = [english, german, latin]

    TOP_N = 5

    RESULT = detect_language(unknown, english, german, TOP_N)
    print("Between English and German, unknown language is closer to profile called", RESULT)

    RESULT_ADV = detect_language_advanced(unknown, all_languages, [german, latin], TOP_N)
    print("Between Latin and German, unknown language is closer to", RESULT_ADV)

    EXPECTED = 'en'
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT, 'Detection not working'
