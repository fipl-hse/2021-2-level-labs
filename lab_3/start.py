"""
Language detection starter
"""

import os
from lab_3.main import (LetterStorage,
                        LanguageProfile,
                        LanguageDetector,
                        ProbabilityLanguageDetector,
                        tokenize_by_sentence,
                        encode_corpus,
                        calculate_distance)

PATH_TO_LAB_FOLDER = os.path.dirname(os.path.abspath(__file__))

if __name__ == '__main__':
    ENG_SAMPLE = "Helium is the byproduct of millennia of radioactive" \
                 " decay from the elements thorium and uranium."
    GERMAN_SAMPLE = "Zwei Begriffe, die nicht unbedingt zueinander passen," \
                    " am Arbeitsplatz schon mal gar nicht."
    UNKNOWN_SAMPLE = "Helium is material."
    SECRET_SAMPLE = " Некој е болен и тој не е слободен. Dлетува гол во дупка од мраз. " \
                    "И пее, а плаче од болка. Дали е ова контраст, можеби – живот?"

    en_tokens = tokenize_by_sentence(ENG_SAMPLE)
    de_tokens = tokenize_by_sentence(GERMAN_SAMPLE)
    unk_tokens = tokenize_by_sentence(UNKNOWN_SAMPLE)
    secret_tokens = tokenize_by_sentence(SECRET_SAMPLE)

    storage = LetterStorage()
    storage.update(en_tokens)
    storage.update(de_tokens)
    storage.update(unk_tokens)
    storage.update(secret_tokens)

    encoded_en = encode_corpus(storage, en_tokens)
    encoded_de = encode_corpus(storage, de_tokens)
    encoded_unk = encode_corpus(storage, unk_tokens)
    encoded_secret = encode_corpus(storage, secret_tokens)

    # score 6, params: k = 5, trie_level = 2
    # predict UNKNOWN_SAMPLE
    unknown_profile = LanguageProfile(storage, 'unk')
    en_profile = LanguageProfile(storage, 'en')
    de_profile = LanguageProfile(storage, 'de')
    secret_profile = LanguageProfile(storage, 'secret')

    unknown_profile.create_from_tokens(encoded_unk, (2,))
    en_profile.create_from_tokens(encoded_en, (2,))
    de_profile.create_from_tokens(encoded_de, (2,))
    secret_profile.create_from_tokens(encoded_secret, (2,))

    RESULT_EN = calculate_distance(unknown_profile, en_profile, 5, 2)
    RESULT_DE = calculate_distance(unknown_profile, de_profile, 5, 2)
    RESULT_SCORE_6 = RESULT_EN, RESULT_DE
    EXPECTED_DISTANCE_TO_EN_DE_PROFILES = 17, 25

    # score 8, k = 5, trie_level = 3
    # predict UNKNOWN_SAMPLE

    unknown_profile.create_from_tokens(encoded_unk, (3,))
    en_profile.create_from_tokens(encoded_en, (3,))
    de_profile.create_from_tokens(encoded_de, (3,))

    unknown_profile.save('unknown_profile.json')
    unknown_profile = LanguageProfile(storage, 'unk')
    unknown_profile.open('unknown_profile.json')

    detector = LanguageDetector()
    detector.register_language(en_profile)
    detector.register_language(de_profile)

    RESULT_SCORE_8 = detector.detect(unknown_profile, 5, (3,))
    EXPECTED_SCORE = {'en': 24, 'de': 25}

    # score 10, k = 1000, trie_levels = (2,)
    # predict SECRET_SAMPLE
    # print(detector.detect(unknown_profile, 1000, (2,)))
    # EXPECTED_LANGUAGE = ?
    # EXPECTED_MIN_DISTANCE = ?

    detector = ProbabilityLanguageDetector()

    for file_name in os.listdir("profiles"):
        profile = LanguageProfile(storage, file_name)
        profile.open(f"profiles/{file_name}")
        detector.register_language(profile)
    probabilities_dict = detector.detect(secret_profile, 1000, (2,))
    secret_language = min(probabilities_dict, key=probabilities_dict.get)[0]
    print('Language:', secret_language)
    print('Distance:', probabilities_dict[secret_language])

    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT_SCORE_6 == EXPECTED_DISTANCE_TO_EN_DE_PROFILES, 'Detection not working'
    assert RESULT_SCORE_8 == EXPECTED_SCORE, 'Detection not working'
