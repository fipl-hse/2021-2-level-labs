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

    unk = main.create_language_profile('unk', unknown_text, [])
    de = main.create_language_profile("de", de_text, [])
    en = main.create_language_profile("en", en_text, [])
    la = main.create_language_profile("la", la_text, [])
    main.save_profile(unk)

    de_profile = main.load_profile(os.path.join(PATH_TO_LAB_FOLDER, r'profiles\de.json'))
    en_profile = main.load_profile(os.path.join(PATH_TO_LAB_FOLDER, r'profiles\en.json'))
    la_profile = main.load_profile(os.path.join(PATH_TO_LAB_FOLDER, r'profiles\la.json'))
    unk_profile = main.load_profile(os.path.join(PATH_TO_LAB_FOLDER, r'profiles\unk.json'))

    languages = ['en', 'de', 'la']
    profiles = [en_profile, de_profile, la_profile]
    RESULT = main.detect_language_advanced(unk_profile,profiles ,languages , 5)
    print(RESULT)
    RESULT1 = main.detect_language_advanced(unk, [en, de, la], languages, 5)
    '''Compare the results of language detection based on your and external(loaded) language profiles'''
    if RESULT1 == RESULT:
        EXPECTED = 'en'
        # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
        assert RESULT == EXPECTED, 'Detection not working'
