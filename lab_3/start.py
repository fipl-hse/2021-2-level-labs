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


def predict_language():
    """
    Calculates distance between top_k n-grams of unknown profile and known profile
    and predicts UNKNOWN_SAMPLE
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

    en_profile_6.create_from_tokens(encoded_en, (5, 2))
    de_profile_6.create_from_tokens(encoded_de, (5, 2))
    unk_profile_6.create_from_tokens(encoded_unk, (5, 2))

    en_distance_6 = calculate_distance(unk_profile_6, en_profile_6, 5, 2)
    de_distance_6 = calculate_distance(unk_profile_6, de_profile_6, 5, 2)
    result_6 = en_distance_6, de_distance_6
    print(result_6)

    en_profile_8 = LanguageProfile(storage, 'en')
    de_profile_8 = LanguageProfile(storage, 'de')
    unk_profile_8 = LanguageProfile(storage, 'unk')

    en_profile_8.create_from_tokens(encoded_en, (5, 3))
    de_profile_8.create_from_tokens(encoded_de, (5, 3))
    unk_profile_8.create_from_tokens(encoded_unk, (5, 3))

    calculate_distance(unk_profile_8, en_profile_8, 5, 3)
    calculate_distance(unk_profile_8, de_profile_8, 5, 3)

    unk_profile_8.save('unknown_profile.json')
    profile_unk = LanguageProfile(storage, 'unk')
    profile_unk.open('unknown_profile.json')

    detector = LanguageDetector()

    detector.register_language(en_profile_8)
    detector.register_language(de_profile_8)

    result_8 = detector.detect(profile_unk, 5, (3,))
    print(result_8)

    expected_distance = 17, 25
    expected_score = {'en': 24, 'de': 25}

    if result_6 == expected_distance and result_8 == expected_score:
        return True
    return False


EXPECTED = predict_language()

RESULT = True

assert RESULT == EXPECTED, 'Detection not working'
