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
        reference_text = file.read()
    tokenized_text = tokenize_by_letters(reference_text)
    storage = LetterStorage()
    storage.update(tokenized_text)

    print(f"Количество букв в хранилище: {storage.get_letter_count()}")
    print(f"5 букв с наименьшим идентификатором: {list(storage.storage.keys())[:5]}")
    print(f"5 букв с наибольшим идентификатором: {list(storage.storage.keys())[-5:]}")
    RESULT = storage.get_letter_count(), list(storage.storage.keys())[:5], list(storage.storage.keys())[-5:]
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT, 'Detection not working'
