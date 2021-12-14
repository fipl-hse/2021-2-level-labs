"""
Language generation starter
"""

import os
from lab_4.main import tokenize_by_letters, LetterStorage

PATH_TO_LAB_FOLDER = os.path.dirname(os.path.abspath(__file__))

if __name__ == '__main__':
    with open(os.path.join(PATH_TO_LAB_FOLDER, 'reference_text.txt'), 'r', encoding='utf-8') as fin:
        text = fin.read()

    tokenized_text = tokenize_by_letters(text)
    storage = LetterStorage()
    storage.update(tokenized_text)

    print('Count of letters: ', storage.get_letter_count())
    print('Top 5 lowest ids: ', list(storage.storage.items())[:5])
    print('Top 5 highest ids: ', list(storage.storage.items())[-5:])

    RESULT = storage.get_letter_count(), list(storage.storage.items())[:5], list(storage.storage.items())[-5:]
    assert RESULT, 'Detection not working'
