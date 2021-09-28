"""
Language detection starter
"""

import os
from main import tokenize
from main import remove_stop_words
from main import get_top_n_words
from main import calculate_frequencies
from main import create_language_profile
from main import compare_profiles
from main import detect_language
from main import compare_profiles_advanced
from main import detect_language_advanced

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
    EXPECTED = 'en'
    RESULT = 'en'
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
en_tokens = tokenize(en_text)
en_stop_words = ['the', 'a', 'an', 'are', 'is', 'am']
de_stop_words = ['ich', 'du', 'bin', 'hast']
la_stop_words = ['cum', 'et', 'multa', 'hic']
print('tokenize:', en_tokens)
en_tokens_norm = remove_stop_words(en_tokens, en_stop_words)
print('remove_stop_words:', en_tokens_norm)
freq_dict = calculate_frequencies(en_tokens_norm)
top_n = 10
print('calculate_frequencies:', freq_dict)
print('get_top_n_words:', get_top_n_words(freq_dict, top_n))
en_profile = create_language_profile('en', en_text, en_stop_words)
print('create_language_profile:', en_profile)
de_profile = create_language_profile('de', de_text, de_stop_words)
la_profile = create_language_profile('la', la_text, la_stop_words)
unk_profile = create_language_profile('unknown', unknown_text, [])
print('compare_profiles:', compare_profiles(unk_profile, en_profile, top_n))
print('detect_language:', detect_language(unk_profile, de_profile, en_profile, top_n))
print('compare_profiles_advanced:', compare_profiles_advanced(unk_profile, en_profile, top_n))
profiles = [de_profile, la_profile, en_profile]
print('detect_languages_advanced:', detect_language_advanced(unk_profile, profiles, [], top_n))
assert RESULT, 'Detection not working'
