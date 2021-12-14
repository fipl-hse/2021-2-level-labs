"""
Language generation starter
"""

import os
from lab_4.main import tokenize_by_letters, \
    LetterStorage, encode_corpus, \
    decode_sentence, LanguageProfile, \
    NGramTextGenerator, LikelihoodBasedTextGenerator

PATH_TO_LAB_FOLDER = os.path.dirname(os.path.abspath(__file__))
with open('reference_text.txt', 'r', encoding='utf-8') as file_to_read:
    text = file_to_read.read()

if __name__ == '__main__':

    # find the appropriate start.py task in your lab_4 description file
    # your code goes here

    tokenized_text = tokenize_by_letters(text)
    storage = LetterStorage()
    storage.update(tokenized_text)
    number_of_letters = storage.get_letter_count()
    lowest_id = list(storage.storage.keys())
    highest_id = list(storage.storage.keys())
    #print(number_of_letters)
    #print(lowest_id[:5])
    #print(highest_id[-5:])

    # score 6
    encoded = encode_corpus(storage, tokenized_text)
    profile = LanguageProfile(storage, 'en')
    profile.create_from_tokens(encoded, (2,))
    generator = NGramTextGenerator(profile)
    generated_text = generator.generate_sentence((3,), 10)
    decoded = decode_sentence(storage, generated_text)

    # score 8
    RESULT_8 = []
    text_generator_8 = LikelihoodBasedTextGenerator(profile)
    for length in range(5, 10):
        RESULT_8.append(text_generator_8.generate_decoded_sentence((8,), length))

    print('Generated sentence for 8:', RESULT_8)

    RESULT = RESULT_8
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT, 'Detection not working'


