"""
Language detection starter
"""

import os
from lab_3.main import LanguageProfile, LetterStorage, ProbabilityLanguageDetector, \
    tokenize_by_sentence, encode_corpus, NGramTrie, LanguageDetector, calculate_distance

PATH_TO_LAB_FOLDER = os.path.dirname(os.path.abspath(__file__))
PATH_TO_PROFILES_FOLDER = os.path.join(PATH_TO_LAB_FOLDER, 'profiles')
profiles = os.listdir(PATH_TO_PROFILES_FOLDER)

if __name__ == '__main__':
    ENG_SAMPLE = "Helium is the byproduct of millennia of radioactive decay " \
                 "from the elements thorium and uranium."
    GERMAN_SAMPLE = "Zwei Begriffe, die nicht unbedingt zueinander passen, " \
                    "am Arbeitsplatz schon mal gar nicht."
    UNKNOWN_SAMPLE = "Helium is material."
    SECRET_SAMPLE = """ Некој е болен и тој не е слободен. Dлетува гол во дупка од мраз.
        И пее, а плаче од болка. Дали е ова контраст, можеби – живот?"""
    # score 10, k = 1000, trie_levels = (2,)
    # predict SECRET_SAMPLE
    # print(detector.detect(unknown_profile, 1000, (2,)))
    # EXPECTED_LANGUAGE = ?
    # EXPECTED_MIN_DISTANCE = ?

    k = 1000
    trie_levels = (2,)
    unknown_text = tokenize_by_sentence(SECRET_SAMPLE)
    storage = LetterStorage()
    storage.update(unknown_text)
    encoded_unknown_text = encode_corpus(storage, unknown_text)
    unknown_profile = LanguageProfile(storage, 'unknown')

    unknown_profile.create_from_tokens(encoded_unknown_text, trie_levels)
    detector = ProbabilityLanguageDetector()

    for file_name in os.listdir(os.path.join(PATH_TO_LAB_FOLDER, 'profiles')):
        profile = LanguageProfile(storage, file_name)
        profile.open(os.path.join(PATH_TO_LAB_FOLDER, 'profiles', file_name))
        detector.register_language(profile)

    probabilities = detector.detect(unknown_profile, k, trie_levels)
    final_language = min(probabilities, key=probabilities.get)

    expected_language = final_language[0]
    expected_min_distance = probabilities[(expected_language, 2)]
    print(f'expected language is {expected_language} and expected min'
          f' distance is {expected_min_distance}')
    RESULT = expected_language
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    # assert RESULT, 'Detection not working'
