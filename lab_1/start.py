"""
Language detection starter
"""

import os

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

    EXPECTED = 'en'
    RESULT = ''

    import main

    stop_words_en = ['a', 'an', 'the', 'and']
    stop_words_de = ['der', 'das', 'die', 'ein', 'eine']

    en_profile = main.create_language_profile('en', en_text, stop_words_en)
    de_profile = main.create_language_profile('de', de_text, stop_words_de)
    unknown_profile = main.create_language_profile('unknown language', unknown_text, [])

    print(main.compare_profiles(unknown_profile, en_profile, 10))
    print(main.detect_language(unknown_profile, de_profile, en_profile, 10))


    #DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT, 'Detection not working'

