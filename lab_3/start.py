"""
Language detection starter
"""

import os
import lab_3.main

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

    tokenize_unknown_sample = lab_3.main.tokenize_by_sentence(UNKNOWN_SAMPLE)
    tokenize_eng_sample = lab_3.main.tokenize_by_sentence(ENG_SAMPLE)
    tokenize_de_sample = lab_3.main.tokenize_by_sentence(GERMAN_SAMPLE)

    storage = lab_3.main.LetterStorage()
    storage.update(tokenize_unknown_sample)
    storage.update(tokenize_eng_sample)
    storage.update(tokenize_de_sample)

    unk_enc = lab_3.main.encode_corpus(storage, tokenize_unknown_sample)
    eng_enc = lab_3.main.encode_corpus(storage, tokenize_eng_sample)
    de_enc = lab_3.main.encode_corpus(storage, tokenize_de_sample)

    unknown_profile = lab_3.main.LanguageProfile(storage, 'unk')
    eng_profile = lab_3.main.LanguageProfile(storage, 'en')
    de_profile = lab_3.main.LanguageProfile(storage, 'de')

    unknown_profile.create_from_tokens(unk_enc, (2,))
    eng_profile.create_from_tokens(eng_enc, (2,))
    de_profile.create_from_tokens(de_enc, (2,))

    distance_unk_eng = lab_3.main.calculate_distance(unknown_profile, eng_profile, 5, 2)
    distance_unk_de = lab_3.main.calculate_distance(unknown_profile, de_profile, 5, 2)

    print(distance_unk_eng)
    print(distance_unk_de)

    # score 8, k = 5, trie_level = 3
    # predict UNKNOWN_SAMPLE
    # print(detector.detect(profile_unk, 5, 3))
    # EXPECTED_SCORE = {'en': 24, 'de': 25}

    # score 10, k = 1000, trie_levels = (2,)
    # predict SECRET_SAMPLE
    # print(detector.detect(unknown_profile, 1000, (2,)))
    # EXPECTED_LANGUAGE = ?
    # EXPECTED_MIN_DISTANCE = ?

    RESULT = distance_unk_eng, distance_unk_de
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT, 'Detection not working'

