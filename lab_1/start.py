"""
Language detection starter
"""

import os
import main

PATH_TO_LAB_FOLDER = os.path.dirname(os.path.abspath(__file__))
PATH_TO_TEXTS_FOLDER = os.path.join(PATH_TO_LAB_FOLDER, 'texts')
PATH_TO_PROFILE_FOLDER = os.path.join(PATH_TO_LAB_FOLDER,'profiles')

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

    en_profile = main.create_language_profile('en', en_text, [])
    de_profile = main.create_language_profile('de', de_text, [])
    la_profile = main.create_language_profile('la', la_text, [])
    unknown_profile = main.create_language_profile('unk', unknown_text, [])

    EXPECTED = 'en'

    de_and_la_result = main.detect_language_advanced(unknown_profile,[de_profile,la_profile],[],4)
    print(de_and_la_result)

    all_profiles = [de_profile,en_profile,la_profile]
    new_all_profiles = [main.load_profile(os.path.join(PATH_TO_PROFILE_FOLDER,'de.json')),
                main.load_profile(os.path.join(PATH_TO_PROFILE_FOLDER,'en.json')),
                main.load_profile(os.path.join(PATH_TO_PROFILE_FOLDER,'la.json'))]
    all_profiles_result = main.detect_language_advanced(unknown_profile,all_profiles,[],4)
    new_all_profiles_result = main.detect_language_advanced(unknown_profile,new_all_profiles,[],4)
    print(all_profiles_result)
    print(new_all_profiles_result)

    RESULT = new_all_profiles_result
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT, 'Detection not working'
