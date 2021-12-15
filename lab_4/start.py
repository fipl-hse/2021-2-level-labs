"""
Language generation starter
"""

import os
from lab_4.main import (tokenize_by_letters,
                        encode_corpus,
                        decode_sentence,
                        LetterStorage,
                        LanguageProfile,
                        NGramTextGenerator)

PATH_TO_LAB_FOLDER = os.path.dirname(os.path.abspath(__file__))

if __name__ == '__main__':
    with open(os.path.join(PATH_TO_LAB_FOLDER, 'reference_text.txt'), 'r', encoding="utf-8") \
            as text:
        text = text.read()
    tokenised_text = tokenize_by_letters(text)
    letter_storage = LetterStorage()
    letter_storage.update(tokenised_text)
    encoded = encode_corpus(letter_storage, tokenised_text)
    profile = LanguageProfile(letter_storage, 'en')
    profile.create_from_tokens(encoded, (2,))
    
    def function_for_grade4():
        '''
        '''
        sorted_letter_storage = sorted(letter_storage.storage, key=letter_storage.storage.get, reverse=True)
        amount = f'Number of letters: {letter_storage.get_letter_count()}'
        min_ids = f'Top 5 min ids: {sorted_letter_storage[-5:]}'
        max_ids = f'Top 5 max ids: {sorted_letter_storage[:5]}'
        return amount, min_ids, max_ids
        
    def function_for_grade6():
        '''
        '''
        text_generator = NGramTextGenerator(profile)
        one = text_generator.generate_decoded_sentence((1,), 5)
        two = text_generator.generate_decoded_sentence((1,), 6)
        three = text_generator.generate_decoded_sentence((1,), 7)
        return one, two, three
    
    def function_for_grade8():
        '''
        '''
        likelihood_text_generator = LikelihoodBasedTextGenerator(profile)
        one = likelihood_text_generator.generate_decoded_sentence((1,), 5)
        two = likelihood_text_generator.generate_decoded_sentence((1,), 6)
        three = likelihood_text_generator.generate_decoded_sentence((1,), 7)
        return one, two, three

    # find the appropriate start.py task in your lab_4 description file
    # your code goes here

    RESULT_4 = function_for_grade4()
    RESULT_6 = function_for_grade6()
    RESULT_8 = function_for_grade8()
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT_8, 'Detection not working'
