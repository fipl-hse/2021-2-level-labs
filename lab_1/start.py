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

    from main import tokenize, remove_stop_words, calculate_frequencies, get_top_n_words, \
    create_language_profile, compare_profiles, detect_language, tokens_en, stop_words_en, \
    tokens_de, stop_words_de, tokens_unknown, stop_words_unknown, freq_dict_en, top_n_en, \
    freq_dict_de, top_n_de, freq_dict_unknown, top_n_unknown, language_en, language_de, \
    language_unknown, unknown_profile, en_profile, de_profile, en_stop_words, de_stop_words, \
    unknown_stop_words



    print(tokenize(en_text))
    print(tokenize(de_text))
    print(tokenize(unknown_text))

    print()

    print(remove_stop_words(tokens_en, stop_words_en))
    print(remove_stop_words(tokens_de, stop_words_de))
    print(remove_stop_words(tokens_unknown, stop_words_unknown))

    print()

    print(calculate_frequencies(tokens_en))
    print(calculate_frequencies(tokens_de))
    print(calculate_frequencies(tokens_unknown))

    print()

    print(get_top_n_words(freq_dict_en, top_n_en))
    print(get_top_n_words(freq_dict_de, top_n_de))
    print(get_top_n_words(freq_dict_unknown, top_n_unknown))

    print()

    print(create_language_profile(language_en, en_text, en_stop_words))
    print(create_language_profile(language_de, de_text, de_stop_words))
    print(create_language_profile(language_unknown, unknown_text, unknown_stop_words))

    print()

    print(compare_profiles(unknown_profile, en_profile, top_n_en))
    print(compare_profiles(unknown_profile, de_profile, top_n_de))

    print()

    print(detect_language(unknown_profile, en_profile, de_profile, top_n_unknown))

    #DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT, 'Detection not working'

