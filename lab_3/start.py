"""
Language detection starter
"""

import os
import lab_3.main

PATH_TO_LAB_FOLDER = os.path.dirname(os.path.abspath(__file__))

if __name__ == '__main__':
    ENG_SAMPLE = """Helium is the byproduct of millennia of radioactive decay
    from the elements thorium and uranium."""
    GERMAN_SAMPLE = """Zwei Begriffe, die nicht unbedingt zueinander passen,
    am Arbeitsplatz schon mal gar nicht."""
    UNKNOWN_SAMPLE = "Helium is material."
    SECRET_SAMPLE = """ Некој е болен и тој не е слободен. Dлетува гол во дупка од мраз.
    И пее, а плаче од болка. Дали е ова контраст, можеби – живот?"""

    # score 6, params: k = 5, trie_level = 2
    # predict UNKNOWN_SAMPLE
    # print(calculate_distance(unknown_profile, en_profile, 5, 2))
    # print(calculate_distance(unknown_profile, de_profile, 5, 2))
    EXPECTED_DISTANCE_TO_EN_DE_PROFILES = 17, 25

    TOKENIZED_ENG_SAMPLE_6 = lab_3.main.tokenize_by_sentence(ENG_SAMPLE)
    TOKENIZED_DE_SAMPLE_6 = lab_3.main.tokenize_by_sentence(GERMAN_SAMPLE)
    TOKENIZED_UNKNOWN_SAMPLE_6 = lab_3.main.tokenize_by_sentence(UNKNOWN_SAMPLE)

    STORAGE_6 = lab_3.main.LetterStorage()
    STORAGE_6.update(TOKENIZED_ENG_SAMPLE_6)
    STORAGE_6.update(TOKENIZED_DE_SAMPLE_6)
    STORAGE_6.update(TOKENIZED_UNKNOWN_SAMPLE_6)

    ENCODED_ENG_6 = lab_3.main.encode_corpus(STORAGE_6, TOKENIZED_ENG_SAMPLE_6)
    ENCODED_DE_6 = lab_3.main.encode_corpus(STORAGE_6, TOKENIZED_DE_SAMPLE_6)
    ENCODED_UNKNOWN_6 = lab_3.main.encode_corpus(STORAGE_6, TOKENIZED_UNKNOWN_SAMPLE_6)

    PROFILE_ENG_6 = lab_3.main.LanguageProfile(STORAGE_6, 'en')
    PROFILE_DE_6 = lab_3.main.LanguageProfile(STORAGE_6, 'de')
    PROFILE_UNKNOWN_6 = lab_3.main.LanguageProfile(STORAGE_6, 'unk')

    PROFILE_ENG_6.create_from_tokens(ENCODED_ENG_6, (2,))
    PROFILE_DE_6.create_from_tokens(ENCODED_DE_6, (2,))
    PROFILE_UNKNOWN_6.create_from_tokens(ENCODED_UNKNOWN_6, (2,))

    DISTANCE_ENG_UNK_6 = lab_3.main.calculate_distance(PROFILE_UNKNOWN_6, PROFILE_ENG_6, 5, 2)
    DISTANCE_DE_UNK_6 = lab_3.main.calculate_distance(PROFILE_UNKNOWN_6, PROFILE_DE_6, 5, 2)

    # score 8, k = 5, trie_level = 3
    # predict UNKNOWN_SAMPLE
    # print(detector.detect(profile_unk, 5, 3))
    EXPECTED_SCORE = {'en': 24, 'de': 25}

    # 1
    TOKENIZED_ENG_SAMPLE_8 = lab_3.main.tokenize_by_sentence(ENG_SAMPLE)
    TOKENIZED_DE_SAMPLE_8 = lab_3.main.tokenize_by_sentence(GERMAN_SAMPLE)
    TOKENIZED_UNKNOWN_SAMPLE_8 = lab_3.main.tokenize_by_sentence(UNKNOWN_SAMPLE)

    STORAGE_8 = lab_3.main.LetterStorage()
    STORAGE_8.update(TOKENIZED_ENG_SAMPLE_8)
    STORAGE_8.update(TOKENIZED_DE_SAMPLE_8)
    STORAGE_8.update(TOKENIZED_UNKNOWN_SAMPLE_8)

    ENCODED_ENG_8 = lab_3.main.encode_corpus(STORAGE_8, TOKENIZED_ENG_SAMPLE_8)
    ENCODED_DE_8 = lab_3.main.encode_corpus(STORAGE_8, TOKENIZED_DE_SAMPLE_8)
    ENCODED_UNKNOWN_8 = lab_3.main.encode_corpus(STORAGE_8, TOKENIZED_UNKNOWN_SAMPLE_8)

    PROFILE_ENG_8 = lab_3.main.LanguageProfile(STORAGE_8, 'en')
    PROFILE_DE_8 = lab_3.main.LanguageProfile(STORAGE_8, 'de')
    PROFILE_UNKNOWN_8 = lab_3.main.LanguageProfile(STORAGE_8, 'unk')

    PROFILE_ENG_8.create_from_tokens(ENCODED_ENG_8, (3,))
    PROFILE_DE_8.create_from_tokens(ENCODED_DE_8, (3,))
    PROFILE_UNKNOWN_8.create_from_tokens(ENCODED_UNKNOWN_8, (3,))

    # 2
    PROFILE_UNKNOWN_8.save(os.path.join(PATH_TO_LAB_FOLDER, 'unknown_profile.json'))

    # 3
    PROFILE_UNK = lab_3.main.LanguageProfile(STORAGE_8, 'unk')
    PROFILE_UNK.open('unknown_profile.json')

    # 4
    DETECTOR = lab_3.main.LanguageDetector()
    DETECTOR.register_language(PROFILE_ENG_8)
    DETECTOR.register_language(PROFILE_DE_8)

    # score 10, k = 1000, trie_levels = (2,)
    # predict SECRET_SAMPLE
    # print(detector.detect(unknown_profile, 1000, (2,)))
    # EXPECTED_LANGUAGE = ?
    # EXPECTED_MIN_DISTANCE = ?

    RESULT_6 = DISTANCE_ENG_UNK_6, DISTANCE_DE_UNK_6
    RESULT_8 = DETECTOR.detect(PROFILE_UNK, 5, (3,))

    # print(RESULT_6)
    # print(RESULT_8)

    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert EXPECTED_DISTANCE_TO_EN_DE_PROFILES == RESULT_6, 'Detection not working'
    assert EXPECTED_SCORE == RESULT_8, 'Detection not working'
