"""
Language generation starter
"""

import os
from lab_4.main import tokenize_by_letters, LetterStorage, encode_corpus, LanguageProfile, NGramTextGenerator
PATH_TO_LAB_FOLDER = os.path.dirname(os.path.abspath(__file__))

if __name__ == '__main__':
    with open(os.path.join(PATH_TO_LAB_FOLDER, 'reference_text.txt'), 'r', encoding="utf-8") \
            as file:
        text = file.read()
    text = tokenize_by_letters(text)
    storage = LetterStorage()
    storage.update(text)
    encoded = encode_corpus(storage, text)
    profile = LanguageProfile(storage, 'english')
    profile.create_from_tokens(encoded, (2,))
    text_generator = NGramTextGenerator(profile)
    sentences = []
    for sentence_length in range(5, 10):
        sentences.append(text_generator.generate_decoded_sentence((1,), sentence_length))
    for sentence in sentences:
        print(sentence)

    RESULT = sentences
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT, 'Detection not working'

