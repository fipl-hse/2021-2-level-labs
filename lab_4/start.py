"""
Language generation starter
"""

import os
from main import tokenize_by_letters, LetterStorage, encode_corpus, LanguageProfile, NGramTextGenerator
PATH_TO_LAB_FOLDER = os.path.dirname(os.path.abspath(__file__))

if __name__ == '__main__':

    # find the appropriate start.py task in your lab_4 description file
    # your code goes here

    # for 4 score
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

    # for 6 score
    encoded_corpus = encode_corpus(text_storage, tokenization_txt)
    en_profile = LanguageProfile(text_storage, 'en')
    en_profile.create_from_tokens(encoded_corpus, (2,))

    txt_generator = NGramTextGenerator(en_profile)

    get_sentence_1 = txt_generator.generate_decoded_sentence((3,), 5)
    get_sentence_2 = txt_generator.generate_decoded_sentence((3,), 6)
    get_sentence_3 = txt_generator.generate_decoded_sentence((3,), 7)

    print('Generated sentence are: {}; {}; {}'.format(get_sentence_1, get_sentence_2, get_sentence_3))

    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT, 'Detection not working'
