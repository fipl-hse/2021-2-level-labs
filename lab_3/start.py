"""
Language detection starter
"""

import os

from lab_3.main import tokenize_by_sentence, LetterStorage, \
    encode_corpus, LanguageProfile, calculate_distance

PATH_TO_LAB_FOLDER = os.path.dirname(os.path.abspath(__file__))


def score_6():
    en_text = tokenize_by_sentence(ENG_SAMPLE)
    de_text = tokenize_by_sentence(GERMAN_SAMPLE)
    unknown_text = tokenize_by_sentence(UNKNOWN_SAMPLE)

    storage = LetterStorage()
    storage.update(en_text)
    encoded_en_text = encode_corpus(storage, en_text)

    storage.update(de_text)
    encoded_de_text = encode_corpus(storage, de_text)

    storage.update(unknown_text)
    encoded_unknown_text = encode_corpus(storage, unknown_text)

    en_profile = LanguageProfile(letter_storage=storage, language_name='en')
    en_profile.create_from_tokens(encoded_en_text, (2,))

    de_profile = LanguageProfile(letter_storage=storage, language_name='de')
    de_profile.create_from_tokens(encoded_de_text, (2,))

    unknown_profile = LanguageProfile(letter_storage=storage, language_name='unknown')
    unknown_profile.create_from_tokens(encoded_unknown_text, (2,))

    distance_en_to_unknown = calculate_distance(unknown_profile, en_profile, 5, 2)
    distance_de_to_unknown = calculate_distance(unknown_profile, de_profile, 5, 2)
    print(f"DISTANCE_TO_EN_DE_PROFILES = {str(distance_en_to_unknown)}, "
          f"{str(distance_de_to_unknown)}")


if __name__ == '__main__':
    ENG_SAMPLE = "Helium is the byproduct of millennia of radioactive decay " \
                 "from the elements thorium and uranium."
    GERMAN_SAMPLE = "Zwei Begriffe, die nicht unbedingt zueinander passen, " \
                    "am Arbeitsplatz schon mal gar nicht."
    UNKNOWN_SAMPLE = "Helium is material."
    SECRET_SAMPLE = " Некој е болен и тој не е слободен. Dлетува гол во дупка од мраз. " \
                    "И пее, а плаче од болка. Дали е ова контраст, можеби – живот?"

    # score 6, params: k = 5, trie_level = 2
    # predict UNKNOWN_SAMPLE
    # print(calculate_distance(unknown_profile, en_profile, 5, 2))
    # print(calculate_distance(unknown_profile, de_profile, 5, 2))
    EXPECTED_DISTANCE_TO_EN_DE_PROFILES = 17, 25
    score_6()

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
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT, 'Detection not working'
