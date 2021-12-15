"""
Language generation starter
"""

import os

from lab_4.language_profile import LanguageProfile
from lab_4.main import tokenize_by_letters, LetterStorage, encode_corpus, NGramTextGenerator, decode_sentence, \
    translate_sentence_to_plain_text, LikelihoodBasedTextGenerator

PATH_TO_LAB_FOLDER = os.path.dirname(os.path.abspath(__file__))

if __name__ == '__main__':
    # find the appropriate start.py task in your lab_4 description file
    # your code goes here
    with open(os.path.join(PATH_TO_LAB_FOLDER, 'reference_text.txt'), 'r', encoding="utf-8") as file:
        text = file.read()
    tokenized = tokenize_by_letters(text)
    storage = LetterStorage()
    storage.update(tokenized)

    # score_4
    print(f"Number of letters: {storage.get_letter_count()}")
    print(f"Letters with the lowest id: {list(storage.storage.items())[:5]}")
    print(f"Letters with the highest id: {list(storage.storage.items())[-5:]}")

    encoded_corpus = encode_corpus(storage, tokenized)
    profile = LanguageProfile(storage, 'en')
    profile.create_from_tokens(encoded_corpus, (2,))

    # score_6
    text_generator = NGramTextGenerator(profile)
    generated_sent_1 = text_generator.generate_decoded_sentence((1,), 6)
    generated_sent_2 = text_generator.generate_decoded_sentence((1,), 7)
    generated_sent_3 = text_generator.generate_decoded_sentence((1,), 8)
    print(f"First generated sentence: {generated_sent_1}")
    print(f"Second generated sentence: {generated_sent_2}")
    print(f"Third generated sentence: {generated_sent_3}")

    # score_8
    text_generator = LikelihoodBasedTextGenerator(profile)
    generated_sent_1 = text_generator.generate_decoded_sentence((1,), 6)
    generated_sent_2 = text_generator.generate_decoded_sentence((1,), 7)
    generated_sent_3 = text_generator.generate_decoded_sentence((1,), 8)
    print(f"First generated sentence: {generated_sent_1}")
    print(f"Second generated sentence: {generated_sent_2}")
    print(f"Third generated sentence: {generated_sent_3}")

    RESULT = ''
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT, 'Detection not working'
