"""
Language generation starter
"""

import os
from lab_4.main import (tokenize_by_letters,
                        decode_sentence,
                        LetterStorage,
                        encode_corpus,
                        LanguageProfile,
                        NGramTextGenerator,
                        translate_sentence_to_plain_text)
from random import randint

PATH_TO_LAB_FOLDER = os.path.dirname(os.path.abspath(__file__))

if __name__ == '__main__':

    with open(os.path.join(PATH_TO_LAB_FOLDER, 'reference_text.txt'), 'r', encoding='utf-8') as file_to_read_ref:
        reference_text = file_to_read_ref.read()

corpus = tokenize_by_letters(reference_text)
storage = LetterStorage()
storage.update(corpus)

    RESULT = storage.get_letter_count()
    print(f'total letter count: {RESULT}')
    
    top_index = sorted(storage.storage, key=storage.storage.get, reverse=True)
    print(f'letters with smallest indicators: {top_index[-1:-6:-1]}')
    print(f'letters with biggest indicators: {top_index[:5]}')
    
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT, 'Detection not working'
