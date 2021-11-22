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
    # EXPECTED_DISTANCE_TO_EN_DE_PROFILES = 17, 25

    # score 8, k = 5, trie_level = 3
    # predict UNKNOWN_SAMPLE
    # print(detector.detect(profile_unk, 5, 3))
    EXPECTED_SCORE = {'en': 24, 'de': 25}
    # creating tokenized tuples
    eng_tokens = tokenize_by_sentence(ENG_SAMPLE)
    de_tokens = tokenize_by_sentence(GERMAN_SAMPLE)
    unk_tokens = tokenize_by_sentence(UNKNOWN_SAMPLE)
    # creating letter storage
    storage = LetterStorage()
    storage.update(eng_tokens)
    storage.update(de_tokens)
    storage.update(unk_tokens)
    # encoding texts
    eng_text = encode_corpus(storage, eng_tokens)
    de_text = encode_corpus(storage, de_tokens)
    unk_text = encode_corpus(storage, unk_tokens)
    # creating n_gamm_tries
    eng_trie = NGramTrie(3, storage)
    eng_trie.extract_n_grams(eng_text)
    eng_trie.get_n_grams_frequencies()
    de_trie = NGramTrie(3, storage)
    de_trie.extract_n_grams(de_text)
    de_trie.get_n_grams_frequencies()
    unk_trie = NGramTrie(3, storage)
    unk_trie.extract_n_grams(unk_text)
    unk_trie.get_n_grams_frequencies()
    # creating profiles
    en_profile = LanguageProfile(storage, 'en')
    en_profile.create_from_tokens(eng_text, (3, ))
    de_profile = LanguageProfile(storage, 'de')
    de_profile.create_from_tokens(de_text, (3, ))
    unknown = LanguageProfile(storage, 'unknown')
    unknown.create_from_tokens(unk_text, (3, ))
    # saving and opening unknown
    unknown.save('unknown_profile.json')
    profile_unk = LanguageProfile(storage, '')
    profile_unk.open('unknown_profile.json')
    # detecting
    detector = LanguageDetector()
    detector.register_language(en_profile)
    detector.register_language(de_profile)
    result = detector.detect(profile_unk, 5, (3, ))
    print(result)



    # score 10, k = 1000, trie_levels = (2,)
    # predict SECRET_SAMPLE
    # print(detector.detect(unknown_profile, 1000, (2,)))
    # EXPECTED_LANGUAGE = ?
    # EXPECTED_MIN_DISTANCE = ?

    RESULT = ''
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert result, EXPECTED_SCORE
