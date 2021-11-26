"""
Language detection starter
"""
from lab_3.main import *
import os

PATH_TO_LAB_FOLDER = os.path.dirname(os.path.abspath(__file__))

if __name__ == '__main__':
    ENG_SAMPLE = "Helium is the byproduct of millennia of radioactive decay from the elements thorium and uranium."
    GERMAN_SAMPLE = "Zwei Begriffe, die nicht unbedingt zueinander passen, am Arbeitsplatz schon mal gar nicht."
    UNKNOWN_SAMPLE = "Helium is material."
    SECRET_SAMPLE = """ Некој е болен и тој не е слободен. Dлетува гол во дупка од мраз. 
    И пее, а плаче од болка. Дали е ова контраст, можеби – живот?"""

    # tokenizing
    en_tokens = tokenize_by_sentence(ENG_SAMPLE)
    de_tokens = tokenize_by_sentence(GERMAN_SAMPLE)
    unk_tokens = tokenize_by_sentence(UNKNOWN_SAMPLE)

    # creating a storage
    storage = LetterStorage()
    storage.update(en_tokens)
    storage.update(de_tokens)
    storage.update(unk_tokens)

    en_text = encode_corpus(storage, en_tokens)
    de_text = encode_corpus(storage, de_tokens)
    unk_text = encode_corpus(storage, unk_tokens)

    unknown_profile = LanguageProfile(storage, 'unk')
    en_profile = LanguageProfile(storage, 'en')
    de_profile = LanguageProfile(storage, 'de')

    en_profile.create_from_tokens(en_text, (5, 2))
    de_profile.create_from_tokens(de_text, (5, 2))
    unknown_profile.create_from_tokens(unk_text, (5, 2))

    en_distance = calculate_distance(unknown_profile, en_profile, 5, 2)
    de_distance = calculate_distance(unknown_profile, de_profile, 5, 2)
    RESULT = en_distance, de_distance
    print(RESULT)
    EXPECTED_DISTANCE_TO_EN_DE_PROFILES = 17, 25

    # score 6, params: k = 5, trie_level = 2
    # predict UNKNOWN_SAMPLE
    # print(calculate_distance(unknown_profile, en_profile, 5, 2))
    # print(calculate_distance(unknown_profile, de_profile, 5, 2))
    # EXPECTED_DISTANCE_TO_EN_DE_PROFILES = 17, 25




    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST


    assert RESULT == EXPECTED_DISTANCE_TO_EN_DE_PROFILES, 'Detection not working'
