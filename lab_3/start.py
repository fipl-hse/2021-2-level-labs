"""
Language detection starter
"""

import os
from lab_3.main import LetterStorage, LanguageProfile, LanguageDetector, \
    tokenize_by_sentence, encode_corpus, calculate_distance

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
        # score 6, params: k = 5, trie_level = 2
        # predict UNKNOWN_SAMPLE
        # print(calculate_distance(unknown_profile, en_profile, 5, 2))
        # print(calculate_distance(unknown_profile, de_profile, 5, 2))
        eng_text = tokenize_by_sentence(ENG_SAMPLE)
        de_text = tokenize_by_sentence(GERMAN_SAMPLE)
        unknown_text = tokenize_by_sentence(UNKNOWN_SAMPLE)

        storage = LetterStorage()
        storage.update(eng_text)
        storage.update(de_text)
        storage.update(unknown_text)

        encoded_eng_text = encode_corpus(storage, eng_text)
        encoded_de_text = encode_corpus(storage, de_text)
        encoded_unknown_text = encode_corpus(storage, unknown_text)

        profile_en = LanguageProfile(letter_storage=storage, language_name='en')
        profile_en.create_from_tokens(encoded_eng_text, (2,))

        profile_de = LanguageProfile(letter_storage=storage, language_name='de')
        profile_de.create_from_tokens(encoded_de_text, (2,))

        unknown_profile = LanguageProfile(letter_storage=storage, language_name='unk')
        unknown_profile.create_from_tokens(encoded_unknown_text, (2,))

        print(calculate_distance(unknown_profile, profile_en, 5, 2))
        print(calculate_distance(unknown_profile, profile_de, 5, 2))


    get_6_score()



    def get_8_score():
        # score 8, k = 5, trie_level = 3
        # predict UNKNOWN_SAMPLE
        # print(detector.detect(profile_unk, 5, 3))
        # EXPECTED_SCORE = {'en': 24, 'de': 25}

        eng_text = tokenize_by_sentence(ENG_SAMPLE)
        de_text = tokenize_by_sentence(GERMAN_SAMPLE)
        unknown_text = tokenize_by_sentence(UNKNOWN_SAMPLE)

        storage = LetterStorage()
        storage.update(eng_text)
        storage.update(de_text)
        storage.update(unknown_text)

        encoded_eng_text = encode_corpus(storage, eng_text)
        encoded_de_text = encode_corpus(storage, de_text)
        encoded_unknown_text = encode_corpus(storage, unknown_text)

        profile_en = LanguageProfile(letter_storage=storage, language_name='en')
        profile_en.create_from_tokens(encoded_eng_text, (3,))

        profile_de = LanguageProfile(letter_storage=storage, language_name='de')
        profile_de.create_from_tokens(encoded_de_text, (3,))

        unknown_profile_1 = LanguageProfile(letter_storage=storage, language_name='unk')
        unknown_profile_1.create_from_tokens(encoded_unknown_text, (3,))

        unknown_profile_1.save('unknown_profile.json')

        unknown_profile_2 = LanguageProfile(letter_storage=storage, language_name='unk')
        unknown_profile_2.open('unknown_profile.json')

        detector = LanguageDetector()
        detector.register_language(profile_en)
        detector.register_language(profile_de)
        print(detector.detect(unknown_profile_2, 5, (3,)))


    get_8_score()



    # score 10, k = 1000, trie_levels = (2,)
    # predict SECRET_SAMPLE
    # print(detector.detect(unknown_profile, 1000, (2,)))
    # EXPECTED_LANGUAGE = ?
    # EXPECTED_MIN_DISTANCE = ?

    RESULT = ''
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT, 'Detection not working'
