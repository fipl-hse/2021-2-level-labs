"""
Language generation starter
"""

import os
from lab_4.main import (tokenize_by_letters,
                        LetterStorage,
                        encode_corpus,
                        decode_sentence,
                        LanguageProfile,
                        NGramTextGenerator,
                        LikelihoodBasedTextGenerator)

PATH_TO_LAB_FOLDER = os.path.dirname(os.path.abspath(__file__))

if __name__ == '__main__':

    with open(os.path.join(PATH_TO_LAB_FOLDER, 'reference_text.txt'), 'r', encoding="utf-8") \
            as file:
        reference_text = file.read()

    # score 4-8
    tokenized_text = tokenize_by_letters(reference_text)
    storage = LetterStorage()
    storage.update(tokenized_text)

    # score 6-8
    encoded_text = encode_corpus(storage, tokenized_text)
    language_profile = LanguageProfile(storage, "en")
    language_profile.create_from_tokens(encoded_text, (2,))


    def score_4():
        print(f"The number of letters: {storage.get_letter_count()}")
        print(f"The letters with the lowest ids: {list(storage.storage)[1:6]}")
        print(f"The letters with the highest ids: {list(storage.storage)[-5:]}")

    def score_6():
        text_generator = NGramTextGenerator(language_profile)
        print(text_generator.generate_decoded_sentence((1,), 5))
        print(text_generator.generate_decoded_sentence((1,), 6))
        print(text_generator.generate_decoded_sentence((1,), 7))

    def score_8():
        text_generator = LikelihoodBasedTextGenerator(language_profile)
        print(text_generator.generate_decoded_sentence((1,), 5))
        print(text_generator.generate_decoded_sentence((1,), 6))
        print(text_generator.generate_decoded_sentence((1,), 7))

    score_4()

    score_6()

    score_8()

    RESULT = ''
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT, 'Detection not working'
