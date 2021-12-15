"""
Language generator starter
"""

import os
from lab_4.main import tokenize_by_letters, LetterStorage, LanguageProfile, \
    NGramTextGenerator, encode_corpus, LikelihoodBasedTextGenerator

PATH_TO_LAB_FOLDER = os.path.dirname(os.path.abspath(__file__))

if __name__ == '__main__':
    with open(os.path.join(PATH_TO_LAB_FOLDER, 'reference_text.txt'),
              'r', encoding='utf-8') as file_to_read:
        REFERENCE_TEXT = file_to_read.read()

    TOKENIZED_TEXT = tokenize_by_letters(REFERENCE_TEXT)
    storage = LetterStorage()
    storage.update(TOKENIZED_TEXT)

    # SCORE 4
    print('the number of letters in the storage:', storage.get_letter_count())
    print('top 5 with lowest id:', list(storage.storage.keys())[:5])
    print('top 5 with highest id:', list(storage.storage.keys())[-5:])

    # SCORE 6
    encoded = encode_corpus(storage, TOKENIZED_TEXT)
    profile = LanguageProfile(storage, 'en')
    profile.create_from_tokens(encoded, (2,))

    text_generator = NGramTextGenerator(profile)
    print('')
    print('SCORE 6')
    print(text_generator.generate_decoded_sentence((1,), 10))
    print(text_generator.generate_decoded_sentence((16,), 7))
    print(text_generator.generate_decoded_sentence((5,), 9))

    # SCORE 8
    likelihood_generator = LikelihoodBasedTextGenerator(profile)
    print('')
    print('SCORE 8')
    print(likelihood_generator.generate_decoded_sentence((3,), 6))
    print(likelihood_generator.generate_decoded_sentence((8,), 7))
    print(likelihood_generator.generate_decoded_sentence((20,), 9))

    RESULT = 'It works^^'
    print('')
    print(RESULT)
    assert RESULT, 'Detection is not working'
