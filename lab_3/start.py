"""
Language detection starter
"""

import os
from lab_3.main import \
    tokenize_by_sentence, \
    LetterStorage, \
    encode_corpus, \
    decode_corpus

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

    # score 8, k = 5, trie_level = 3
    # predict UNKNOWN_SAMPLE
    # print(detector.detect(profile_unk, 5, 3))
    #EXPECTED_SCORE = {'en': 24, 'de': 25}

    # score 10, k = 1000, trie_levels = (2,)
    # predict SECRET_SAMPLE
    # print(detector.detect(unknown_profile, 1000, (2,)))
    # EXPECTED_LANGUAGE = ?
    # EXPECTED_MIN_DISTANCE = ?

    eng_tokenize = tokenize_by_sentence(ENG_SAMPLE)
    german_tokenize = tokenize_by_sentence(GERMAN_SAMPLE)
    unknown_tokenize = tokenize_by_sentence(UNKNOWN_SAMPLE)

    storage = LetterStorage()
    storage.update(eng_tokenize)
    storage.update(german_tokenize)
    storage.update(unknown_tokenize)

    eng_tokenize_encoded = encode_corpus(storage, eng_tokenize)
    german_tokenize_encoded = encode_corpus(storage, german_tokenize)
    unknown_tokenize_encoded = encode_corpus(storage, unknown_tokenize)

    eng_tokenize_decoded = decode_corpus(storage, eng_tokenize_encoded)
    german_tokenize_decoded = decode_corpus(storage, german_tokenize_encoded)
    unknown_tokenize_decoded = decode_corpus(storage, unknown_tokenize_encoded)

    RESULT = ''
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT, 'Detection not working'

