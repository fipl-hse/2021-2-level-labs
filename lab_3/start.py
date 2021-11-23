"""
Language detection starter
"""

import os
from lab_3.main import (
    LetterStorage,
    LanguageProfile,
    LanguageDetector,
    ProbabilityLanguageDetector,
    create_profile_from_text,
    calculate_distance
)

PATH_TO_LAB_FOLDER = os.path.dirname(os.path.abspath(__file__))

if __name__ == '__main__':
    ENG_SAMPLE = "Helium is the byproduct of millennia of radioactive decay from the elements thorium and uranium."
    GERMAN_SAMPLE = "Zwei Begriffe, die nicht unbedingt zueinander passen, am Arbeitsplatz schon mal gar nicht."
    UNKNOWN_SAMPLE = "Helium is material."
    SECRET_SAMPLE = """ Некој е болен и тој не е слободен. Dлетува гол во дупка од мраз. 
    И пее, а плаче од болка. Дали е ова контраст, можеби – живот?"""

    # score 6, params: k = 5, trie_level = 2
    # predict UNKNOWN_SAMPLE
    k = 5
    trie_levels = (2, 3)
    storage = LetterStorage()
    en_profile = create_profile_from_text(ENG_SAMPLE, storage, trie_levels, 'en')
    de_profile = create_profile_from_text(GERMAN_SAMPLE, storage, trie_levels, 'de')
    unknown_profile = create_profile_from_text(UNKNOWN_SAMPLE, storage, trie_levels, 'unknown')

    EN_DISTANCE = calculate_distance(unknown_profile, en_profile, k, (2,))
    DE_DISTANCE = calculate_distance(unknown_profile, de_profile, k, (2,))

    EXPECTED_DISTANCE_TO_EN_DE_PROFILES = 17, 25
    assert EN_DISTANCE, EXPECTED_DISTANCE_TO_EN_DE_PROFILES[0]
    assert DE_DISTANCE, EXPECTED_DISTANCE_TO_EN_DE_PROFILES[1]

    # score 8, k = 5, trie_level = 3
    # predict UNKNOWN_SAMPLE

    detector = LanguageDetector()
    detector.register_language(en_profile)
    detector.register_language(de_profile)

    ACTUAL_SCORE = detector.detect(unknown_profile, k, (3,))
    EXPECTED_SCORE = {'en': 24, 'de': 25}
    assert ACTUAL_SCORE == EXPECTED_SCORE

    # score 10, k = 1000, trie_levels = (2,)
    # predict SECRET_SAMPLE
    # print(detector.detect(unknown_profile, 1000, (2,)))
    # EXPECTED_LANGUAGE = ?
    # EXPECTED_MIN_DISTANCE = ?
    storage = LetterStorage()
    unknown_profile = create_profile_from_text(SECRET_SAMPLE, storage, trie_levels, 'unknown')
    detector = ProbabilityLanguageDetector()
    for file_name in os.listdir("profiles"):
        profile = LanguageProfile(storage, file_name)
        profile.open(f"profiles/{file_name}")
        detector.register_language(profile)
    probabilities = detector.detect(unknown_profile, 1000, (2,))
    predicted_language = min(probabilities, key=probabilities.get)
    print(predicted_language, probabilities[predicted_language])

    #RESULT = ''
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    #assert RESULT, 'Detection not working'

