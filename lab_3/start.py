"""
Language detection starter
"""

import os

from lab_3.main import tokenize_by_sentence, LetterStorage, encode_corpus, LanguageProfile, calculate_distance

PATH_TO_LAB_FOLDER = os.path.dirname(os.path.abspath(__file__))

if __name__ == '__main__':
    ENG_SAMPLE = "Helium is the byproduct of millennia of radioactive decay from the elements thorium and uranium."
    GERMAN_SAMPLE = "Zwei Begriffe, die nicht unbedingt zueinander passen, am Arbeitsplatz schon mal gar nicht."
    UNKNOWN_SAMPLE = "Helium is material."
    SECRET_SAMPLE = """ Некој е болен и тој не е слободен. Dлетува гол во дупка од мраз. 
    И пее, а плаче од болка. Дали е ова контраст, можеби – живот?"""
    # score 6, params: k = 5, trie_level = 2
    # predict UNKNOWN_SAMPLE
    # print(calculate_distance(unknown_profile, en_profile, 5, 2))
    # print(calculate_distance(unknown_profile, de_profile, 5, 2))
    EXPECTED_DISTANCE_TO_EN_DE_PROFILES = 17, 25

    RESULT = ''
    tokenized_unk = tokenize_by_sentence(UNKNOWN_SAMPLE)
    letter_storage = LetterStorage()
    letter_storage.update(tokenized_unk)
    encoded_unk_corpus = encode_corpus(letter_storage, tokenized_unk)
    unknown_profile = LanguageProfile(letter_storage=letter_storage, language_name='unk')
    unknown_profile.create_from_tokens(encoded_unk_corpus, (2,))

    tokenized_eng = tokenize_by_sentence(ENG_SAMPLE)
    letter_storage.update(tokenized_eng)
    encoded_eng_corpus = encode_corpus(letter_storage, tokenized_eng)
    eng_profile = LanguageProfile(letter_storage=letter_storage, language_name='eng')
    eng_profile.create_from_tokens(encoded_eng_corpus, (2,))

    tokenized_de = tokenize_by_sentence(GERMAN_SAMPLE)
    letter_storage.update(tokenized_de)
    encoded_de_corpus = encode_corpus(letter_storage, tokenized_de)
    de_profile = LanguageProfile(letter_storage=letter_storage, language_name='de')
    de_profile.create_from_tokens(encoded_de_corpus, (2,))

    eng_distance = calculate_distance(unknown_profile, eng_profile, 5, 2)
    de_distance = calculate_distance(unknown_profile, de_profile, 5, 2)
    if eng_distance == EXPECTED_DISTANCE_TO_EN_DE_PROFILES[0] and\
        de_distance == EXPECTED_DISTANCE_TO_EN_DE_PROFILES[1]:
        RESULT = [eng_distance, de_distance]
    print(RESULT)
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT, 'Detection not working'


