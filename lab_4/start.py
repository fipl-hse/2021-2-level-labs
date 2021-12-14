"""
Language generation starter
"""

import os
from lab_4.main import tokenize_by_letters, LetterStorage, encode_corpus, \
    decode_sentence, translate_sentence_to_plain_text, \
    LanguageProfile, NGramTextGenerator, LikelihoodBasedTextGenerator

PATH_TO_LAB_FOLDER = os.path.dirname(os.path.abspath(__file__))


if __name__ == '__main__':

    # find the appropriate start.py task in your lab_4 description file
    # your code goes here

    def score_4():
        """
        Score 4
        """
        with open(os.path.join(PATH_TO_LAB_FOLDER, 'reference_text.txt'), 'r', encoding="utf-8") \
                as file:
            text = file.read()

        tokenization = tokenize_by_letters(text)
        storage = LetterStorage()
        storage.update(tokenization)

        #print("Number of letters: ", storage.get_letter_count())
        #print("Letters with the lowest identifier: ", list(storage.storage.items())[:5])
        #print("Letters with the highest identifier: ", list(storage.storage.items())[-5:])


    def score_6():
        """
        Score 6
        """
        with open(os.path.join(PATH_TO_LAB_FOLDER, 'reference_text.txt'), 'r', encoding="utf-8")\
                as file:
            text = file.read()
        tokenized = tokenize_by_letters(text)
        storage = LetterStorage()
        storage.update(tokenized)
        encoded = encode_corpus(storage, tokenized)
        profile = LanguageProfile(storage, 'en')
        profile.create_from_tokens(encoded, (2,))
        text_generator = NGramTextGenerator(profile)
        sentences = []
        for sentence_length in range(5, 10):
            sentences.append(text_generator.generate_decoded_sentence((1,), sentence_length))
        for sentence in sentences:
            print(sentence)


    def score_8():
        """
        Score 8
        """
        with open(os.path.join(PATH_TO_LAB_FOLDER, 'reference_text.txt'), 'r', encoding="utf-8") \
                as file:
            text = file.read()
        tokenization = tokenize_by_letters(text)
        storage = LetterStorage()
        storage.update(tokenization)
        encoded_corpus = encode_corpus(storage, tokenization)
        profile = LanguageProfile(storage, 'en')
        profile.create_from_tokens(encoded_corpus, (2,))
        text_generator = LikelihoodBasedTextGenerator(profile)
        sentences = []
        for length in range(5, 10):
            sentences.append(text_generator.generate_decoded_sentence((1,), length))
        return sentences

    #score_4()
    #score_6()
    RESULT = score_8()
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT, 'Detection not working'