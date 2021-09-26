"""
Language detection starter
"""

import os
import main

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

    EXPECTED = 'en'
    RESULT = ''

    unknown_profile = main.create_language_profile('unknown', unknown_text, [])

    # Create profiles from text
    # en_profile = main.create_language_profile('en', en_text, [])
    # de_profile = main.create_language_profile('de', de_text, [])
    # la_profile = main.create_language_profile('la', la_text, [])

    # Or load profiles from json
    en_profile = main.load_profile(os.path.join(PATH_TO_PROFILES_FOLDER, 'en.json'))
    de_profile = main.load_profile(os.path.join(PATH_TO_PROFILES_FOLDER, 'de.json'))
    la_profile = main.load_profile(os.path.join(PATH_TO_PROFILES_FOLDER, 'la.json'))

    # You may save profiles as json
    # main.save_profile(en_profile)
    # main_save_profile(de_profile)
    # main.save_profile(la_profile)

    profiles = [en_profile, de_profile, la_profile]
    
    RESULT = main.detect_language_advanced(unknown_profile, profiles, [], 5)

    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert EXPECTED == RESULT, 'Detection not working'
