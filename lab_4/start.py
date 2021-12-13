"""
Language generation starter
"""

import os
from lab_4.main import tokenize_by_letters, \
    LetterStorage, \
    encode_corpus, \
    decode_sentence, \
    LanguageProfile, \
    NGramTextGenerator, \
    LikelihoodBasedTextGenerator, \
    BackOffGenerator, \
    PublicLanguageProfile

PATH_TO_LAB_FOLDER = os.path.dirname(os.path.abspath(__file__))

if __name__ == '__main__':

    def score_4():
        with open(os.path.join(PATH_TO_LAB_FOLDER, 'reference_text.txt'), 'r', encoding="utf-8") as file:
            text = file.read()

        tokenized = tokenize_by_letters(text)
        storage = LetterStorage()
        storage.update(tokenized)

        print("Score 4!")
        print("Number of letters: ", storage.get_letter_count())
        print("Letters with the lowest ids: ", list(storage.storage.items())[:5])
        print("Letters with the highest ids: ", list(storage.storage.items())[-5:])
        print("")

    def score_6():
        with open(os.path.join(PATH_TO_LAB_FOLDER, 'reference_text.txt'), 'r', encoding="utf-8") as file:
            text = file.read()

        tokenized = tokenize_by_letters(text)
        storage = LetterStorage()
        storage.update(tokenized)

        encoded = encode_corpus(storage, tokenized)

        profile = LanguageProfile(storage, 'en')
        profile.create_from_tokens(encoded, (2,))

        text_generator = NGramTextGenerator(profile)
        sentences = []

        for sentence_length in range(5, 10):
            sentences.append(text_generator.generate_decoded_sentence((1,), sentence_length))

        print("Score 6!")
        for sentence in sentences:
            print(sentence)
        print("")

    def score_8():
        with open(os.path.join(PATH_TO_LAB_FOLDER, 'reference_text.txt'), 'r', encoding="utf-8") as file:
            text = file.read()

        tokenized = tokenize_by_letters(text)
        storage = LetterStorage()
        storage.update(tokenized)

        encoded = encode_corpus(storage, tokenized)

        profile = LanguageProfile(storage, 'en')
        profile.create_from_tokens(encoded, (2,))

        text_generator = LikelihoodBasedTextGenerator(profile)
        sentences = []

        for sentence_length in range(5, 10):
            sentences.append(text_generator.generate_decoded_sentence((1,), sentence_length))

        print("Score 8!")
        for sentence in sentences:
            print(sentence)
        print("")

    def score_10():
        storage = LetterStorage()

        profile = PublicLanguageProfile(storage, 'ne')
        profile.open(os.path.join(PATH_TO_LAB_FOLDER, 'ne'))

        text_generator = NGramTextGenerator(profile)
        likelihood_text_generator = LikelihoodBasedTextGenerator(profile)
        backoff_text_generator = BackOffGenerator(profile)
        print("Score 10!")
        print(text_generator.generate_decoded_sentence((storage.get_special_token_id(),), 5))
        print(likelihood_text_generator.generate_decoded_sentence((storage.get_special_token_id(),), 5))
        print(backoff_text_generator.generate_decoded_sentence((storage.get_special_token_id(),), 5))


    #score_4()
    #score_6()
    #score_8()
    score_10()

    RESULT = ''
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT, 'Detection not working'
