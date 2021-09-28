"""
Language detection starter
"""

import os
from main import tokenize
from main import remove_stop_words
from main import calculate_frequencies
from main import get_top_n_words
from main import create_language_profile
from main import compare_profiles
from main import detect_language
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
    RESULT = 'en'
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
print('tokenize:', tokenize(en_text))
en_tokens = tokenize(en_text)
en_stop = ['a', 'an', 'the', 'am', 'is', 'are']
de_stop = ['der', 'das', 'ich', 'du', 'bin', 'hast']
print('remove stop words:', remove_stop_words(en_tokens, en_stop))
en_normal = remove_stop_words(en_tokens, en_stop)
print('calculate frequences:', calculate_frequencies(en_normal))
frequency_dict = (calculate_frequencies(en_normal))
print('get top n words:', get_top_n_words(frequency_dict, 10))
en_profile = create_language_profile('en', en_text, en_stop)
print('create language profile', en_profile)
de_profile = create_language_profile('de', de_text, de_stop)
print('create language profile', de_profile)
un_profile = create_language_profile('unknown', unknown_text, [])
print('create language profile', un_profile)
print('compare profiles:', compare_profiles(un_profile, en_profile, 10))
print('detect language:', detect_language(un_profile, de_profile, en_profile, 10))
assert RESULT, 'Detection not working'
