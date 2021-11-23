"""
Language detection starter
"""

import os
from lab_3.main import tokenize_by_sentence, LetterStorage, encode_corpus, \
    LanguageProfile, calculate_distance, LanguageDetector

PATH_TO_LAB_FOLDER = os.path.dirname(os.path.abspath(__file__))

if __name__ == '__main__':
    ENG_SAMPLE = """Helium is the byproduct of millennia of radioactive
decay from the elements thorium and uranium."""
    GERMAN_SAMPLE = """Zwei Begriffe, die nicht unbedingt zueinander passen,
am Arbeitsplatz schon mal gar nicht."""
    UNKNOWN_SAMPLE = "Helium is material."
    SECRET_SAMPLE = """ Некој е болен и тој не е слободен. Dлетува гол во дупка од мраз.
И пее, а плаче од болка. Дали е ова контраст, можеби – живот?"""

    eng_tokens = tokenize_by_sentence(ENG_SAMPLE)
    de_tokens = tokenize_by_sentence(GERMAN_SAMPLE)
    unk_tokens = tokenize_by_sentence(UNKNOWN_SAMPLE)

    storage = LetterStorage()
    storage.update(eng_tokens)
    storage.update(de_tokens)
    storage.update(unk_tokens)

    eng_encoded = encode_corpus(storage, eng_tokens)
    de_encoded = encode_corpus(storage, de_tokens)
    unk_encoded = encode_corpus(storage, unk_tokens)

    # score 6, params: k = 5, trie_level = 2
    # predict UNKNOWN_SAMPLE
    '''''
    eng_profile = LanguageProfile(storage, 'eng')
    de_profile = LanguageProfile(storage, 'de')
    unk_profile = LanguageProfile(storage, 'unk')

    eng_profile.create_from_tokens(eng_encoded, (2,))
    de_profile.create_from_tokens(de_encoded, (2,))
    unk_profile.create_from_tokens(unk_encoded, (2,))

    eng_distance = calculate_distance(unk_profile, eng_profile, 5, 2)
    de_distance = calculate_distance(unk_profile, de_profile, 5, 2)

    RESULT_6 = eng_distance, de_distance
    EXPECTED_DISTANCE_TO_EN_DE_PROFILES = 17, 25
    '''''

    # score 8, k = 5, trie_level = 3
    # predict UNKNOWN_SAMPLE
    eng_profile_8 = LanguageProfile(storage, 'en')
    de_profile_8 = LanguageProfile(storage, 'de')
    unk_profile_8 = LanguageProfile(storage, 'unk')

    eng_profile_8.create_from_tokens(eng_encoded, (3,))
    de_profile_8.create_from_tokens(de_encoded, (3,))
    unk_profile_8.create_from_tokens(unk_encoded, (3,))

    unk_profile_8.save('unknown_profile.json')
    unk_profile_new = LanguageProfile(storage, 'unk')
    unk_profile_new.open('unknown_profile.json')

    detector = LanguageDetector()
    detector.register_language(eng_profile_8)
    detector.register_language(de_profile_8)

    RESULT_8 = detector.detect(unk_profile_new, 5, (3,))
    print(RESULT_8)
    EXPECTED_SCORE = {'en': 24, 'de': 25}

    # score 10, k = 1000, trie_levels = (2,)
    # predict SECRET_SAMPLE
    # print(detector.detect(unknown_profile, 1000, (2,)))
    # EXPECTED_LANGUAGE = ?
    # EXPECTED_MIN_DISTANCE = ?

    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    # assert RESULT_6 == EXPECTED_DISTANCE_TO_EN_DE_PROFILES, 'Detection not working'
    assert RESULT_8 == EXPECTED_SCORE, 'Detection not working'
