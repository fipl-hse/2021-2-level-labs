"""
Language detection starter
"""

import os
from lab_3.main import tokenize_by_sentence, LetterStorage, encode_corpus, \
    LanguageProfile, calculate_distance, LanguageDetector

PATH_TO_LAB_FOLDER = os.path.dirname(os.path.abspath(__file__))

if __name__ == '__main__':
    ENG_SAMPLE = "Helium is the byproduct of millennia of " \
                 "radioactive decay from the elements thorium and uranium."
    GERMAN_SAMPLE = "Zwei Begriffe, die nicht unbedingt " \
                    "zueinander passen, am Arbeitsplatz schon mal gar nicht."
    UNKNOWN_SAMPLE = "Helium is material."
    SECRET_SAMPLE = """ Некој е болен и тој не е слободен. Dлетува гол во дупка од мраз.
    И пее, а плаче од болка. Дали е ова контраст, можеби – живот?"""

    # score 6, params: k = 5, trie_level = 2
    # predict UNKNOWN_SAMPLE
    # print(calculate_distance(unknown_profile, en_profile, 5, 2))
    # print(calculate_distance(unknown_profile, de_profile, 5, 2))

    tokenize_unknown_sample = tokenize_by_sentence(UNKNOWN_SAMPLE)
    tokenize_eng_sample = tokenize_by_sentence(ENG_SAMPLE)
    tokenize_de_sample = tokenize_by_sentence(GERMAN_SAMPLE)

    storage = LetterStorage()
    storage.update(tokenize_unknown_sample)
    storage.update(tokenize_eng_sample)
    storage.update(tokenize_de_sample)

    unk_enc = encode_corpus(storage, tokenize_unknown_sample)
    eng_enc = encode_corpus(storage, tokenize_eng_sample)
    de_enc = encode_corpus(storage, tokenize_de_sample)

    unknown_profile_6 = LanguageProfile(storage, 'unk')
    eng_profile_6 = LanguageProfile(storage, 'en')
    de_profile_6 = LanguageProfile(storage, 'de')

    unknown_profile_6.create_from_tokens(unk_enc, (2,))
    eng_profile_6.create_from_tokens(eng_enc, (2,))
    de_profile_6.create_from_tokens(de_enc, (2,))

    distance_unk_eng = calculate_distance(unknown_profile_6, eng_profile_6, 5, 2)
    distance_unk_de = calculate_distance(unknown_profile_6, de_profile_6, 5, 2)

    EXPECTED_DISTANCE_TO_EN_DE_PROFILES = 17, 25
    RESULT_FOR_6 = distance_unk_eng, distance_unk_de
    print(RESULT_FOR_6)

    # score 8, k = 5, trie_level = 3
    # predict UNKNOWN_SAMPLE
    # print(detector.detect(profile_unk, 5, 3))
    # EXPECTED_SCORE = {'en': 24, 'de': 25}

    unknown_profile_8 = LanguageProfile(storage, 'unk')
    eng_profile_8 = LanguageProfile(storage, 'en')
    de_profile_8 = LanguageProfile(storage, 'de')

    unknown_profile_8.create_from_tokens(unk_enc, (3,))
    eng_profile_8.create_from_tokens(eng_enc, (3,))
    de_profile_8.create_from_tokens(de_enc, (3,))

    calculate_distance(unknown_profile_8, eng_profile_8, 5, 3)
    calculate_distance(unknown_profile_8, de_profile_8, 5, 3)

    unknown_profile_8.save('unknown_profile.json')
    profile_unk = LanguageProfile(storage, 'unk')
    profile_unk.open('unknown_profile.json')

    detector = LanguageDetector()

    detector.register_language(eng_profile_8)
    detector.register_language(de_profile_8)
    RESULT_FOR_8 = detector.detect(profile_unk, 5, (3,))
    EXPECTED_SCORE = {'en': 24, 'de': 25}
    print(RESULT_FOR_8)

    # score 10, k = 1000, trie_levels = (2,)
    # predict SECRET_SAMPLE
    # print(detector.detect(unknown_profile, 1000, (2,)))
    # EXPECTED_LANGUAGE = ?
    # EXPECTED_MIN_DISTANCE = ?

    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT_FOR_6 == EXPECTED_DISTANCE_TO_EN_DE_PROFILES, 'Detection not working'
    assert RESULT_FOR_8 == EXPECTED_SCORE, 'Detection not working'
