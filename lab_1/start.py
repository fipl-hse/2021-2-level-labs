"""
Language detection starter
"""

import os

from main import tokenize

from main import tokenize
from main import remove_stop_words
from main import calculate_frequencies
from main import get_top_n_words
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

    with open(os.path.join(PATH_TO_TEXTS_FOLDER, 'unknown.txt'), 'r', encoding='utf-8') as \
            file_to_read:
        unknown_text = file_to_read.read()

    with open(os.path.join(PATH_TO_TEXTS_FOLDER, 'la.txt'), 'r', encoding='utf-8') as \
            file_to_read:
        la_text = file_to_read.read()

    EXPECTED = 'en'
    RESULT = 'en'
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST

english_tokens = tokenize(en_text)
tokens_less_5 = []
for token in english_tokens:
    if len(token) < 5:
        tokens_less_5.append(token)
tokens_less_5 = sorted(tokens_less_5, reverse=True, key=len)
print(tokens_less_5)


en_tokens = tokenize(en_text)
print('tokenization:', tokenize(en_text))

en_stop_words = ['the', 'a', 'an']
de_stop_words = ['der', 'die', 'das']
la_stop_words = ['et', 'cum', 'hic', 'hoc', 'latin']

print('tokens without stop words: ', remove_stop_words(en_tokens, en_stop_words))
frequencies = remove_stop_words(en_tokens, en_stop_words)
print('frequencies dictionary: ', calculate_frequencies(frequencies))
freq_dict = calculate_frequencies(frequencies)
TOP_N = 5
print('top n words: ', get_top_n_words(freq_dict, TOP_N))
en_profile = create_language_profile('en', en_text, en_stop_words)
print('en profile: ', en_profile)
de_profile = create_language_profile('de', de_text, de_stop_words)
la_profile = create_language_profile('la', la_text, la_stop_words)
unknown_profile = create_language_profile('unknown', unknown_text, [])
print('compare profiles: ', compare_profiles(unknown_profile, en_profile, TOP_N))
print('detect language: ', detect_language(unknown_profile, en_profile, de_profile, TOP_N))
print('compare profile advanced: ', compare_profiles_advanced(unknown_profile, de_profile, TOP_N))
profiles = [en_profile, de_profile, la_profile]
print('detect_language_advanced: ', detect_language_advanced(unknown_profile, profiles, [], TOP_N))

assert RESULT, 'Detection not working'
