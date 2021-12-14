"""
Language generation starter
"""
import os
from lab_4.main import (tokenize_by_letters,
                        LetterStorage,
                        encode_corpus,
                        LanguageProfile,
                        NGramTextGenerator,
                        LikelihoodBasedTextGenerator)
PATH_TO_LAB_FOLDER = os.path.dirname(os.path.abspath(__file__))
if __name__ == '__main__':
    # find the appropriate start.py task in your lab_4 description file
    # your code goes here
    with open(os.path.join(PATH_TO_LAB_FOLDER, 'reference_text.txt'), 'r',
              encoding='utf-8') as file_to_read:
        reference_text = file_to_read.read()
    tokenized = tokenize_by_letters(reference_text)
    storage = LetterStorage()
    storage.update(tokenized)
    # score 4
    print('The number of letters in the storage:', storage.get_letter_count())
    print('Top 5 letters with the lowest ids:', list(storage.storage.keys())[:5])
    print('Top 5 letters with the highest ids:', list(storage.storage.keys())[-5:])
    encoded = encode_corpus(storage, tokenized)
    en_profile = LanguageProfile(storage, 'en')
    en_profile.create_from_tokens(encoded, (2,))
    text_generator_6 = NGramTextGenerator(en_profile)
    sentence_6 = text_generator_6.generate_decoded_sentence((4,), 8)
    # score 6
    RESULT_6 = sentence_6
    print('Generated sentence for 6:', RESULT_6)
    RESULT_8 = []
    text_generator_8 = LikelihoodBasedTextGenerator(en_profile)
    for length in range(5, 10):
        RESULT_8.append(text_generator_8.generate_decoded_sentence((8,), length))

    # score 8
    print('Generated sentences for 8:', RESULT_8)

    RESULT = RESULT_8
    print(RESULT)
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT, 'Detection not working'
