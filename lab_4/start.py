"""
Language generation starter
"""

import os
from lab_4.main import (
    tokenize_by_letters,
    encode_corpus,
    LetterStorage,
    LanguageProfile,
    NGramTextGenerator,
    decode_sentence,
    translate_sentence_to_plain_text
)

PATH_TO_LAB_FOLDER = os.path.dirname(os.path.abspath(__file__))

if __name__ == '__main__':

    with open(os.path.join(PATH_TO_LAB_FOLDER, 'reference_text.txt'), 'r', encoding="utf-8") \
            as file:
        text = file.read()

    tokenization = tokenize_by_letters(text)
    storage = LetterStorage()
    storage.update(tokenization)

    print("number of letters: ", storage.get_letter_count())
    print("lowest identifier: ", list(storage.storage.items())[:5])
    print("highest identifier: ", list(storage.storage.items())[-5:])

    encoded_corpus = encode_corpus(storage, tokenization)

    profile = LanguageProfile(storage, 'en')
    profile.create_from_tokens(encoded_corpus, (2,))

    text_generator = NGramTextGenerator(profile)
    sentences = []

    result = []

    for length in range(5, 10):
        sentences.append(text_generator.generate_sentence((1,), length))
        decoded_corpus = decode_sentence(storage, sentences)
        result.append(translate_sentence_to_plain_text(decoded_corpus))
    print(result)

    RESULT = ''
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT, 'Detection not working'
