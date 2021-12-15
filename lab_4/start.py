"""
Language generation starter
"""

import os
from lab_4.main import tokenize_by_letters, LetterStorage


PATH_TO_LAB_FOLDER = os.path.dirname(os.path.abspath(__file__))

if __name__ == '__main__':

    # find the appropriate start.py task in your lab_4 description file
    # your code goes here

    with open(os.path.join(PATH_TO_LAB_FOLDER, 'reference_text.txt'), 'r', encoding='utf-8') as file:
        text = file.read()
    tokenized_text = tokenize_by_letters(text)
    storage = LetterStorage()
    storage.update(tokenized_text)
    print('Count of letters: ', storage.get_letter_count())
    print('5 letters with the lowest ids', list(storage.storage.items())[:5])
    print('5 letters with the highest ids', list(storage.storage.items())[-5:])

    RESULT = storage.get_letter_count(), list(storage.storage.items())[:5], list(storage.storage.items())[-5:]
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT, 'Detection not working'


    RESULT = ''
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT, 'Detection not working'

