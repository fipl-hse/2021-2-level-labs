"""
Language generation starter
"""

import os
from lab_4.main import tokenize_by_letters, LetterStorage

PATH_TO_LAB_FOLDER = os.path.dirname(os.path.abspath(__file__))
PATH_TO_TEXT_FOLDER = os.path.join(PATH_TO_LAB_FOLDER)

if __name__ == '__main__':

    # find the appropriate start.py task in your lab_4 description file
    # your code goes here

    with open(os.path.join(PATH_TO_TEXT_FOLDER, 'reference_text.txt'), 'r', encoding='utf-8') as file_to_read:
        whole_text = file_to_read.read()

    token_text = tokenize_by_letters(whole_text)
    storage = LetterStorage()
    storage.update(token_text)

    print(storage.get_letter_count())
    print(list(storage.storage.keys())[1:6])
    print(list(storage.storage.keys())[-5:])

    RESULT = ''
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    # assert RESULT, 'Detection not working'
