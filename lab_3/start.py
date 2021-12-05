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
    ENG_SAMPLE = "Helium is the byproduct of millennia of " \
                 "radioactive decay from the elements thorium and uranium."
    GERMAN_SAMPLE = "Zwei Begriffe, die nicht unbedingt " \
                    "zueinander passen, am Arbeitsplatz schon mal gar nicht."
    UNKNOWN_SAMPLE = "Helium is material."
    SECRET_SAMPLE = """ Некој е болен и тој не е слободен. Dлетува гол во дупка од мраз.
    И пее, а плаче од болка. Дали е ова контраст, можеби – живот?"""
    EXPECTED_DISTANCE_TO_EN_DE_PROFILES = 17, 25

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
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT == EXPECTED, 'Detection not working'
