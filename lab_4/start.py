"""
Language generation starter
"""

import os
from lab_4 import main

PATH_TO_LAB_FOLDER = os.path.dirname(os.path.abspath(__file__))

if __name__ == '__main__':

    # find the appropriate start.py task in your lab_4 description file
    # your code goes here

    with open(os.path.join(PATH_TO_LAB_FOLDER, 'reference_text.txt'), 'r', encoding='utf-8') as file_to_read:
        reference_text = file_to_read.read()

    # 4
    tokenized_text = main.tokenize_by_letters(reference_text)
    storage = main.LetterStorage()
    storage.update(tokenized_text)

    num_of_letters = storage.get_letter_count()
    lowest_id = list(storage.storage.keys())
    highest_id = list(storage.storage.keys())

    print('Количество букв в хранилище:', num_of_letters)
    print('5 букв с наименьшим идентификатором:', lowest_id[:5])
    print('5 букв с наибольшим идентификатором:', highest_id[-5:])


    # 6
    encoded = main.encode_corpus(storage, tokenized_text)
    profile = main.LanguageProfile(storage, 'en')
    profile.create_from_tokens(encoded, (2,))

    generator = main.NGramTextGenerator(profile)
    generated_text = generator.generate_sentence((3,), 10)
    decoded = main.decode_sentence(storage, generated_text)

    RESULT = main.translate_sentence_to_plain_text(decoded)
    print(RESULT)

    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT, 'Detection not working'
