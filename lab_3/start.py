"""
Language detection starter
"""

import os
from lab_3.main import tokenize_by_sentence, LetterStorage, encode_corpus, \
    LanguageProfile, calculate_distance, LanguageDetector

PATH_TO_LAB_FOLDER = os.path.dirname(os.path.abspath(__file__))

if __name__ == '__main__':
    ENG_SAMPLE = "Helium is the byproduct of millennia of " \
                 "radioactive decay from the elements thorium and uranium."
    GERMAN_SAMPLE = "Zwei Begriffe, die nicht unbedingt zueinander passen, " \
                    "am Arbeitsplatz schon mal gar nicht."
    UNKNOWN_SAMPLE = "Helium is material."
    SECRET_SAMPLE = """ Некој е болен и тој не е слободен. Dлетува гол во дупка од мраз.
    И пее, а плаче од болка. Дали е ова контраст, можеби – живот?"""


def predict_language(k_6: int, k_8: int, trie_level_6: int, trie_level_8: int):
    """
    Calculates distance between top_k n-grams of unknown profile and known profile
    and predicts UNKNOWN_SAMPLE
    :param k_6 and k_8: number of frequent N-grams to take into consideration
    :param trie_level_6 and trie_level_8: N-gram sizes to use in comparison
    :return: True if succeeds, False if not
    """

    tokenized_en = tokenize_by_sentence(ENG_SAMPLE)
    tokenized_de = tokenize_by_sentence(GERMAN_SAMPLE)
    tokenized_unk = tokenize_by_sentence(UNKNOWN_SAMPLE)

    storage = LetterStorage()
    storage.update(tokenized_en)
    storage.update(tokenized_de)
    storage.update(tokenized_unk)

    encoded_en = encode_corpus(storage, tokenized_en)
    encoded_de = encode_corpus(storage, tokenized_de)
    encoded_unk = encode_corpus(storage, tokenized_unk)

    en_profile_6 = LanguageProfile(storage, 'en')
    de_profile_6 = LanguageProfile(storage, 'de')
    unk_profile_6 = LanguageProfile(storage, 'unk')

    en_profile_6.create_from_tokens(encoded_en, (k_6, trie_level_6))
    de_profile_6.create_from_tokens(encoded_de, (k_6, trie_level_6))
    unk_profile_6.create_from_tokens(encoded_unk, (k_6, trie_level_6))

    en_distance_6 = calculate_distance(unk_profile_6, en_profile_6, k_6, trie_level_6)
    de_distance_6 = calculate_distance(unk_profile_6, de_profile_6, k_6, trie_level_6)
    RESULT_6 = en_distance_6, de_distance_6
    print(RESULT_6)

    en_profile_8 = LanguageProfile(storage, 'en')
    de_profile_8 = LanguageProfile(storage, 'de')
    unk_profile_8 = LanguageProfile(storage, 'unk')

    en_profile_8.create_from_tokens(encoded_en, (k_8, trie_level_8))
    de_profile_8.create_from_tokens(encoded_de, (k_8, trie_level_8))
    unk_profile_8.create_from_tokens(encoded_unk, (k_8, trie_level_8))

    calculate_distance(unk_profile_8, en_profile_8, k_8, trie_level_8)
    calculate_distance(unk_profile_8, de_profile_8, k_8, trie_level_8)

    unk_profile_8.save('unknown_profile.json')
    profile_unk = LanguageProfile(storage, 'unk')
    profile_unk.open('unknown_profile.json')

    detector = LanguageDetector()

    detector.register_language(en_profile_8)
    detector.register_language(de_profile_8)

    RESULT_8 = detector.detect(profile_unk, 5, (3,))
    print(RESULT_8)

    EXPECTED_DISTANCE_TO_EN_DE_PROFILES = 17, 25
    EXPECTED_SCORE = {'en': 24, 'de': 25}

    if RESULT_6 == EXPECTED_DISTANCE_TO_EN_DE_PROFILES and RESULT_8 == EXPECTED_SCORE:
        return True
    return False


EXPECTED = predict_language(5, 5, 2, 3)

RESULT = True

assert RESULT == EXPECTED, 'Detection not working'
