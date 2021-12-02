"""
Language detection starter
"""
import os
from lab_3.main import tokenize_by_sentence, \
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
    GERMAN_SAMPLE = "Zwei Begriffe, die nicht unbedingt zueinander " \
                    "passen, am Arbeitsplatz schon mal gar nicht."
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

    eng_tokens = tokenize_by_sentence(ENG_SAMPLE)
    de_tokens = tokenize_by_sentence(GERMAN_SAMPLE)
    unknown_tokens = tokenize_by_sentence(UNKNOWN_SAMPLE)

    storage = LetterStorage()
    storage.update(eng_tokens)
    storage.update(de_tokens)
    storage.update(unknown_tokens)

    eng_text_encoded = encode_corpus(storage, eng_tokens)
    de_text_encoded = encode_corpus(storage, de_tokens)
    unknown_text_encoded = encode_corpus(storage, unknown_tokens)

    eng_grams = NGramTrie(3, storage)
    eng_grams.extract_n_grams(eng_text_encoded)
    eng_grams.get_n_grams_frequencies()

    de_grams = NGramTrie(3, storage)
    de_grams.extract_n_grams(de_text_encoded)
    de_grams.get_n_grams_frequencies()

    unknown_grams = NGramTrie(3, storage)
    unknown_grams.extract_n_grams(unknown_text_encoded)
    unknown_grams.get_n_grams_frequencies()

    eng_profile = LanguageProfile(storage, 'en')
    eng_profile.create_from_tokens(eng_text_encoded, (3,))

    de_profile = LanguageProfile(storage, 'de')
    de_profile.create_from_tokens(de_text_encoded, (3,))

    unknown_profile = LanguageProfile(storage, 'unknown')
    unknown_profile.create_from_tokens(unknown_text_encoded, (3,))

    unknown_profile.save('unknown_profile.json')
    profile_unk = LanguageProfile(storage, '')
    profile_unk.open('unknown_profile.json')

    detector = LanguageDetector()
    detector.register_language(eng_profile)
    detector.register_language(de_profile)
    language = detector.detect(profile_unk, 5, (3,))
    print(language)

    RESULT = ''
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    EXPECTED_SCORE = {'en': 24, 'de': 25}
    assert language, EXPECTED_SCORE
