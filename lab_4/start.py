"""
Language generation starter
"""

import os
from lab_4.main import (tokenize_by_letters, LetterStorage, encode_corpus,
                        LanguageProfile, NGramTextGenerator,
                        LikelihoodBasedTextGenerator)

PATH_TO_LAB_FOLDER = os.path.dirname(os.path.abspath(__file__))

if __name__ == '__main__':
    # find the appropriate start.py task in your lab_4 description file
    # your code goes here

    with open(os.path.join(PATH_TO_LAB_FOLDER, 'reference_text.txt'), 'r',
              encoding='utf-8') as file_to_read:
        reference_text = file_to_read.read()

    tokenized_text = tokenize_by_letters(reference_text)
    storage = LetterStorage()
    storage.update(tokenized_text)

    encoded_text = encode_corpus(storage, tokenized_text)
    profile = LanguageProfile(storage, "en")
    profile.create_from_tokens(encoded_text, (2,))

    # score 4
    def score_4():
        print('The number of letters: ', storage.get_letter_count())
        print('The letters with the lowest ids: ', list(storage.storage)[:5])
        print('The letters with the highest ids: ', list(storage.storage)[-5:])

    # score 6
    def score_6():
        text_generator = NGramTextGenerator(profile)
        sentence = text_generator.generate_decoded_sentence((1,), 5)
        print(sentence)
        return sentence

    # score 8
    def score_8():
        text_generator = LikelihoodBasedTextGenerator(profile)
        sentence = text_generator.generate_decoded_sentence((1,), 5)
        print(sentence)
        return sentence


    score_4()
    score_6()
    RESULT = score_8()
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT, 'Detection not working'
