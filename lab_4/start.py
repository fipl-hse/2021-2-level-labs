"""
Language generation starter
"""

import os
from lab_4.main import tokenize_by_letters, LetterStorage, \
    encode_corpus, decode_sentence, LanguageProfile, NGramTextGenerator,\
    LikelihoodBasedTextGenerator, translate_sentence_to_plain_text

PATH_TO_LAB_FOLDER = os.path.dirname(os.path.abspath(__file__))

if __name__ == '__main__':

    # find the appropriate start.py task in your lab_4 description file
    # your code goes here

    def score_4():
        with open(os.path.join(PATH_TO_LAB_FOLDER, 'reference_text.txt'), 'r', encoding="utf-8")\
            as file:
            text = file.read()
        tokenized_text = tokenize_by_letters(text)
        storage = LetterStorage()
        storage.update(tokenized_text)
        #RETURN
        number_of_letters = storage.get_letter_count()
        the_lowest_id = list(storage.storage.items())[:5]
        the_highest_id = list(storage.storage.items())[-5:]
        print('Number of letters = {} '.format(number_of_letters))
        print('Letters with the lowest id: {}'.format(the_lowest_id))
        print('Letters with the highest id: {}'.format(the_highest_id))
        return number_of_letters, the_lowest_id, the_highest_id

    def score_6():
        with open(os.path.join(PATH_TO_LAB_FOLDER, 'reference_text.txt'), 'r', encoding="utf-8")\
            as file:
            text = file.read()
        tokenized_text = tokenize_by_letters(text)
        storage = LetterStorage()
        storage.update(tokenized_text)
        #ENCODE
        encoded_text = encode_corpus(storage, tokenized_text)
        #LANGUAGE PROFILE
        profile = LanguageProfile(storage, 'en')
        profile.create_from_tokens(encoded_text, (2,))
        #GENERATION
        generate_text = NGramTextGenerator(profile)
        sentences = []
        decoded_sentences = []
        for length in range(5, 10):
            sentences.append(generate_text.generate_decoded_sentence((1,), length))
            decoded_corpus = decode_sentence(storage, sentences)
            decoded_sentences.append(translate_sentence_to_plain_text(decoded_corpus))
        #PRINT
        return decoded_sentences

    def score_8():
        with open(os.path.join(PATH_TO_LAB_FOLDER, 'reference_text.txt'), 'r', encoding="utf-8")\
            as file:
            text = file.read()
        tokenized_text = tokenize_by_letters(text)
        storage = LetterStorage()
        storage.update(tokenized_text)
        # ENCODE
        encoded_text = encode_corpus(storage, tokenized_text)
        # LANGUAGE PROFILE
        profile = LanguageProfile(storage, 'en')
        profile.create_from_tokens(encoded_text, (2,))
        # GENERATION
        generate_text = LikelihoodBasedTextGenerator(profile)
        sentences = []
        for length in range(5, 10):
            sentences.append(generate_text.generate_decoded_sentence((1,), length))
        # PRINT
        return sentences


    RESULT = ''
    score_4()
    score_6()
    RESULT = score_8()

    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT, 'Detection not working'
