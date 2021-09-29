"""
Language detection starter
"""
from main import *
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

    with open(os.path.join(PATH_TO_TEXTS_FOLDER, 'la.txt'), 'r', encoding='utf-8') as \
            file_to_read:
        la_text = file_to_read.read()

    en_profile = create_language_profile('en', en_text, [])
    de_profile = create_language_profile('de', de_text, [])
    unknown_profile = create_language_profile('unknown', unknown_text,[])
    la_profile = create_language_profile('la', en_text, [])
    EXPECTED = 'en'
    RESULT = ''

    simple_detection = detect_language(unknown_profile, en_profile, de_profile, 3)
    print(simple_detection)


    profiles_list = [en_profile,de_profile,la_profile]
    languages = ['de','la']

    advanced_detection_all = detect_language_advanced(unknown_profile, profiles_list, languages, 3)
    print(advanced_detection_all)

    advanced_det_two = detect_language_advanced(unknown_profile, profiles_list, [], 3)
    print(advanced_det_two)


    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT, 'Detection not working'