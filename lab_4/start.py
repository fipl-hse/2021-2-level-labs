"""
Language generation starter
"""

import os
from main import tokenize_by_letters
from main import LetterStorage

PATH_TO_LAB_FOLDER = os.path.dirname(os.path.abspath(__file__))

if __name__ == '__main__':

    # find the appropriate start.py task in your lab_4 description file
    # your code goes here
    def process_text():
        # opened file
        with open(os.path.join(PATH_TO_LAB_FOLDER, 'reference_text.txt'), 'r', encoding='utf-8') as file_to_read:
            text = file_to_read.read()
        # tokenized text
        text = tokenize_by_letters(text)
        # created object
        storage = LetterStorage()
        # filled storage
        storage.update(text)
        print('\n**********STORAGE**********\n', storage.storage)
        # counted token
        token_len = storage.get_letter_count()
        print('\n***********COUNT***********\n', 'count function = ', token_len, '\ncount in dict = ',
              len(storage.storage))
        # print top-5 token with the smallest and the biggest id
        top_n = 5
        smallest_id_token_list = []
        biggest_id_token_list = []
        for letter, i in storage.storage.items():
            if i < top_n + 1:
                smallest_id_token_list.append(letter)
            elif token_len - i < 5:
                biggest_id_token_list.append(letter)
        print('\n***********TOP***********')
        print('top ', top_n, 'token list : ', smallest_id_token_list)
        print('last', top_n, 'token list : ', biggest_id_token_list)


    process_text()

    RESULT = '1'
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT, 'Detection not working'
