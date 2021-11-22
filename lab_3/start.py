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

    TOKENIZED_ENG_SAMPLE = lab_3.main.tokenize_by_sentence(ENG_SAMPLE)
    TOKENIZED_DE_SAMPLE = lab_3.main.tokenize_by_sentence(GERMAN_SAMPLE)
    TOKENIZED_UNKNOWN_SAMPLE = lab_3.main.tokenize_by_sentence(UNKNOWN_SAMPLE)

    STORAGE = lab_3.main.LetterStorage()
    STORAGE.update(TOKENIZED_ENG_SAMPLE)
    STORAGE.update(TOKENIZED_DE_SAMPLE)
    STORAGE.update(TOKENIZED_UNKNOWN_SAMPLE)

    ENCODED_ENG = lab_3.main.encode_corpus(STORAGE, TOKENIZED_ENG_SAMPLE)
    ENCODED_DE = lab_3.main.encode_corpus(STORAGE, TOKENIZED_DE_SAMPLE)
    ENCODED_UNKNOWN = lab_3.main.encode_corpus(STORAGE, TOKENIZED_UNKNOWN_SAMPLE)

    PROFILE_ENG = lab_3.main.LanguageProfile(STORAGE, 'en')
    PROFILE_DE = lab_3.main.LanguageProfile(STORAGE, 'de')
    PROFILE_UNKNOWN = lab_3.main.LanguageProfile(STORAGE, 'unk')

    PROFILE_ENG.create_from_tokens(ENCODED_ENG, (2,))
    PROFILE_DE.create_from_tokens(ENCODED_DE, (2,))
    PROFILE_UNKNOWN.create_from_tokens(ENCODED_UNKNOWN, (2,))

    DISTANCE_ENG_UNK = lab_3.main.calculate_distance(PROFILE_UNKNOWN, PROFILE_ENG, 5, 2)
    DISTANCE_DE_UNK = lab_3.main.calculate_distance(PROFILE_UNKNOWN, PROFILE_DE, 5, 2)

    # print(DISTANCE_ENG_UNK)
    # print(DISTANCE_DE_UNK)

    # score 8, k = 5, trie_level = 3
    # predict UNKNOWN_SAMPLE
    # print(detector.detect(profile_unk, 5, 3))
    # EXPECTED_SCORE = {'en': 24, 'de': 25}

    # score 10, k = 1000, trie_levels = (2,)
    # predict SECRET_SAMPLE
    # print(detector.detect(unknown_profile, 1000, (2,)))
    # EXPECTED_LANGUAGE = ?
    # EXPECTED_MIN_DISTANCE = ?

    RESULT = DISTANCE_ENG_UNK, DISTANCE_DE_UNK
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert EXPECTED_DISTANCE_TO_EN_DE_PROFILES == RESULT, 'Detection not working'

