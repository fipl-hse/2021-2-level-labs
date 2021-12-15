"""
Language detection starter
"""

import os
import lab_3.main

PATH_TO_LAB_FOLDER = os.path.dirname(os.path.abspath(__file__))

if __name__ == '__main__':
    ENG_SAMPLE = """Helium is the byproduct of millennia of
     radioactive decay from the elements thorium and uranium."""
    GERMAN_SAMPLE = """Zwei Begriffe, die nicht unbedingt 
    zueinander passen, am Arbeitsplatz schon mal gar nicht."""
    UNKNOWN_SAMPLE = "Helium is material."
    SECRET_SAMPLE = """ Некој е болен и тој не е слободен. Dлетува гол во дупка од мраз. 
    И пее, а плаче од болка. Дали е ова контраст, можеби – живот?"""
    # score 6, params: k = 5, trie_level = 2
    # predict UNKNOWN_SAMPLE

    tokenize_eng = lab_3.main.tokenize_by_sentence(ENG_SAMPLE)
    tokenize_de = lab_3.main.tokenize_by_sentence(GERMAN_SAMPLE)
    tokenize_unk = lab_3.main.tokenize_by_sentence(UNKNOWN_SAMPLE)

    letter_storage = lab_3.main.LetterStorage()
    letter_storage.update(tokenize_unk)
    letter_storage.update(tokenize_de)
    letter_storage.update(tokenize_eng)

    encoded_eng = lab_3.main.encode_corpus(letter_storage, tokenize_eng)
    encoded_de = lab_3.main.encode_corpus(letter_storage, tokenize_de)
    encoded_unk = lab_3.main.encode_corpus(letter_storage, tokenize_unk)

    profile_eng = lab_3.main.LanguageProfile(letter_storage, "en")
    profile_de = lab_3.main.LanguageProfile(letter_storage, "de")
    profile_unk = lab_3.main.LanguageProfile(letter_storage, "unk")

    profile_eng.create_from_tokens(encoded_eng, (2,))
    profile_de.create_from_tokens(encoded_de, (2,))
    profile_unk.create_from_tokens(encoded_unk, (2,))

    print(lab_3.main.calculate_distance(profile_unk, profile_eng, 5, 2))
    print(lab_3.main.calculate_distance(profile_unk, profile_de, 5, 2))
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

    RESULT = '17\n25'
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT, 'Detection not working'
