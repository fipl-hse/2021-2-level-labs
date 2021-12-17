"""
Language generation starter
"""

import os

from lab_4.language_profile import LanguageProfile
from lab_4.main import tokenize_by_letters, LetterStorage, \
    encode_corpus, NGramTextGenerator, LikelihoodBasedTextGenerator, \
    decode_sentence, translate_sentence_to_plain_text

PATH_TO_LAB_FOLDER = os.path.dirname(os.path.abspath(__file__))

if __name__ == '__main__':
    # find the appropriate start.py task in your lab_4 description file
    # your code goes here
    with open(os.path.join(PATH_TO_LAB_FOLDER, 'reference_text.txt'),
              'r', encoding="utf-8") as file:
        text = file.read()
    tokenized = tokenize_by_letters(text)
    storage = LetterStorage()
    storage.update(tokenized)

    # score_4
    print(f"Number of letters: {storage.get_letter_count()}")
    print(f"Letters with the lowest id: {list(storage.storage.items())[:5]}")
    print(f"Letters with the highest id: {list(storage.storage.items())[-5:]}")

    print("------------------------------------------------------")

    encoded_corpus = encode_corpus(storage, tokenized)
    profile = LanguageProfile(storage, 'en')
    profile.create_from_tokens(encoded_corpus, (2,))

    # score_6
    text_generator = NGramTextGenerator(profile)
    for length in range(5, 10):
        generated_text = text_generator.generate_sentence((1,), length)
        decoded_text = decode_sentence(storage, generated_text)
        plain_text = translate_sentence_to_plain_text(decoded_text)
        print(plain_text)

    print("------------------------------------------------------")

    # score_8
    text_generator = LikelihoodBasedTextGenerator(profile)
    sentences = []
    for length in range(5, 10):
        sentences.append(text_generator.generate_decoded_sentence((1,), length))
    print(sentences)
    RESULT = sentences

    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT, 'Detection not working'
