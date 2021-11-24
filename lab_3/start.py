"""
Language detection starter
"""

import os
from lab_3.main import LanguageProfile, LetterStorage, tokenize_by_sentence, encode_corpus, calculate_distance

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
    eng = tokenize_by_sentence(ENG_SAMPLE)
    de = tokenize_by_sentence(GERMAN_SAMPLE)
    unknown = tokenize_by_sentence(UNKNOWN_SAMPLE)

    storage = LetterStorage()
    storage.update(eng)
    storage.update(de)
    storage.update(unknown)

    eng_encoded = encode_corpus(storage, eng)
    de_encoded = encode_corpus(storage, de)
    unknown_encoded = encode_corpus(storage, unknown)

    eng_profile = LanguageProfile(storage, 'eng')
    de_profile = LanguageProfile(storage, 'de')
    unknown_profile = LanguageProfile(storage, 'unknown')

    eng_profile.create_from_tokens(eng_encoded, (5, 2))
    de_profile.create_from_tokens(de_encoded, (5, 2))
    unknown_profile.create_from_tokens(unknown_encoded, (5, 2))

    eng_unk_dist = calculate_distance(unknown_profile, eng_profile, 5, 2)
    de_unk_dist = calculate_distance(unknown_profile, de_profile, 5, 2)

    RESULT_FOR_6 = eng_unk_dist, de_unk_dist
    print(RESULT_FOR_6)






    # score 8, k = 5, trie_level = 3
    # predict UNKNOWN_SAMPLE
    # print(detector.detect(profile_unk, 5, 3))
    # EXPECTED_SCORE = {'en': 24, 'de': 25}

    # score 10, k = 1000, trie_levels = (2,)
    # predict SECRET_SAMPLE
    # print(detector.detect(unknown_profile, 1000, (2,)))
    # EXPECTED_LANGUAGE = ?
    # EXPECTED_MIN_DISTANCE = ?

    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT_FOR_6 == EXPECTED_DISTANCE_TO_EN_DE_PROFILES, 'Detection not working'
