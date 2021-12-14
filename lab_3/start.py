"""
Language detection starter
"""

import os
from lab_3.main import (tokenize_by_sentence,
                        LetterStorage,
                        encode_corpus,
                        LanguageProfile,
                        calculate_distance,
                        LanguageDetector,
                        ProbabilityLanguageDetector)

PATH_TO_LAB_FOLDER = os.path.dirname(os.path.abspath(__file__))

if __name__ == '__main__':
    ENG_SAMPLE = "Helium is the byproduct of millennia of radioactive decay " \
                 "from the elements thorium and uranium."
    GERMAN_SAMPLE = "Zwei Begriffe, die nicht unbedingt zueinander passen, " \
                    "am Arbeitsplatz schon mal gar nicht."
    UNKNOWN_SAMPLE = "Helium is material."
    SECRET_SAMPLE = """ Некој е болен и тој не е слободен. Dлетува гол во дупка од мраз.
    И пее, а плаче од болка. Дали е ова контраст, можеби – живот?"""

    # use tokenize_by_sentence
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
    eng_profile = LanguageProfile(storage, 'en')
    de_profile = LanguageProfile(storage, 'de')
    unk_profile = LanguageProfile(storage, 'unk')
    # score 10
    secret_profile = LanguageProfile(storage, 'secret')


    def score_6(k=5, trie_level=2):
        """
        score 6, params: k = 5, trie_level = 2
        predict UNKNOWN_SAMPLE
        EXPECTED_DISTANCE_TO_EN_DE_PROFILES = 17, 25
        """
        # use create_from_tokens
        eng_profile.create_from_tokens(encoded_eng_text, (trie_level,))
        de_profile.create_from_tokens(encoded_de_text, (trie_level,))
        unk_profile.create_from_tokens(encoded_unk_text, (trie_level,))

        prediction_dist_eng = calculate_distance(unk_profile, eng_profile, k, trie_level)
        prediction_dist_de = calculate_distance(unk_profile, de_profile, k, trie_level)

        return prediction_dist_eng, prediction_dist_de


    def score_8(k=5, trie_level=3):
        """
        score 8, params: k = 5, trie_level = 3
        predict UNKNOWN_SAMPLE
        EXPECTED_SCORE = {'en': 24, 'de': 25}
        """
        # use create_from_tokens
        eng_profile.create_from_tokens(encoded_eng_text, (trie_level,))
        de_profile.create_from_tokens(encoded_de_text, (trie_level,))
        unk_profile.create_from_tokens(encoded_unk_text, (trie_level,))

        # use method register_language in LanguageDetector
        detector = LanguageDetector()

        detector.register_language(eng_profile)
        detector.register_language(de_profile)

        unk_profile.save('unk_profile.json')
        unk_profile.open('unk_profile.json')

        return detector.detect(unk_profile, k, (trie_level,))

    def score_10(k=1000, trie_levels=(2,)):
        """
        score 10, params: k = 1000, trie_levels = (2,)
        predict SECRET_SAMPLE
        EXPECTED_LANGUAGE = ?
        EXPECTED_MIN_DISTANCE = ?
        """
        # use create_from_tokens
        secret_profile.create_from_tokens(encoded_secret_text, trie_levels)

        detector = ProbabilityLanguageDetector()

        for file_name in os.listdir(os.path.join(PATH_TO_LAB_FOLDER, 'profiles')):
            profile = LanguageProfile(storage, file_name)
            profile.open(os.path.join(PATH_TO_LAB_FOLDER, 'profiles', file_name))
            detector.register_language(profile)

        probabilities = detector.detect(secret_profile, k, trie_levels)
        predicted_language = min(probabilities, key=probabilities.get)

        return predicted_language[0], probabilities[predicted_language]

    ACTUAL_6 = score_6()
    EXPECTED_DISTANCE_TO_EN_DE_PROFILES = 17, 25
    assert ACTUAL_6 == EXPECTED_DISTANCE_TO_EN_DE_PROFILES, 'Detection not working'

    RESULT = score_8()
    EXPECTED_SCORE = {'en': 24, 'de': 25}
    assert ACTUAL_8 == EXPECTED_SCORE, 'Detection not working'

    EXPECTED_LANGUAGE = score_10()[0]
    EXPECTED_MIN_DISTANCE = score_10()[1]
    print(EXPECTED_LANGUAGE, EXPECTED_MIN_DISTANCE)

    def get_6_score():
        """ score 6, params: k = 5, trie_level = 2
            predict UNKNOWN_SAMPLE
            print(calculate_distance(unknown_profile, en_profile, 5, 2))
            print(calculate_distance(unknown_profile, de_profile, 5, 2))"""
        eng_text = tokenize_by_sentence(ENG_SAMPLE)
        de_text = tokenize_by_sentence(GERMAN_SAMPLE)
        unknown_text = tokenize_by_sentence(UNKNOWN_SAMPLE)
        letter_storage = LetterStorage()
        letter_storage.update(eng_text)
        letter_storage.update(de_text)
        letter_storage.update(unknown_text)
        encoded_eng_text = encode_corpus(letter_storage, eng_text)
        encoded_de_text = encode_corpus(letter_storage, de_text)
        encoded_unknown_text = encode_corpus(letter_storage, unknown_text)
        profile_en = LanguageProfile(letter_storage=letter_storage, language_name='en')
        profile_en.create_from_tokens(encoded_eng_text, (2,))
        profile_de = LanguageProfile(letter_storage=letter_storage, language_name='de')
        profile_de.create_from_tokens(encoded_de_text, (2,))
        unknown_profile = LanguageProfile(letter_storage=letter_storage, language_name='unk')
        unknown_profile.create_from_tokens(encoded_unknown_text, (2,))
        distance_en = calculate_distance(unknown_profile, profile_en, 5, 2)
        distance_de = calculate_distance(unknown_profile, profile_de, 5, 2)
        print(distance_en, distance_de)

    get_6_score()

    EXPECTED = {'en': 24, 'de': 25}

    def get_8_score():
        """ score 8, k = 5, trie_level = 3
            # predict UNKNOWN_SAMPLE
            # print(detector.detect(profile_unk, 5, 3))
            # EXPECTED_SCORE = {'en': 24, 'de': 25}"""
        eng_text = tokenize_by_sentence(ENG_SAMPLE)
        de_text = tokenize_by_sentence(GERMAN_SAMPLE)
        unknown_text = tokenize_by_sentence(UNKNOWN_SAMPLE)
        letter_storage = LetterStorage()
        letter_storage.update(eng_text)
        letter_storage.update(de_text)
        letter_storage.update(unknown_text)
        encoded_eng_text = encode_corpus(letter_storage, eng_text)
        encoded_de_text = encode_corpus(letter_storage, de_text)
        encoded_unknown_text = encode_corpus(letter_storage, unknown_text)
        profile_en = LanguageProfile(letter_storage=letter_storage, language_name='en')
        profile_en.create_from_tokens(encoded_eng_text, (3,2))
        profile_de = LanguageProfile(letter_storage=letter_storage, language_name='de')
        profile_de.create_from_tokens(encoded_de_text, (3,2))
        unknown_profile_1 = LanguageProfile(letter_storage=letter_storage, language_name='unk')
        unknown_profile_1.create_from_tokens(encoded_unknown_text, (3,2))
        unknown_profile_1.save('unknown_profile.json')
        unknown_profile_2 = LanguageProfile(letter_storage=letter_storage, language_name='unk')
        unknown_profile_2.open('unknown_profile.json')
        language_detector = LanguageDetector()
        language_detector.register_language(profile_en)
        language_detector.register_language(profile_de)
        result = language_detector.detect(unknown_profile_2, 5, (3,2))
        return result

    # score 10, k = 1000, trie_levels = (2,)
    # predict SECRET_SAMPLE
    # print(detector.detect(unknown_profile, 1000, (2,)))
    # EXPECTED_LANGUAGE = ?
    # EXPECTED_MIN_DISTANCE = ?

    RESULT = get_8_score()
    print(RESULT)

    # RESULT = ''

    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    # assert RESULT, 'Detection not working'
