"""
Language generation starter
"""

import os
from lab_4.main import tokenize_by_letters, LetterStorage, encode_corpus, NGramTextGenerator, \
    LikelihoodBasedTextGenerator
from lab_4.language_profile import LanguageProfile


PATH_TO_LAB_FOLDER = os.path.dirname(os.path.abspath(__file__))
PATH_TO_TEXT_FOLDER = os.path.join(PATH_TO_LAB_FOLDER)

if __name__ == '__main__':

    # find the appropriate start.py task in your lab_4 description file
    # your code goes here

    with open(os.path.join(PATH_TO_TEXT_FOLDER, 'reference_text.txt'), 'r', encoding='utf-8') \
            as read_text:
        CORPUS = read_text.read()

    # for score 4

    TOKENIZED_CORPUS = tokenize_by_letters(CORPUS)

    ENG_STORAGE = LetterStorage()
    ENG_STORAGE.update(TOKENIZED_CORPUS)

    print('the number of letters is: ', ENG_STORAGE.get_letter_count())
    print('first five letters are: ', list(ENG_STORAGE.storage)[1:6])
    print('last five letters are: ', list(ENG_STORAGE.storage)[-5:])

    # for score 6

    ENCODED_CORPUS = encode_corpus(ENG_STORAGE, TOKENIZED_CORPUS)
    PROFILE = LanguageProfile(ENG_STORAGE, 'en')
    PROFILE.create_from_tokens(ENCODED_CORPUS, (2,))
    TEXT_GENERATOR = NGramTextGenerator(PROFILE)
    print(TEXT_GENERATOR.generate_decoded_sentence((10,), 5))
    print(TEXT_GENERATOR.generate_decoded_sentence((13,), 6))
    print(TEXT_GENERATOR.generate_decoded_sentence((7,), 7))

    # for score 8

    LIKELIHOOD_TEXT_GENERATOR = LikelihoodBasedTextGenerator(PROFILE)
    print(LIKELIHOOD_TEXT_GENERATOR.generate_decoded_sentence((6,), 6))
    print(LIKELIHOOD_TEXT_GENERATOR.generate_decoded_sentence((2,), 5))
    print(LIKELIHOOD_TEXT_GENERATOR.generate_decoded_sentence((1,), 7))

    RESULT = ''
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    # assert RESULT, 'Detection not working'
