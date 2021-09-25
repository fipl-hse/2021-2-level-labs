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

        import main

        en = main.load_profile(os.path.join(PATH_TO_LAB_FOLDER, r"profiles\en.json"))
        de = main.load_profile(os.path.join(PATH_TO_LAB_FOLDER, r"profiles\de.json"))
        la = main.load_profile(os.path.join(PATH_TO_LAB_FOLDER, r"profiles\la.json"))
        new_profile = main.create_language_profile("unk", unknown_text, [])
        interesting = main.compare_profiles_advanced(new_profile, en, 5)
        print(interesting)
        result = main.detect_language_advanced(new_profile, [en, de, la], [], 5)
        print(result)

    with open(os.path.join(PATH_TO_TEXTS_FOLDER, "la.txt"), "r", encoding="utf-8") as file_to_read:
        la_text = file_to_read.read()

    EXPECTED = 'en'
    RESULT = ''
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT, 'Detection not working'
