"""
Language detection starter
"""
import os
from lab_3.main import tokenize_by_sentence, LetterStorage,\
    encode_corpus, LanguageProfile, calculate_distance, LanguageDetector
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

    eng_tokens = tokenize_by_sentence(ENG_SAMPLE)
    ge_tokens = tokenize_by_sentence(GERMAN_SAMPLE)
    unk_tokens = tokenize_by_sentence(UNKNOWN_SAMPLE)

    letters = LetterStorage()
    letters.update(eng_tokens)
    letters.update(ge_tokens)
    letters.update(unk_tokens)

    encoded_eng = encode_corpus(letters, eng_tokens)
    encoded_ge = encode_corpus(letters, ge_tokens)
    encoded_unk = encode_corpus(letters, unk_tokens)

    eng_profile = LanguageProfile(letters, "eng")
    de_profile = LanguageProfile(letters, "ge")
    unknown_profile = LanguageProfile(letters, "unk")

    ngram_sizes = tuple([2])

    eng_profile.create_from_tokens(encoded_eng, ngram_sizes)
    de_profile.create_from_tokens(encoded_ge, ngram_sizes)
    unknown_profile.create_from_tokens(encoded_unk, ngram_sizes)

    #result_for_eng = calculate_distance(
    # unknown_profile,eng_profile, k, trie_level)
    print(calculate_distance(unknown_profile, eng_profile, 5, 2))
    print(calculate_distance(unknown_profile, de_profile, 5, 2))

    # score 8, k = 5, trie_level = 3
    # predict UNKNOWN_SAMPLE
    # print(detector.detect(profile_unk, 5, 3))
    # EXPECTED_SCORE = {'en': 24, 'de': 25}

    unknown_profile.save('unknown_profile.json')
    profile_unk = LanguageProfile(letters, "unk")
    profile_unk.open('unknown_profile.json')

    detector = LanguageDetector()
    detector.register_language(eng_profile)
    detector.register_language(de_profile)

    ngram_sizes = tuple([3])

    eng_profile.create_from_tokens(encoded_eng, ngram_sizes)
    de_profile.create_from_tokens(encoded_ge, ngram_sizes)
    profile_unk.create_from_tokens(encoded_unk, ngram_sizes)

    print(detector.detect(profile_unk, 5, ngram_sizes))

    # score 10, k = 1000, trie_levels = (2,)
    # predict SECRET_SAMPLE
    # print(detector.detect(unknown_profile, 1000, (2,)))
    # EXPECTED_LANGUAGE = ?
    # EXPECTED_MIN_DISTANCE = ?

    RESULT = ''
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT, 'Detection not working'
