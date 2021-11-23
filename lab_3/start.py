"""
Language detection starter
"""

import os
from lab_3 import main

PATH_TO_LAB_FOLDER = os.path.dirname(os.path.abspath(__file__))

if __name__ == '__main__':
    ENG_SAMPLE = "Helium is the byproduct of millennia of radioactive decay from the elements thorium and uranium."
    GERMAN_SAMPLE = "Zwei Begriffe, die nicht unbedingt zueinander passen, am Arbeitsplatz schon mal gar nicht."
    UNKNOWN_SAMPLE = "Helium is material."
    SECRET_SAMPLE = """ Некој е болен и тој не е слободен. Dлетува гол во дупка од мраз. 
    И пее, а плаче од болка. Дали е ова контраст, можеби – живот?"""

    # score 6, params: k = 5, trie_level = 2
    # predict UNKNOWN_SAMPLE
    # print(calculate_distance(unknown_profile, en_profile, 5, 2))
    # print(calculate_distance(unknown_profile, de_profile, 5, 2))
    EXPECTED_DISTANCE_TO_EN_DE_PROFILES = 17, 25

    tokenize_unknown_sample = main.tokenize_by_sentence(UNKNOWN_SAMPLE)
    tokenize_en_sample = main.tokenize_by_sentence(ENG_SAMPLE)
    tokenize_de_sample = main.tokenize_by_sentence(GERMAN_SAMPLE)

    storage = main.LetterStorage()
    storage.update(tokenize_unknown_sample)
    storage.update(tokenize_en_sample)
    storage.update(tokenize_de_sample)

    unknown_encoded_corpus = main.encode_corpus(storage, tokenize_unknown_sample)
    en_encoded_corpus = main.encode_corpus(storage, tokenize_en_sample)
    de_encoded_corpus = main.encode_corpus(storage, tokenize_de_sample)

    unknown_profile = main.LanguageProfile(storage, 'unknown')
    en_profile = main.LanguageProfile(storage, 'en')
    de_profile = main.LanguageProfile(storage, 'de')

    unknown_profile.create_from_tokens(unknown_encoded_corpus, (2,))
    en_profile.create_from_tokens(en_encoded_corpus, (2,))
    de_profile.create_from_tokens(de_encoded_corpus, (2,))

    distance_en = main.calculate_distance(unknown_profile, en_profile, 5, 2)
    distance_de = main.calculate_distance(unknown_profile, de_profile, 5, 2)

    RESULT = (distance_en, distance_de)
    print(RESULT)
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT, 'Detection not working'
