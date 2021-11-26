"""
Language detection starter
"""

import os
from lab_3.main import tokenize_by_sentence, LetterStorage, encode_corpus, decode_corpus

PATH_TO_LAB_FOLDER = os.path.dirname(os.path.abspath(__file__))

if __name__ == '__main__':
    ENG_SAMPLE = "Helium is the byproduct of millennia of radioactive decay from the elements thorium and uranium."
    GERMAN_SAMPLE = "Zwei Begriffe, die nicht unbedingt zueinander passen, am Arbeitsplatz schon mal gar nicht."
    UNKNOWN_SAMPLE = "Helium is material."
    SECRET_SAMPLE = """ Некој е болен и тој не е слободен. Dлетува гол во дупка од мраз. 
    И пее, а плаче од болка. Дали е ова контраст, можеби – живот?"""


    EXPECTED_DISTANCE_TO_EN_DE_PROFILES = 17, 25


    eng_tokenize = tokenize_by_sentence(ENG_SAMPLE)
    german_tokenize = tokenize_by_sentence(GERMAN_SAMPLE)
    unknown_tokenize = tokenize_by_sentence(UNKNOWN_SAMPLE)

    print(eng_tokenize, german_tokenize, unknown_tokenize)

    storage = LetterStorage()
    storage.update(eng_tokenize)
    storage.update(german_tokenize)
    storage.update(unknown_tokenize)

    eng_tokenize_encoded = encode_corpus(storage, eng_tokenize)
    german_tokenize_encoded = encode_corpus(storage, german_tokenize)
    unknown_tokenize_encoded = encode_corpus(storage, unknown_tokenize)

    print(eng_tokenize_encoded, german_tokenize_encoded, unknown_tokenize_encoded)

    eng_tokenize_decoded = decode_corpus(storage, eng_tokenize_encoded)
    german_tokenize_decoded = decode_corpus(storage, german_tokenize_encoded)
    unknown_tokenize_decoded = decode_corpus(storage, unknown_tokenize_encoded)

    print(eng_tokenize_decoded, german_tokenize_decoded, unknown_tokenize_decoded)

    RESULT = f'{eng_tokenize_decoded}, {german_tokenize_decoded}, {unknown_tokenize_decoded}'


    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT, 'Detection not working'

