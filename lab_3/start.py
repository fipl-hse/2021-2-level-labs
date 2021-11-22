"""
Language detection starter
"""

import os
from lab_3.main import \
    tokenize_by_sentence, \
    LetterStorage, \
    encode_corpus, \
    decode_corpus, \
    NGramTrie, \
    LanguageProfile, \
    calculate_distance, \
    LanguageDetector

PATH_TO_LAB_FOLDER = os.path.dirname(os.path.abspath(__file__))

if __name__ == '__main__':
    ENG_SAMPLE = "Helium is the byproduct of millennia of radioactive " \
                 "decay from the elements thorium and uranium."
    GERMAN_SAMPLE = "Zwei Begriffe, die nicht unbedingt zueinander passen, " \
                    "am Arbeitsplatz schon mal gar nicht."
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
    # EXPECTED_SCORE = {'en': 24, 'de': 25}

    # score 10, k = 1000, trie_levels = (2,)
    # predict SECRET_SAMPLE
    # print(detector.detect(unknown_profile, 1000, (2,)))
    # EXPECTED_LANGUAGE = ?
    # EXPECTED_MIN_DISTANCE = ?

    # tokenize by sentence:
    eng_tokens = tokenize_by_sentence(ENG_SAMPLE)
    de_tokens = tokenize_by_sentence(GERMAN_SAMPLE)
    unknown_tokens = tokenize_by_sentence(UNKNOWN_SAMPLE)

    # creating letter storages
    storage = LetterStorage()  # создание пустого экземпляра класса
    storage.update(eng_tokens)
    storage.update(de_tokens)
    storage.update(unknown_tokens)

    # encoding text
    eng_text_encoded = encode_corpus(storage, eng_tokens)
    de_text_encoded = encode_corpus(storage, de_tokens)
    unk_text_encoded = encode_corpus(storage, unknown_tokens)

    # decoding text
    eng_text_decoded = decode_corpus(storage, eng_tokens)
    de_text_decoded = decode_corpus(storage, de_tokens)
    unk_text_decoded = decode_corpus(storage, unknown_tokens)

    # creating n-grams
    eng_grams = NGramTrie(3, storage)
    de_grams = NGramTrie(3, storage)
    unknown_grams = NGramTrie(3, storage)

    # creating language profiles
    eng_profile = LanguageProfile(storage, 'en')
    de_profile = LanguageProfile(storage, 'de')
    unknown_profile = LanguageProfile(storage, 'unknown')

    # saving
    # calculating distance
    # detecting language

    RESULT = ''
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT, 'Detection not working'
