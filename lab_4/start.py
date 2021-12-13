"""
Language generation starter
"""

import os
from lab_4.main import tokenize_by_letters, LetterStorage, LanguageProfile, \
    NGramTextGenerator, decode_sentence, encode_corpus, \
    translate_sentence_to_plain_text

PATH_TO_LAB_FOLDER = os.path.dirname(os.path.abspath(__file__))

if __name__ == '__main__':

    # find the appropriate start.py task in your lab_4 description file
    # your code goes here

    """
    Mark 4
    """

    PATH_TO_LAB_FOLDER = os.path.dirname(os.path.abspath(__file__))

    with open(os.path.join(PATH_TO_LAB_FOLDER, 'reference_text.txt'),
              'r', encoding='utf-8') as file_to_read:
        REFERENCE_TEXT = file_to_read.read()

    REFERENCE_TEXT_TOKENS = tokenize_by_letters(REFERENCE_TEXT)
    storage = LetterStorage()
    storage.update(REFERENCE_TEXT_TOKENS)
    letters_id = list(storage.storage.keys())

    print("The № of letters:", storage.get_letter_count())
    print("Top-5 of the lowest id numbers:", letters_id[:5])
    print("Top-5 of the highest id numbers:", letters_id[-5:])

    """
    Mark 6
    """
    encoded = encode_corpus(storage, REFERENCE_TEXT_TOKENS)
    profile = LanguageProfile(storage, 'en')
    profile.create_from_tokens(encoded, (2,))

    generator = NGramTextGenerator(profile)
    sentence = generator.generate_sentence((1,), 10)
    decoded = decode_sentence(storage, sentence)

    RESULT = translate_sentence_to_plain_text(decoded)
    print('Generated sentence:', RESULT)

    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT, 'Detection not working'




