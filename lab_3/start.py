"""
Language detection starter
"""

import os
import lab_3.main

PATH_TO_LAB_FOLDER = os.path.dirname(os.path.abspath(__file__))

if __name__ == '__main__':
    ENG_SAMPLE = "Helium is the byproduct of millennia of radioactive decay from " \
                 "the elements thorium and uranium."
    GERMAN_SAMPLE = "Zwei Begriffe, die nicht unbedingt zueinander passen, " \
                    "am Arbeitsplatz schon mal gar nicht."
    UNKNOWN_SAMPLE = "Helium is material."
    SECRET_SAMPLE = """ Некој е болен и тој не е слободен. Dлетува гол во дупка од мраз.
    И пее, а плаче од болка. Дали е ова контраст, можеби – живот?"""

    # score 6, params: k = 5, trie_level = 2
    def score_6():
        #TOKENS
        eng_sample_tokens = lab_3.main.tokenize_by_sentence(ENG_SAMPLE)
        de_sample_tokens = lab_3.main.tokenize_by_sentence(GERMAN_SAMPLE)
        unk_sample_tokens = lab_3.main.tokenize_by_sentence(UNKNOWN_SAMPLE)
        #STORAGE
        storage = lab_3.main.LetterStorage()
        storage.update(eng_sample_tokens)
        storage.update(de_sample_tokens)
        storage.update(unk_sample_tokens)
        #ENCODE
        encoded_eng = lab_3.main.encode_corpus(storage, eng_sample_tokens)
        encoded_de = lab_3.main.encode_corpus(storage, de_sample_tokens)
        encoded_unk = lab_3.main.encode_corpus(storage, unk_sample_tokens)
        #PROFILES
        en_profile = lab_3.main.LanguageProfile(storage, 'en')
        de_profile = lab_3.main.LanguageProfile(storage, 'de')
        unk_profile = lab_3.main.LanguageProfile(storage, 'unk')
        en_profile.create_from_tokens(encoded_eng, (2, ))
        de_profile.create_from_tokens(encoded_de, (2, ))
        unk_profile.create_from_tokens(encoded_unk, (2, ))
        #DISTANCE
        un_en_distance = lab_3.main.calculate_distance(unk_profile, en_profile, 5, 2)
        un_de_distance = lab_3.main.calculate_distance(unk_profile, de_profile, 5, 2)
        # predict UNKNOWN_SAMPLE
        print(un_en_distance)
        print(un_de_distance)
        #EXPECTED_DISTANCE_TO_EN_DE_PROFILES = 17, 25

    # score 8, k = 5, trie_level = 3
    def score_8():
        # TOKENS
        eng_sample_tokens = lab_3.main.tokenize_by_sentence(ENG_SAMPLE)
        de_sample_tokens = lab_3.main.tokenize_by_sentence(GERMAN_SAMPLE)
        unk_sample_tokens = lab_3.main.tokenize_by_sentence(UNKNOWN_SAMPLE)
        # STORAGE
        storage = lab_3.main.LetterStorage()
        storage.update(eng_sample_tokens)
        storage.update(de_sample_tokens)
        storage.update(unk_sample_tokens)
        # ENCODE
        encoded_eng = lab_3.main.encode_corpus(storage, eng_sample_tokens)
        encoded_de = lab_3.main.encode_corpus(storage, de_sample_tokens)
        encoded_unk = lab_3.main.encode_corpus(storage, unk_sample_tokens)
        # PROFILES
        en_profile = lab_3.main.LanguageProfile(storage, 'en')
        de_profile = lab_3.main.LanguageProfile(storage, 'de')
        unk_profile = lab_3.main.LanguageProfile(storage, 'unk')
        en_profile.create_from_tokens(encoded_eng, (3,))
        de_profile.create_from_tokens(encoded_de, (3,))
        unk_profile.create_from_tokens(encoded_unk, (3,))
        #FILE
        unk_profile.save('unk_profile.json')
        unk_profile.open('unk_profile.json')
        #DETECTOR
        detector = lab_3.main.LanguageDetector()
        detector.register_language(en_profile)
        detector.register_language(de_profile)
        # predict UNKNOWN_SAMPLE
        print(detector.detect(unk_profile, 5, (3,)))
        #EXPECTED_SCORE = {'en': 24, 'de': 25}

    # score 10, k = 1000, trie_levels = (2,)
    # predict SECRET_SAMPLE
    # print(detector.detect(unknown_profile, 1000, (2,)))
    # EXPECTED_LANGUAGE = ?
    # EXPECTED_MIN_DISTANCE = ?
    RESULT = score_8()
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT, 'Detection not working'