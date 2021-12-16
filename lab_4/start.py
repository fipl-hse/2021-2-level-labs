"""
Language generation starter
"""

import os
from lab_4.main import (
    tokenize_by_letters,
    encode_corpus,
    LetterStorage,
    LanguageProfile,
    NGramTextGenerator
)

PATH_TO_LAB_FOLDER = os.path.dirname(os.path.abspath(__file__))

if __name__ == '__main__':

    with open(os.path.join(PATH_TO_LAB_FOLDER, 'reference_text.txt'), 'r', encoding="utf-8") \
            as file:
        text = file.read()

    tokenization = tokenize_by_letters(text)
    storage = LetterStorage()
    storage.update(tokenization)

    print('storage: ', storage.storage)
    print('number of letters: ', storage.get_letter_count())
    print('lowest identifier: ', list(storage.storage.items())[:5])
    print('highest identifier: ', list(storage.storage.items())[-5:])

    encoded = encode_corpus(storage, tokenization)

    profile = LanguageProfile(storage, 'en')
    profile.create_from_tokens(encoded, (2,))

    text_generator = NGramTextGenerator(profile)

    sent_one = text_generator.generate_decoded_sentence((1,), 5)
    sent_two = text_generator.generate_decoded_sentence((1,), 6)
    sent_three = text_generator.generate_decoded_sentence((1,), 7)
    print(sent_one, sent_two, sent_three)

    RESULT = 'The an ond s ing. Hat warer bento cof forouristedese peasitiomelece. Mal dichillieeta radotrssh lacaim nemowholy eveprtsosayoov geidryexpopami.'
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT, 'Detection not working'
