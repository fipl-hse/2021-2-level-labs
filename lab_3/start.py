"""
Language detection starter
"""

import os
from lab_3.main import *

PATH_TO_LAB_FOLDER = os.path.dirname(os.path.abspath(__file__))


def score_6():
    eng_text = tokenize_by_sentence(ENG_SAMPLE)
    de_text = tokenize_by_sentence(GERMAN_SAMPLE)
    unk_text = tokenize_by_sentence(UNKNOWN_SAMPLE)
    storage = LetterStorage()
    storage.update(eng_text)
    storage.update(de_text)
    storage.update(unk_text)
    encoded_eng_text = encode_corpus(storage, eng_text)
    encoded_de_text = encode_corpus(storage, de_text)
    encoded_unk_text = encode_corpus(storage, unk_text)

    profile_en = LanguageProfile(letter_storage=storage, language_name='en')
    profile_en.create_from_tokens(encoded_eng_text, (2,))

    profile_de = LanguageProfile(letter_storage=storage, language_name='de')
    profile_de.create_from_tokens(encoded_de_text, (2,))

    unk_profile = LanguageProfile(letter_storage=storage, language_name='unk')
    unk_profile.create_from_tokens(encoded_unk_text, (2,))

    dist_eng_to_unk = calculate_distance(unk_profile, profile_en, 5, 2)
    dist_de_to_unk = calculate_distance(unk_profile, profile_de, 5, 2)

    print("Score 6: " + str(dist_eng_to_unk) + " " + str(dist_de_to_unk))


def score_8():
    eng_text = tokenize_by_sentence(ENG_SAMPLE)
    de_text = tokenize_by_sentence(GERMAN_SAMPLE)
    unk_text = tokenize_by_sentence(UNKNOWN_SAMPLE)
    storage = LetterStorage()
    storage.update(eng_text)
    storage.update(de_text)
    storage.update(unk_text)
    encoded_eng_text = encode_corpus(storage, eng_text)
    encoded_de_text = encode_corpus(storage, de_text)
    encoded_unk_text = encode_corpus(storage, unk_text)

    profile_en = LanguageProfile(letter_storage=storage, language_name='en')
    profile_en.create_from_tokens(encoded_eng_text, (3,))

    profile_de = LanguageProfile(letter_storage=storage, language_name='de')
    profile_de.create_from_tokens(encoded_de_text, (3,))

    unknown = LanguageProfile(letter_storage=storage, language_name='unk')
    unknown.create_from_tokens(encoded_unk_text, (3,))

    unknown.save('unknown_profile.json')

    unk_profile = LanguageProfile(letter_storage=storage, language_name='unk')
    unk_profile.open('unknown_profile.json')

    detector = LanguageDetector()
    detector.register_language(profile_en)
    detector.register_language(profile_de)

    print("Score 8: " + str(detector.detect(unk_profile, 5, (3,))))


def score_10():
    profiles = []

    for file_name in os.listdir(os.path.join(PATH_TO_LAB_FOLDER, 'profiles')):
        profile = LanguageProfile(letter_storage=LetterStorage(), language_name=file_name)
        profile.open(os.path.join(PATH_TO_LAB_FOLDER, 'profiles', file_name))
        profiles.append(profile)

    detector = LanguageDetector()

    for profile in profiles:
        detector.register_language(profile)

    unk_text = tokenize_by_sentence(SECRET_SAMPLE)
    storage = LetterStorage()
    storage.update(unk_text)
    encoded_unk_text = encode_corpus(storage, unk_text)

    unknown_profile = LanguageProfile(letter_storage=storage, language_name='unk')
    unknown_profile.create_from_tokens(encoded_unk_text, (2,))

    results = detector.detect(unknown_profile, 1000, (2,))

    closest_language = ()

    for language, distance in results.items():
        if not closest_language:
            closest_language = (language, distance)
        elif distance < closest_language[1]:
            closest_language = (language, distance)

    print("Score 10: " + str(closest_language))


if __name__ == '__main__':
    ENG_SAMPLE = "Helium is the byproduct of millennia of radioactive decay from the elements" \
                 " thorium and uranium."
    GERMAN_SAMPLE = "Zwei Begriffe, die nicht unbedingt zueinander passen, am Arbeitsplatz" \
                    " schon mal gar nicht."
    UNKNOWN_SAMPLE = "Helium is material."
    SECRET_SAMPLE = """ Некој е болен и тој не е слободен. Dлетува гол во дупка од мраз. 
    И пее, а плаче од болка. Дали е ова контраст, можеби – живот?"""

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

    score_8()

    # score 10, k = 1000, trie_levels = (2,)
    # predict SECRET_SAMPLE
    # print(detector.detect(unknown_profile, 1000, (2,)))
    # EXPECTED_LANGUAGE = ?
    # EXPECTED_MIN_DISTANCE = ?

    score_10()

    RESULT = ''
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT, 'Detection not working'

