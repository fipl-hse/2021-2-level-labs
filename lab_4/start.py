"""
Language generation starter
"""

import os
from lab_4.main import tokenize_by_letters, LetterStorage, LanguageProfile, \
    NGramTextGenerator, encode_corpus, decode_sentence, translate_sentence_to_plain_text, \
    LikelihoodBasedTextGenerator


PATH_TO_LAB_FOLDER = os.path.dirname(os.path.abspath(__file__))
PATH_TO_TEXT_FOLDER = os.path.join(PATH_TO_LAB_FOLDER)

if __name__ == '__main__':

    # find the appropriate start.py task in your lab_4 description file
    # your code goes here

    with open(os.path.join(PATH_TO_TEXT_FOLDER, 'reference_text.txt'), 'r',
              encoding='utf-8') as file_to_read:
        reference_text = file_to_read.read()

    #score 4
    TOKENIZED_TEXT = tokenize_by_letters(reference_text)
    STORAGE = LetterStorage()
    STORAGE.update(TOKENIZED_TEXT)

    NUM_OF_LETTERS = STORAGE.get_letter_count()
    LOWEST_ID = list(STORAGE.storage.keys())
    HIGHEST_ID = list(STORAGE.storage.keys())

    print('The number of letters is:', NUM_OF_LETTERS)
    print('5 letters with the lowest id:', LOWEST_ID[:5])
    print('5 letters with the highest id:', HIGHEST_ID[-5:])

    #score 6

    ENCODED = encode_corpus(STORAGE, TOKENIZED_TEXT)
    PROFILE = LanguageProfile(STORAGE, 'en')
    PROFILE.create_from_tokens(ENCODED, (2,))

    GENERATOR = NGramTextGenerator(PROFILE)
    GENERATED_TEXT = GENERATOR.generate_sentence((8,), 10)
    DECODED = decode_sentence(STORAGE, GENERATED_TEXT)

    RESULT_FOR_6 = translate_sentence_to_plain_text(DECODED)

    #score 8

    LIKELIHOOD_GENERATOR = LikelihoodBasedTextGenerator(PROFILE)
    RESULT_FOR_8 = LIKELIHOOD_GENERATOR.generate_decoded_sentence((8,), 10)

    print(RESULT_FOR_6)
    print(RESULT_FOR_8)
    RESULT = RESULT_FOR_8
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT, 'Detection not working'
