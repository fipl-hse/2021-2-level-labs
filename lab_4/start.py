"""
Language generation starter
"""

import os
from lab_4.main import tokenize_by_letters, LetterStorage, LanguageProfile, \
    NGramTextGenerator, encode_corpus, decode_sentence, translate_sentence_to_plain_text


PATH_TO_LAB_FOLDER = os.path.dirname(os.path.abspath(__file__))
PATH_TO_TEXT_FOLDER = os.path.join(PATH_TO_LAB_FOLDER)

if __name__ == '__main__':

    # find the appropriate start.py task in your lab_4 description file
    # your code goes here

    with open(os.path.join(PATH_TO_TEXT_FOLDER, 'reference_text.txt'), 'r',
              encoding='utf-8') as file_to_read:
        reference_text = file_to_read.read()

    #score 4
    tokenized_text = tokenize_by_letters(reference_text)
    storage = LetterStorage()
    storage.update(tokenized_text)

    num_of_letters = storage.get_letter_count()
    lowest_id = list(storage.storage.keys())
    highest_id = list(storage.storage.keys())

    print('The number of letters is:', num_of_letters)
    print('5 letters with the lowest id:', lowest_id[:5])
    print('5 letters with the highest id:', highest_id[-5:])

    #score 6

    encoded = encode_corpus(storage, tokenized_text)
    profile = LanguageProfile(storage, 'en')
    profile.create_from_tokens(encoded, (2,))

    generator = NGramTextGenerator(profile)
    generated_text = generator.generate_sentence((3,), 10)
    decoded = decode_sentence(storage, generated_text)

    RESULT_FOR_6 = translate_sentence_to_plain_text(decoded)
    print(RESULT_FOR_6)
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT_FOR_6, 'Detection not working'
