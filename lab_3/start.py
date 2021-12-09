"""
Language detection starter
"""

import os
from lab_3.main import (tokenize_by_sentence,
                        LetterStorage,
                        encode_corpus,
                        LanguageProfile,
                        calculate_distance)

PATH_TO_LAB_FOLDER = os.path.dirname(os.path.abspath(__file__))

if __name__ == '__main__':
    ENG_SAMPLE = "Helium is the byproduct of millennia of radioactive decay from the elements thorium and uranium."
    GERMAN_SAMPLE = "Zwei Begriffe, die nicht unbedingt zueinander passen, am Arbeitsplatz schon mal gar nicht."
    UNKNOWN_SAMPLE = "Helium is material."
    SECRET_SAMPLE = """ Некој е болен и тој не е слободен. Dлетува гол во дупка од мраз. 
    И пее, а плаче од болка. Дали е ова контраст, можеби – живот?"""

    eng_text = tokenize_by_sentence(ENG_SAMPLE)
    de_text = tokenize_by_sentence(GERMAN_SAMPLE)
    unk_text = tokenize_by_sentence(UNKNOWN_SAMPLE)

    storage = LetterStorage()
    storage.update(eng_text)
    storage.update(de_text)
    storage.update(unk_text)

    encoded_eng_corpus = encode_corpus(storage, eng_text)
    encoded_de_corpus = encode_corpus(storage, de_text)
    encoded_unk_corpus = encode_corpus(storage, unk_text)

    eng_profile = LanguageProfile(storage, 'en')
    de_profile = LanguageProfile(storage, 'de')
    unk_profile = LanguageProfile(storage, 'unk')

    k = 5
    trie_level = 2
    eng_profile.create_from_tokens(encoded_eng_corpus, (trie_level,))
    de_profile.create_from_tokens(encoded_de_corpus, (trie_level,))
    unk_profile.create_from_tokens(encoded_unk_corpus, (trie_level,))

    # score 6, params: k = 5, trie_level = 2
    # predict UNKNOWN_SAMPLE
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

    RESULT = ''
    RESULT = (calculate_distance(unk_profile, eng_profile, 5, 2)), \
             (calculate_distance(unk_profile, de_profile, 5, 2))
    print(RESULT)
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT, 'Detection not working'