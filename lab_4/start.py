"""
Language generation starter
"""

import os

from lab_4.language_profile import LanguageProfile
from lab_4.main import tokenize_by_letters, LetterStorage, encode_corpus, NGramTextGenerator

PATH_TO_LAB_FOLDER = os.path.dirname(os.path.abspath(__file__))

if __name__ == '__main__':
    with open(os.path.join(PATH_TO_LAB_FOLDER, 'reference_text.txt'), 'r', encoding="utf-8") \
            as file:
        text = file.read()

    tokenized = tokenize_by_letters(text)
    storage = LetterStorage()
    storage.update(tokenized)

    encoded = encode_corpus(storage, tokenized)

    profile = LanguageProfile(storage, 'en')
    profile.create_from_tokens(encoded, (2,))

    text_generator = NGramTextgenerator(profile)
    sentences = []

    for sentence_length in range(5,10):
        sentences.append(text_generator.generate_decoded_sentence((1,), sentence_length))

    for sentence in sentences:
        print(sentence)
    # find the appropriate start.py task in your lab_4 description file
    # your code goes here

    RESULT = ''
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT, 'Detection not working'
