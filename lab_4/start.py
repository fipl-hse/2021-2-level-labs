"""
Language generation starter
"""

import os
from main import tokenize_by_letters, \
    LetterStorage, \
    encode_corpus, \
    decode_sentence, \
    LanguageProfile, \
    NGramTextGenerator, \
    translate_sentence_to_plain_text

PATH_TO_LAB_FOLDER = os.path.dirname(os.path.abspath(__file__))

if __name__ == '__main__':

    def score_6():
        """
        6 realisation
        """
        with open(os.path.join(PATH_TO_LAB_FOLDER, 'reference_text.txt'),
                'r', encoding="utf-8") as file:
            text = file.read()

        tokens = tokenize_by_letters(text)
        storage = LetterStorage()
        storage.update(tokens)

        encoded_text = encode_corpus(storage, tokens)

        profile = LanguageProfile(storage, 'en')
        profile.create_from_tokens(encoded_text, (2,))

        generate_text = NGramTextGenerator(profile)
        decoded_sentences = []
        for lenth in range(5, 10):
            sentence = generate_text.generate_sentence((1,), lenth)
            decode_sentence(storage, sentence)
            decoded_sentences.append(translate_sentence_to_plain_text(tuple(decoded_sentences)))
        return decoded_sentences

    RESULT = score_6()
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT, 'Detection not working'
