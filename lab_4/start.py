"""
Language generation starter
"""

import os
from main import LetterStorage, tokenize_by_letters, NGramTextGenerator, encode_corpus
from language_profile import LanguageProfile


PATH_TO_LAB_FOLDER = os.path.dirname(os.path.abspath(__file__))

if __name__ == '__main__':

    # find the appropriate start.py task in your lab_4 description file
    # your code goes here
        #4
    with open("reference_text.txt", 'r', encoding='utf-8') as f:
        text = str(f)
        tokenized_text = tokenize_by_letters(text)
        storage = LetterStorage()
        storage.update(tokenized_text)

        print(f'number of letters: {storage.get_letter_count()}')

        index_dict = sorted(storage.storage.items(), key=lambda x: x[1])

        print(f'first 5: {index_dict[0:5]}')
        print(f'last 5: {index_dict[-1:-6:-1]}')

        #6
        storage_2 = LetterStorage()
        storage_2.update(tokenized_text)
        profile = LanguageProfile(storage_2, 'en')
        encoded_text_thing = encode_corpus(storage_2,tokenized_text)
        profile.create_from_tokens(encoded_text_thing, (2,))
        generator = NGramTextGenerator(profile)
        sentence_1 = generator.generate_decoded_sentence((1,), 6)
        sentence_2 = generator.generate_decoded_sentence((4,), 8)
        sentence_3 = generator.generate_decoded_sentence((2,), 5)

        print(sentence_1)
        print(sentence_2)
        print(sentence_3)

    RESULT = ''
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT, 'Detection not working'