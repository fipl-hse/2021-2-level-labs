"""
Language generation starter
"""

import os
from lab_4.main import tokenize_by_letters, LetterStorage, LanguageProfile, \
    NGramTextGenerator, decode_sentence, encode_corpus, \
    translate_sentence_to_plain_text, LikelihoodBasedTextGenerator

PATH_TO_LAB_FOLDER = os.path.dirname(os.path.abspath(__file__))

if __name__ == '__main__':
    def score_4():
        with open(os.path.join(PATH_TO_LAB_FOLDER, 'reference_text.txt'), 'r', encoding='utf-8') \
                as file_to_read:
            text = file_to_read.read()

        tokenized_text = tokenize_by_letters(text)
        storage = LetterStorage()
        storage.update(tokenized_text)

        number_of_letters = storage.get_letter_count()
        the_lowest_id = list(storage.storage.items())[:5]
        the_highest_id = list(storage.storage.items())[-5:]

        print('Score 4')
        print('The number of letters in storage: {} '.format(number_of_letters))
        print('Top 5 letters with the lowest ids: {} '.format(the_lowest_id))
        print('Top 5 letters with the highest ids: {} '.format(the_highest_id))
        return number_of_letters, the_lowest_id, the_highest_id

    def score_6():
        with open(os.path.join(PATH_TO_LAB_FOLDER, 'reference_text.txt'), 'r', encoding='utf-8') \
                as file_to_read:
            text = file_to_read.read()

        tokenized_text = tokenize_by_letters(text)
        storage = LetterStorage()
        storage.update(tokenized_text)

        encoded_text = encode_corpus(storage, tokenized_text)

        profile = LanguageProfile(storage, 'en')
        profile.create_from_tokens(encoded_text, (2,))

        generate_text = NGramTextGenerator(profile)
        sentences = generate_text.generate_sentence((1,), 7)
        decoded_sentences = decode_sentence(storage, sentences)

        decoded_corpus = translate_sentence_to_plain_text(decoded_sentences)
        print('Score 6')
        print(decoded_corpus)
        return decoded_corpus

    def score_8():
        with open(os.path.join(PATH_TO_LAB_FOLDER, 'reference_text.txt'), 'r', encoding='utf-8') \
                as file_to_read:
            text = file_to_read.read()

        tokenized_text = tokenize_by_letters(text)
        storage = LetterStorage()
        storage.update(tokenized_text)

        encoded_text = encode_corpus(storage, tokenized_text)

        profile = LanguageProfile(storage, 'en')
        profile.create_from_tokens(encoded_text, (2,))

        generate_text = LikelihoodBasedTextGenerator(profile)
        sentences = generate_text.generate_sentence((1,), 7)
        decoded_sentences = decode_sentence(storage, sentences)

        decoded_corpus = translate_sentence_to_plain_text(decoded_sentences)
        print('Score 8')
        print(decoded_corpus)
        return decoded_corpus

    score_4()
    score_6()
    score_8()

    RESULT = score_8()

    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT, 'Detection not working'
