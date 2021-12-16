"""
Language generation starter
"""

import os
from lab_4.main import tokenize_by_letters, LetterStorage, LanguageProfile, \
    NGramTextGenerator, decode_sentence, encode_corpus, \
    translate_sentence_to_plain_text, LikelihoodBasedTextGenerator

PATH_TO_LAB_FOLDER = os.path.dirname(os.path.abspath(__file__))

if __name__ == '__main__':
    with open(os.path.join(PATH_TO_LAB_FOLDER, 'reference_text.txt'), 'r', encoding="utf-8") \
            as file:
        text = file.read()
    tokenized_text = tokenize_by_letters(text)
    storage = LetterStorage()
    storage.update(tokenized_text)
    print('Score 4')
    print('Number of letters = {} '.format(storage.get_letter_count()))
    print('Letters with the lowest id: {}'.format(list(storage.storage.items())[:5]))
    print('Letters with the highest id: {}'.format(list(storage.storage.items())[-5:]))

    with open(os.path.join(PATH_TO_LAB_FOLDER, 'reference_text.txt'), 'r', encoding="utf-8") \
            as file:
        text = file.read()
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

    with open(os.path.join(PATH_TO_LAB_FOLDER, 'reference_text.txt'), 'r', encoding="utf-8") \
            as file:
        text = file.read()
    storage = LetterStorage()
    storage.update(tokenize_by_letters(text))
    encoded_text = encode_corpus(storage, tokenized_text)

    profile = LanguageProfile(storage, 'en')
    profile.create_from_tokens(encoded_text, (2,))

    generate_text = LikelihoodBasedTextGenerator(profile)
    sentences = generate_text.generate_sentence((1,), 7)
    decoded_sentences = decode_sentence(storage, sentences)

    decoded_corpus_8 = translate_sentence_to_plain_text(decoded_sentences)
    print('Score 8')
    print(decoded_corpus_8)
    RESULT = decoded_corpus_8

    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT, 'Detection not working'
