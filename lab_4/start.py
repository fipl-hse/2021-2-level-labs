"""
Language generation starter
"""

import os
from lab_4.main import (
    tokenize_by_letters,
    encode_corpus,
    LetterStorage,
    LanguageProfile,
    NGramTextGenerator,
    LikelihoodBasedTextGenerator
)

PATH_TO_LAB_FOLDER = os.path.dirname(os.path.abspath(__file__))

if __name__ == '__main__':

    # find the appropriate start.py task in your lab_4 description file
    # your code goes here

    with open("reference_text.txt", encoding="utf-8") as f:
        print("--- 4 ---")
        corpus = tokenize_by_letters(f.read())
        storage = LetterStorage()
        storage.update(corpus)
        print(len(storage.storage))
        print(list(storage.storage.items())[:5])
        print(list(storage.storage.items())[-5:])

        print("--- 6 ---")
        profile = LanguageProfile(storage, "idk")
        profile.create_from_tokens(encode_corpus(storage, corpus), (1, 2, 3, 4,))
        generator = NGramTextGenerator(profile)
        for length in range(5, 11):
            print(generator.generate_decoded_sentence((1, 2, 3,), length))

        print("--- 8 ---")
        generator = LikelihoodBasedTextGenerator(profile)
        for length in range(5, 11):
            print(generator.generate_decoded_sentence((1, 2, 3,), length))

    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    # assert RESULT, 'Detection not working'
