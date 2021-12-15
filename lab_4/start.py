"""
Language generation starter
"""

import os
from lab_4.main import (tokenize_by_letters, LetterStorage,
                        LanguageProfile, encode_corpus, NGramTextGenerator,
                        LikelihoodBasedTextGenerator)

PATH_TO_LAB_FOLDER = os.path.dirname(os.path.abspath(__file__))

if __name__ == '__main__':

    # find the appropriate start.py task in your lab_4 description file
    # your code goes here

    with open(os.path.join(PATH_TO_LAB_FOLDER, 'reference_text.txt'), 'r', encoding='utf-8') as file_to_read:
        whole_text = file_to_read.read()

    token_text = tokenize_by_letters(whole_text)
    storage = LetterStorage()
    storage.update(token_text)

    prof = LanguageProfile(storage, 'en')
    enc_text = encode_corpus(storage, token_text)
    prof.create_from_tokens(enc_text, (2,))

    # 6
    # generator = NGramTextGenerator(prof)
    # gen_sentence = generator.generate_decoded_sentence((3,), 6)
    # print(gen_sentence)

    # 4
    # print(storage.get_letter_count())
    # print(list(storage.storage.keys())[1:6])
    # print(list(storage.storage.keys())[-5:])

    # 8
    gen_8 = LikelihoodBasedTextGenerator(prof)
    gen_sen_8 = gen_8.generate_decoded_sentence((1,), 8)
    print(gen_sen_8)

    RESULT = ''
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    # assert RESULT, 'Detection not working'
