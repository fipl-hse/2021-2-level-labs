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


    print(main.tokenize(en_text))
    print(main.tokenize(de_text))
    print(main.tokenize(unknown_text))

    print()


    tokens_en = main.tokenize(en_text)
    tokens_de = main.tokenize(de_text)
    tokens_unknown = main.tokenize(unknown_text)

    stop_words_en = ['a', 'an', 'the', 'and']
    stop_words_de = ['der', 'das', 'die', 'ein', 'eine']
    stop_words_unknown = []

    print(main.remove_stop_words(tokens_en, stop_words_en))
    print(main.remove_stop_words(tokens_de, stop_words_de))
    print(main.remove_stop_words(tokens_unknown, stop_words_unknown))

    print()


    freq_dict_en = main.calculate_frequencies(tokens_en)
    freq_dict_de = main.calculate_frequencies(tokens_de)
    freq_dict_unknown = main.calculate_frequencies(tokens_unknown)

    print(main.calculate_frequencies(tokens_en))
    print(main.calculate_frequencies(tokens_de))
    print(main.calculate_frequencies(tokens_unknown))

    print()


    new_dicts_en = {v: k for k, v in freq_dict_en.items()}
    new_dicts_de = {v: k for k, v in freq_dict_de.items()}
    new_dicts_unknown = {v: k for k, v in freq_dict_unknown.items()}

    top_n_en = len(new_dicts_en)
    top_n_de = len(new_dicts_de)
    top_n_unknown = len(new_dicts_unknown)

    print(main.get_top_n_words(freq_dict_en, top_n_en))
    print(main.get_top_n_words(freq_dict_de, top_n_de))
    print(main.get_top_n_words(freq_dict_unknown, top_n_unknown))

    print()


    en_stop_words = main.remove_stop_words(tokens_en, stop_words_en)
    de_stop_words = main.remove_stop_words(tokens_de, stop_words_de)
    unknown_stop_words = main.remove_stop_words(tokens_unknown, stop_words_unknown)

    freq_dict_en = main.calculate_frequencies(main.remove_stop_words(main.tokenize(en_text), en_stop_words))
    freq_dict_de = main.calculate_frequencies(main.remove_stop_words(main.tokenize(de_text), de_stop_words))
    freq_dict_unknown = main.calculate_frequencies(main.remove_stop_words(main.tokenize(unknown_text), unknown_stop_words))


    print(main.create_language_profile('en', en_text, en_stop_words))
    print(main.create_language_profile('de', de_text, de_stop_words))
    print(main.create_language_profile('unknown', unknown_text, unknown_stop_words))

    print()


    en_profile = main.create_language_profile('en', en_text, en_stop_words)
    de_profile = main.create_language_profile('de', de_text, de_stop_words)
    unknown_profile = main.create_language_profile('unknown', unknown_text, unknown_stop_words)

    print(main.compare_profiles(unknown_profile, en_profile, top_n_en))
    print(main.compare_profiles(unknown_profile, de_profile, top_n_de))

    print()

    top_n_en = len(main.get_top_n_words(freq_dict_en, top_n_en))
    top_n_de = len(main.get_top_n_words(freq_dict_de, top_n_de))
    top_n_unknown = len(main.get_top_n_words(freq_dict_unknown, top_n_unknown))

    print(main.detect_language(unknown_profile, en_profile, de_profile, top_n_unknown))


    #DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT, 'Detection not working'

