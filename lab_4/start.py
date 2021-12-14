"""
Language generation starter
"""

import os
from lab_4.main import (tokenize_by_letters, LetterStorage,
                        LanguageProfile, NGramTextGenerator,
                        decode_sentence, encode_corpus,
                        translate_sentence_to_plain_text)

PATH_TO_LAB_FOLDER = os.path.dirname(os.path.abspath(__file__))

if __name__ == '__main__':
    with open('reference_text.txt', 'r', encoding='utf-8') as file_to_read:
        text = file_to_read.read()

    tokenized_text = tokenize_by_letters(text)

    storage = LetterStorage()
    storage.update(tokenized_text)

    # score 4
    print('The number of letters in storage:', storage.get_letter_count())
    print('Top 5 letters with the lowest id:', list(storage.storage.keys())[:5])
    print('Top 5 letters with the highest id:', list(storage.storage.keys())[-5:])

    # SCORE 6
    encoded = encode_corpus(storage, tokenized_text)
    profile = LanguageProfile(storage, 'en')
    profile.create_from_tokens(encoded, (2,))

    text_generator = NGramTextGenerator(profile)
    generated_sentence = text_generator.generate_sentence((3,), 5)
    decoded_sentence = decode_sentence(storage, generated_sentence)
    plain_text = translate_sentence_to_plain_text(decoded_sentence)
    print('generated sentence:', plain_text)

    RESULT = ''
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT, 'Detection not working'
