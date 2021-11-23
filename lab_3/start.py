"""
Language detection starter
"""

import os
from lab_3.main import (tokenize_by_sentence,
                        LetterStorage,
                        encode_corpus,
                        LanguageProfile,
                        calculate_distance,
                        LanguageDetector)

PATH_TO_LAB_FOLDER = os.path.dirname(os.path.abspath(__file__))

if __name__ == '__main__':
    ENG_SAMPLE = "Helium is the byproduct of millennia of radioactive decay " \
                 "from the elements thorium and uranium."
    GERMAN_SAMPLE = "Zwei Begriffe, die nicht unbedingt zueinander passen, " \
                    "am Arbeitsplatz schon mal gar nicht."
    UNKNOWN_SAMPLE = "Helium is material."
    SECRET_SAMPLE = """ Некој е болен и тој не е слободен. Dлетува гол во дупка од мраз. 
    И пее, а плаче од болка. Дали е ова контраст, можеби – живот?"""

    # use tokenize_by_sentence()
    # score 6-8
    eng_text = tokenize_by_sentence(ENG_SAMPLE)
    de_text = tokenize_by_sentence(GERMAN_SAMPLE)
    unk_text = tokenize_by_sentence(UNKNOWN_SAMPLE)
    # score 10 secret_text
    secret_text = tokenize_by_sentence(SECRET_SAMPLE)

    # use method update in LetterStorage
    # score 6-8
    storage = LetterStorage()
    storage.update(eng_text)
    storage.update(de_text)
    storage.update(unk_text)
    # score 10
    storage.update(secret_text)

    # use function encode_corpus
    # score 6-8
    encoded_eng_text = encode_corpus(storage, eng_text)
    encoded_de_text = encode_corpus(storage, de_text)
    encoded_unk_text = encode_corpus(storage, unk_text)
    # score 10
    encoded_secret_text = encode_corpus(storage, secret_text)

    # use LanguageProfile
    # score 6-8
    eng_profile = LanguageProfile(letter_storage=storage, language_name='en')
    de_profile = LanguageProfile(letter_storage=storage, language_name='de')
    unk_profile = LanguageProfile(letter_storage=storage, language_name='unk')
    # score 10
    secret_profile = LanguageProfile(letter_storage=storage, language_name='secret')

    # use method register_language in LanguageDetector
    # score 8
    detector = LanguageDetector()
    detector.register_language(eng_profile)
    detector.register_language(de_profile)
    # score 10
    profiles = []
    for file_name in os.listdir(os.path.join(PATH_TO_LAB_FOLDER, 'profiles')):
        profile = LanguageProfile(letter_storage=LetterStorage(), language_name=file_name)
        profile.open(os.path.join(PATH_TO_LAB_FOLDER, 'profiles', file_name))
        profiles.append(profile)
    for profile in profiles:
        detector.register_language(profile)

    def score_6(k=5, trie_level=2):
        """
        score 6, params: k = 5, trie_level = 2
        predict UNKNOWN_SAMPLE
        EXPECTED_DISTANCE_TO_EN_DE_PROFILES = 17, 25
        """
        eng_profile.create_from_tokens(encoded_eng_text, (trie_level,))
        de_profile.create_from_tokens(encoded_de_text, (trie_level,))
        unk_profile.create_from_tokens(encoded_unk_text, (trie_level,))

        prediction_dist_eng = calculate_distance(unk_profile, eng_profile, k, trie_level)
        prediction_dist_de = calculate_distance(unk_profile, de_profile, k, trie_level)
        print(prediction_dist_eng, prediction_dist_de)

    def score_8(k=5, trie_level=3):
        """
        score 8, params: k = 5, trie_level = 3
        predict UNKNOWN_SAMPLE
        EXPECTED_SCORE = {'en': 24, 'de': 25}
        """
        eng_profile.create_from_tokens(encoded_eng_text, (trie_level,))
        de_profile.create_from_tokens(encoded_de_text, (trie_level,))
        unk_profile.create_from_tokens(encoded_unk_text, (trie_level,))

        unk_profile.save('unk_profile.json')
        unk_profile.open('unk_profile.json')

        print(detector.detect(unk_profile, k, (trie_level,)))

    def score_10(k=1000, trie_levels=(2,)):
        """
        score 10, params: k = 1000, trie_levels = (2,)
        predict SECRET_SAMPLE
        EXPECTED_LANGUAGE = ?
        EXPECTED_MIN_DISTANCE = ?
        """
        results = detector.detect(secret_profile, k, trie_levels)
        closest_language = ()
        for language, distance in results.items():
            if not closest_language:
                closest_language = (language, distance)
            elif distance < closest_language[1]:
                closest_language = (language, distance)
        print(closest_language)
        # print(detector.detect(unknown_profile, 1000, (2,)))

    score_6()
    score_8()

    # RESULT = ''
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    # assert RESULT, 'Detection not working'

