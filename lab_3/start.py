"""
Language detection starter
"""

import os
from lab_3.main import (tokenize_by_sentence,
                       encode_corpus,
                       calculate_distance,
                       LetterStorage,
                       LanguageProfile,
                       LanguageDetector,
                       ProbabilityLanguageDetector)
PATH_TO_LAB_FOLDER = os.path.dirname(os.path.abspath(__file__))

if __name__ == '__main__':
    ENG_SAMPLE = '''Helium is the byproduct of millennia of radioactive decay from the elements
    thorium and uranium.'''
    GERMAN_SAMPLE = '''Zwei Begriffe, die nicht unbedingt zueinander passen,
    am Arbeitsplatz schon mal gar nicht.'''
    UNKNOWN_SAMPLE = "Helium is material."
    SECRET_SAMPLE = """ Некој е болен и тој не е слободен. Dлетува гол во дупка од мраз.
    И пее, а плаче од болка. Дали е ова контраст, можеби – живот?"""

    text_en = tokenize_by_sentence(ENG_SAMPLE)
    text_de = tokenize_by_sentence(GERMAN_SAMPLE)
    text_unk = tokenize_by_sentence(UNKNOWN_SAMPLE)
    text_secret = tokenize_by_sentence(SECRET_SAMPLE)

    storage = LetterStorage()
    storage.update(text_en)
    storage.update(text_de)
    storage.update(text_unk)
    storage.update(text_secret)

    encoded_en = encode_corpus(storage, text_en)
    encoded_de = encode_corpus(storage, text_de)
    encoded_unk = encode_corpus(storage, text_unk)
    encoded_secret = encode_corpus(storage, text_secret)

    # score 6, params: k = 5, trie_level = 2
    # predict UNKNOWN_SAMPLE
    # print(calculate_distance(unknown_profile, en_profile, 5, 2))
    # print(calculate_distance(unknown_profile, de_profile, 5, 2))
    profile_en_6 = LanguageProfile(storage, 'en')
    profile_de_6 = LanguageProfile(storage, 'de')
    profile_unk_6 = LanguageProfile(storage, 'unk')

    profile_en_6.create_from_tokens(encoded_en, (2,))
    profile_de_6.create_from_tokens(encoded_de, (2,))
    profile_unk_6.create_from_tokens(encoded_unk, (2,))

    distance_en_unk_6 = calculate_distance(profile_unk_6, profile_en_6, 5, 2)
    distance_de_unk_6 = calculate_distance(profile_unk_6, profile_de_6, 5, 2)
    RESULT_6 = distance_en_unk_6, distance_de_unk_6
    EXPECTED_DISTANCE_TO_EN_DE_PROFILES = 17, 25
    assert RESULT_6 == EXPECTED_DISTANCE_TO_EN_DE_PROFILES, 'Detection not working'

    # score 8, k = 5, trie_level = 3
    # predict UNKNOWN_SAMPLE
    # print(detector.detect(profile_unk, 5, 3))
    # EXPECTED_SCORE = {'en': 24, 'de': 25}
    profile_en_8 = LanguageProfile(storage, 'en')
    profile_de_8 = LanguageProfile(storage, 'de')
    profile_unk_8 = LanguageProfile(storage, 'unk')

    profile_en_8.create_from_tokens(encoded_en, (3,))
    profile_de_8.create_from_tokens(encoded_de, (3,))
    profile_unk_8.create_from_tokens(encoded_unk, (3,))

    calculate_distance(profile_unk_8, profile_en_8, 5, 3)
    calculate_distance(profile_unk_8, profile_de_8, 5, 3)

    profile_unk_8.save('unknown_profile.json')
    profile_unk = LanguageProfile(storage, 'unk')
    profile_unk.open('unknown_profile.json')

    detector = LanguageDetector()

    detector.register_language(profile_en_8)
    detector.register_language(profile_de_8)

    RESULT_8 = detector.detect(profile_unk, 5, 3)
    EXPECTED_SCORE = {'en': 24, 'de': 25}
    assert RESULT_8 == EXPECTED_SCORE, 'Detection not working'

    # score 10, k = 1000, trie_levels = (2,)
    # predict SECRET_SAMPLE
    # print(detector.detect(unknown_profile, 1000, (2,)))
    # EXPECTED_LANGUAGE = ?
    #  = ?
    detector = ProbabilityLanguageDetector()
    profile_secret = LanguageProfile(storage, 'secret')
    profile_secret.create_from_tokens(encoded_secret, (2,))
    for in_file in os.listdir("profiles"):
        profile = LanguageProfile(storage, in_file)
        profile.open(f'profiles/{in_file}')
        detector.register_language(profile)
    probabilities = detector.detect(profile_secret, 1000, (2,))
    EXPECTED_LANGUAGE = min(probabilities.items(), key=lambda x: x[1])[0]
    EXPECTED_MIN_DISTANCE = probabilities[EXPECTED_LANGUAGE]
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    # assert RESULT, 'Detection not working'
