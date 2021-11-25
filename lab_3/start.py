"""
Language detection starter
"""

import os
from lab_3.main import tokenize_by_sentence, LetterStorage, encode_corpus, LanguageProfile, calculate_distance

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

    unk_tokenization = tokenize_by_sentence(UNKNOWN_SAMPLE)
    deutsch_tokenization = tokenize_by_sentence(GERMAN_SAMPLE)
    eng_tokenization = tokenize_by_sentence(ENG_SAMPLE)

    unk_letter_storage = LetterStorage()
    unk_letter_storage.update(unk_tokenization)
    unk_encoded_corpus = encode_corpus(unk_letter_storage, unk_tokenization)
    unk_lg_profile = LanguageProfile(letter_storage=unk_letter_storage, language_name='unknown')
    unk_lg_profile.create_from_tokens(unk_encoded_corpus, (3,))

    deutsch_letter_storage = LetterStorage()
    deutsch_letter_storage.update(deutsch_tokenization)
    deutsch_encoded_corpus = encode_corpus(deutsch_letter_storage, deutsch_tokenization)
    deutsch_lg_profile = LanguageProfile(letter_storage=deutsch_letter_storage, language_name='de')
    deutsch_lg_profile.create_from_tokens(deutsch_encoded_corpus, (3,))

    eng_letter_storage = LetterStorage()
    eng_letter_storage.update(eng_tokenization)
    eng_encoded_corpus = encode_corpus(eng_letter_storage, eng_tokenization)
    eng_lg_profile = LanguageProfile(letter_storage=eng_letter_storage, language_name='en')
    eng_lg_profile.create_from_tokens(eng_encoded_corpus, (3,))

    eng_unk_distance = calculate_distance(unknown_profile=unk_lg_profile, known_profile=eng_lg_profile,
                                          k=5, trie_level=3)
    deutsch_unk_distance = calculate_distance(unknown_profile=unk_lg_profile, known_profile=deutsch_lg_profile,
                                              k=5, trie_level=3)
    # score 8, k = 5, trie_level = 3
    # predict UNKNOWN_SAMPLE
    # print(detector.detect(profile_unk, 5, 3))
    # EXPECTED_SCORE = {'en': 24, 'de': 25}

    # score 10, k = 1000, trie_levels = (2,)
    # predict SECRET_SAMPLE
    # print(detector.detect(unknown_profile, 1000, (2,)))
    # EXPECTED_LANGUAGE = ?
    # EXPECTED_MIN_DISTANCE = ?

    RESULT = 'DISTANCE_TO_EN_DE_PROFILES = {}, {}'.format(eng_unk_distance, deutsch_unk_distance)
    print(RESULT)
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT, 'Detection not working'

