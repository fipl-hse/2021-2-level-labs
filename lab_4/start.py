"""
Language generation starter
"""

import os
from main import tokenize_by_letters, LetterStorage, encode_corpus, \
    LanguageProfile, NGramTextGenerator, decode_sentence, \
    translate_sentence_to_plain_text, LikelihoodBasedTextGenerator

PATH_TO_LAB_FOLDER = os.path.dirname(os.path.abspath(__file__))
PATH_TO_TEXT_FOLDER = os.path.join(PATH_TO_LAB_FOLDER)

if __name__ == '__main__':

    # find the appropriate start.py task in your lab_4 description file
    # your code goes here

    # 4
    with open(os.path.join(PATH_TO_TEXT_FOLDER, "reference_text.txt"), "r",
              encoding="utf-8") as file_to_read:
        text = file_to_read.read()
    text_tokens = tokenize_by_letters(text)
    text_storage = LetterStorage()
    text_storage.update(text_tokens)
    number_of_letters_text = text_storage.get_letter_count()
    the_least_id = list(text_storage.storage)[:5]
    the_most_id = list(text_storage.storage)[-5:]
    print(number_of_letters_text, "\n", the_least_id, "\n", the_most_id)
    # 6
    encoded_text = encode_corpus(text_storage, text_tokens)
    text_profile = LanguageProfile(text_storage, "en")
    text_profile.create_from_tokens(encoded_text, (2,))
    text_generator = NGramTextGenerator(text_profile)
    sentence = text_generator.generate_sentence((5,), 7)
    decoded_sentence = decode_sentence(text_storage, sentence)
    RESULT = translate_sentence_to_plain_text(decoded_sentence)
    print(RESULT)
    # 8
    new_text_generator = LikelihoodBasedTextGenerator(text_profile)
    RESULT = []
    for i in range(5, 10):
        RESULT.append(new_text_generator.generate_decoded_sentence((8,), i))
    print("".join(RESULT))
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT, 'Detection not working'
