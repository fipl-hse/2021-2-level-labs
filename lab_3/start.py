"""
Language detection starter
"""

import os

from lab_3.main import tokenize_by_sentence, LetterStorage, \
    encode_corpus, LanguageProfile, calculate_distance, \
    LanguageDetector, ProbabilityLanguageDetector

PATH_TO_LAB_FOLDER = os.path.dirname(os.path.abspath(__file__))

if __name__ == '__main__':
    ENG_SAMPLE = "Helium is the byproduct of millennia of radioactive decay " \
                 "from the elements thorium and uranium."
    GERMAN_SAMPLE = "Zwei Begriffe, die nicht unbedingt zueinander passen, " \
                    "am Arbeitsplatz schon mal gar nicht."
    UNKNOWN_SAMPLE = "Helium is material."
    SECRET_SAMPLE = " Некој е болен и тој не е слободен. Dлетува гол во дупка од мраз. " \
                    "И пее, а плаче од болка. Дали е ова контраст, можеби – живот?"

    en_text = tokenize_by_sentence(ENG_SAMPLE)
    de_text = tokenize_by_sentence(GERMAN_SAMPLE)
    unknown_text = tokenize_by_sentence(UNKNOWN_SAMPLE)
    secret_text = tokenize_by_sentence(SECRET_SAMPLE)

    storage = LetterStorage()
    storage.update(en_text)
    storage.update(de_text)
    storage.update(unknown_text)
    storage.update(secret_text)

    encoded_en_text = encode_corpus(storage, en_text)
    encoded_de_text = encode_corpus(storage, de_text)
    encoded_unknown_text = encode_corpus(storage, unknown_text)
    encoded_secret_text = encode_corpus(storage, secret_text)

    # score 6, params: k = 5, trie_level = 2
    # predict UNKNOWN_SAMPLE
    # print(calculate_distance(unknown_profile, en_profile, 5, 2))
    # print(calculate_distance(unknown_profile, de_profile, 5, 2))

    en_profile_6 = LanguageProfile(letter_storage=storage, language_name='en')
    en_profile_6.create_from_tokens(encoded_en_text, (2,))

    de_profile_6 = LanguageProfile(letter_storage=storage, language_name='de')
    de_profile_6.create_from_tokens(encoded_de_text, (2,))

    unknown_profile_6 = LanguageProfile(letter_storage=storage, language_name='unknown')
    unknown_profile_6.create_from_tokens(encoded_unknown_text, (2,))

    distance_en_to_unknown_6 = calculate_distance(unknown_profile_6, en_profile_6, 5, 2)
    distance_de_to_unknown_6 = calculate_distance(unknown_profile_6, de_profile_6, 5, 2)
    print(f"DISTANCE_TO_EN_DE_PROFILES = {str(distance_en_to_unknown_6)}, "
          f"{str(distance_de_to_unknown_6)}")
    EXPECTED_DISTANCE_TO_EN_DE_PROFILES = 17, 25

    # score 8, k = 5, trie_level = 3
    # predict UNKNOWN_SAMPLE
    # print(detector.detect(profile_unk, 5, 3))
    # EXPECTED_SCORE = {'en': 24, 'de': 25}

    en_profile_8 = LanguageProfile(letter_storage=storage, language_name='en')
    de_profile_8 = LanguageProfile(letter_storage=storage, language_name='de')
    unknown_profile_8 = LanguageProfile(letter_storage=storage, language_name='unk')

    en_profile_8.create_from_tokens(encoded_en_text, (5, 3))
    de_profile_8.create_from_tokens(encoded_de_text, (5, 3))
    unknown_profile_8.create_from_tokens(encoded_unknown_text, (5, 3))

    calculate_distance(unknown_profile_8, en_profile_8, 5, 3)
    calculate_distance(unknown_profile_8, de_profile_8, 5, 3)

    unknown_profile_8.save('unknown_profile.json')
    profile_unk = LanguageProfile(letter_storage=storage, language_name='unk')
    profile_unk.open('unknown_profile.json')

    detector = LanguageDetector()

    detector.register_language(en_profile_8)
    detector.register_language(de_profile_8)

    print(f"EXPECTED_SCORE = {detector.detect(profile_unk, 5, (3,))}")

    # score 10, k = 1000, trie_levels = (2,)
    # predict SECRET_SAMPLE
    # print(detector.detect(unknown_profile, 1000, (2,)))
    # EXPECTED_LANGUAGE = ?
    # EXPECTED_MIN_DISTANCE = ?

    secret_profile = LanguageProfile(letter_storage=storage, language_name='secret')
    secret_profile.create_from_tokens(encoded_secret_text, (2,))
    detector = ProbabilityLanguageDetector()

    for file_name in os.listdir(os.path.join(PATH_TO_LAB_FOLDER, 'profiles')):
        profile = LanguageProfile(letter_storage=storage, language_name=file_name)
        profile.open(os.path.join(PATH_TO_LAB_FOLDER, 'profiles', file_name))
        detector.register_language(profile)

    probabilities = detector.detect(secret_profile, 1000, (2,))
    predicted_language = min(probabilities, key=probabilities.get)

    print(f'EXPECTED_LANGUAGE = {predicted_language[0]}. '
          f'EXPECTED_MIN_DISTANCE = {probabilities[predicted_language]}')

    RESULT = ''
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT, 'Detection not working'
