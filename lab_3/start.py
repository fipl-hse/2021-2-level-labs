"""
Language detection starter
"""

import os
from lab_3.main import tokenize_by_sentence, LetterStorage, encode_corpus

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

    tokenized_un = tokenize_by_sentence(UNKNOWN_SAMPLE)
    tokenized_en = tokenize_by_sentence(ENG_SAMPLE)
    tokenized_ge = tokenize_by_sentence(GERMAN_SAMPLE)

    un_letter_storage = LetterStorage()
    un_letter_storage.update(tokenized_un)
    encoded_un_corpus = encode_corpus(un_letter_storage, tokenized_un)

    en_letter_storage = LetterStorage()
    en_letter_storage.update(tokenized_en)
    encoded_en_corpus = encode_corpus(en_letter_storage, tokenized_en)

    ge_letter_storage = LetterStorage()
    ge_letter_storage.update(tokenized_ge)
    encoded_ge_corpus = encode_corpus(ge_letter_storage, tokenized_ge)

    # score 8, k = 5, trie_level = 3
    # predict UNKNOWN_SAMPLE
    # print(detector.detect(profile_unk, 5, 3))
    # EXPECTED_SCORE = {'en': 24, 'de': 25}

    # score 10, k = 1000, trie_levels = (2,)
    # predict SECRET_SAMPLE
    # print(detector.detect(unknown_profile, 1000, (2,)))
    # EXPECTED_LANGUAGE = ?
    # EXPECTED_MIN_DISTANCE = ?

    RESULT = ''
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT, 'Detection not working'

