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

    eng_profile = LanguageProfile(storage, 'en')
    de_profile = LanguageProfile(storage, 'de')
    unk_profile = LanguageProfile(storage, 'unk')


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
        return prediction_dist_eng, prediction_dist_de


    ACTUAL_6 = score_6()
    EXPECTED_DISTANCE_TO_EN_DE_PROFILES = 17, 25
    assert ACTUAL_6 == EXPECTED_DISTANCE_TO_EN_DE_PROFILES, 'Detection not working'

    # RESULT = ''
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    # assert RESULT, 'Detection not working'
