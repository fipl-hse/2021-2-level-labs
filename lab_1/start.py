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

    lang_unk = main.create_language_profile('unk', unknown_text, [])
    lang_en = main.create_language_profile('en', en_text, [])
    lang_de = main.create_language_profile('de', de_text, [])
    lang_la = main.create_language_profile('la', la_text, [])

    TOP_N = 4

    langs = [lang_en, lang_de, lang_la]

    det = main.detect_language(lang_unk, lang_en, lang_de, TOP_N)

    det_adv = main.detect_language_advanced(lang_unk, langs, [lang_la, lang_de], TOP_N)

    EXPECTED = 'en'
    RESULT = det
    print('basic result is', RESULT)
    RESULT_ADV = det_adv
    print('advanced result is',RESULT_ADV)
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT, 'Detection not working'
