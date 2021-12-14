"""
Language generation starter
"""

import os
from lab_4.main import tokenize_by_letters, LetterStorage, \
    encode_corpus, decode_sentence, LanguageProfile, NGramTextGenerator,\
    LikelihoodBasedTextGenerator

PATH_TO_LAB_FOLDER = os.path.dirname(os.path.abspath(__file__))

if __name__ == '__main__':
    def score_4():
        """
        4
        """
        with open(os.path.join(PATH_TO_LAB_FOLDER, 'reference_text.txt'), 'r', encoding="utf-8")\
            as file:
            text = file.read()
        tokenized_text = tokenize_by_letters(text)
        storage = LetterStorage()
        storage.update(tokenized_text)
        print('Number of letters = {} '.format(storage.get_letter_count()))
        print('Letters with the lowest id: {}'.format(list(storage.storage.items())[:5]))
        print('Letters with the highest id: {}'.format(list(storage.storage.items())[-5:]))

    def score_6():
        """
        6
        """
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
        for length in range(5, 10):
            sentences.append(generate_text.generate_decoded_sentence((1,), length))
        #PRINT
        for sentence in sentences:
            print(sentence)

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
        for sentence in sentences:
            print(sentence)

    score_4()
    score_6()
    RESULT = score_6()
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT, 'Detection not working'
