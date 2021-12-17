"""
Language generation starter
"""

import os
from lab_4.main import tokenize_by_letters, LetterStorage, \
     encode_corpus, LanguageProfile, decode_sentence, NGramTextGenerator,\
     LikelihoodBasedTextGenerator, translate_sentence_to_plain_text

PATH_TO_LAB_FOLDER = os.path.dirname(os.path.abspath(__file__))

if __name__ == '__main__':
    print("****************SCORE 4****************")
    with open(os.path.join(PATH_TO_LAB_FOLDER, 'reference_text.txt'), 'r', encoding="utf-8") \
            as file_to_read:
        reference_text = file_to_read.read()
    preprocessed_text = tokenize_by_letters(reference_text)
    storage = LetterStorage()
    storage.update(preprocessed_text)

    number_of_letters = storage.get_letter_count()

    print('The number of letters is', number_of_letters)
    print('Top 5 letters with the lowest id is', list(storage.storage.keys())[:5])
    print('Top 5 letters with the highest id is', list(storage.storage.keys())[-5:])

    print("****************SCORE 6****************")
    # with open(os.path.join(PATH_TO_LAB_FOLDER, 'reference_text.txt'), 'r', encoding="utf-8") \
    #         as file_to_read:
    #     reference_text = file_to_read.read()
    # preprocessed_text = tokenize_by_letters(reference_text)
    # storage = LetterStorage()
    # storage.update(preprocessed_text)
    encoded_text = encode_corpus(storage, preprocessed_text)
    language_profile = LanguageProfile(storage, 'en')
    language_profile.create_from_tokens(encoded_text, (2,))
    generator = NGramTextGenerator(language_profile)
    for length in range(5, 10):
        generated_text = generator.generate_sentence((1,), length)
        decoded_text = decode_sentence(storage, generated_text)
        plain_text = translate_sentence_to_plain_text(decoded_text)
        print(plain_text)

    print("****************SCORE 8****************")
    # with open(os.path.join(PATH_TO_LAB_FOLDER, 'reference_text.txt'), 'r', encoding="utf-8") \
    #         as file_to_read:
    #     reference_text = file_to_read.read()
    # storage = LetterStorage()
    # storage.update(tokenize_by_letters(reference_text))
    encoded_corpus = encode_corpus(storage, tokenize_by_letters(reference_text))
    language_profile = LanguageProfile(storage, 'en')
    language_profile.create_from_tokens(encoded_corpus, (2,))
    generated_text = LikelihoodBasedTextGenerator(language_profile)
    sentences = []
    for length in range(5, 10):
        sentences.append(generated_text.generate_decoded_sentence((1,), length))
    print(sentences)
    RESULT = sentences

    # find the appropriate start.py task in your lab_4 description file
    # your code goes here

    # RESULT = ''
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT, 'Detection not working'
