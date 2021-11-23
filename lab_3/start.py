"""
Language detection starter
"""

import os
from lab_3.main import tokenize_by_sentence, LetterStorage, encode_corpus, \
    LanguageProfile, calculate_distance

PATH_TO_LAB_FOLDER = os.path.dirname(os.path.abspath(__file__))

if __name__ == '__main__':
    ENG_SAMPLE = "Helium is the byproduct of millennia of radioactive decay from the elements thorium and uranium."
    GERMAN_SAMPLE = "Zwei Begriffe, die nicht unbedingt zueinander passen, am Arbeitsplatz schon mal gar nicht."
    UNKNOWN_SAMPLE = "Helium is material."
    SECRET_SAMPLE = """ Некој е болен и тој не е слободен. Dлетува гол во дупка од мраз. 
    И пее, а плаче од болка. Дали е ова контраст, можеби – живот?"""

    # score 6, params: k = 5, trie_level = 2
    # predict UNKNOWN_SAMPLE

    eng = tokenize_by_sentence(ENG_SAMPLE)
    ger = tokenize_by_sentence(GERMAN_SAMPLE)
    unk = tokenize_by_sentence(UNKNOWN_SAMPLE)

    unistorage = LetterStorage()
    unistorage.update(eng)
    unistorage.update(ger)
    unistorage.update(unk)

    encoded_eng = encode_corpus(unistorage, eng)
    encoded_ger = encode_corpus(unistorage, ger)
    encoded_unk = encode_corpus(unistorage, unk)

    profile_eng = LanguageProfile(letter_storage=unistorage, language_name='en')
    profile_eng.create_from_tokens(encoded_eng, (2,))

    profile_ger = LanguageProfile(letter_storage=unistorage, language_name='de')
    profile_ger.create_from_tokens(encoded_ger, (2,))

    profile_unk = LanguageProfile(letter_storage=unistorage, language_name='unk')
    profile_unk.create_from_tokens(encoded_unk, (2,))

    print(calculate_distance(profile_unk, profile_eng, 5, 2))
    print(calculate_distance(profile_unk, profile_ger, 5, 2))
    EXPECTED_DISTANCE_TO_EN_DE_PROFILES = 17, 25

    # score 8, k = 5, trie_level = 3
    # predict UNKNOWN_SAMPLE
    # print(detector.detect(profile_unk, 5, 3))
    # EXPECTED_SCORE = {'en': 24, 'de': 25}

    # score 10, k = 1000, trie_levels = (2,)
    # predict SECRET_SAMPLE
    # print(detector.detect(unknown_profile, 1000, (2,)))
    # EXPECTED_LANGUAGE = ?
    # EXPECTED_MIN_DISTANCE = ?

    RESULT = EXPECTED_DISTANCE_TO_EN_DE_PROFILES
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT, 'Detection not working'

