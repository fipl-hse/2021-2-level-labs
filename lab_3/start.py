"""
Language detection starter
"""

import os
from lab_3.main import LanguageProfile, LetterStorage, \
    tokenize_by_sentence, encode_corpus, calculate_distance

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
    en_tuple = tokenize_by_sentence(ENG_SAMPLE)
    de_tuple = tokenize_by_sentence(GERMAN_SAMPLE)
    un_tuple = tokenize_by_sentence(UNKNOWN_SAMPLE)

    storage = LetterStorage()
    storage.update(en_tuple)
    storage.update(de_tuple)
    storage.update(un_tuple)

    un_encoded = encode_corpus(storage, un_tuple)
    en_encoded = encode_corpus(storage, en_tuple)
    de_encoded = encode_corpus(storage, de_tuple)

    un_profile = LanguageProfile(storage, 'unknown')
    en_profile = LanguageProfile(storage, 'en')
    de_profile = LanguageProfile(storage, 'de')

    un_profile.create_from_tokens(un_encoded, (2,))
    en_profile.create_from_tokens(en_encoded, (2,))
    de_profile.create_from_tokens(de_encoded, (2,))

    distance_un_en = calculate_distance(un_profile, en_profile, 5, 2)
    distance_un_de = calculate_distance(un_profile, en_profile, 5, 2)

    print(distance_un_en)
    print(distance_un_de)

    # score 8, k = 5, trie_level = 3
    # predict UNKNOWN_SAMPLE
    # print(detector.detect(profile_unk, 5, 3))
    # EXPECTED_SCORE = {'en': 24, 'de': 25}

    # score 10, k = 1000, trie_levels = (2,)
    # predict SECRET_SAMPLE
    # print(detector.detect(unknown_profile, 1000, (2,)))
    # EXPECTED_LANGUAGE = ?
    # EXPECTED_MIN_DISTANCE = ?

    RESULT = distance_un_en, distance_un_de
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT, 'Detection not working'

