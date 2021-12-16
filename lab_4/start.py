"""
Language generation starter
"""

import os
from main import tokenize_by_letters, LetterStorage
PATH_TO_LAB_FOLDER = os.path.dirname(os.path.abspath(__file__))

if __name__ == '__main__':

    # find the appropriate start.py task in your lab_4 description file
    # your code goes here
    with open(os.path.join(PATH_TO_LAB_FOLDER, 'reference_text.txt'), 'r', encoding='utf-8') as file:
        text = file.read()
    tokenization_txt = tokenize_by_letters(text)
    text_storage = LetterStorage()
    text_storage.update(tokenization_txt)

    number_of_letters = text_storage.get_letter_count()
    id_least = list(text_storage.storage)[:5]
    id_most = list(text_storage.storage)[-5:]

    RESULT = 'Total letters in the text: {}'.format(number_of_letters), \
             'Five letters with the least id: {}'.format(id_least), \
             'Five letters with the most id: {}'.format(id_most)
    print(RESULT)
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT, 'Detection not working'
