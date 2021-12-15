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
                        LikelihoodBasedTextGenerator,
                        BackOffGenerator,
                        PublicLanguageProfile)

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


    def score_4():
        """
        score 4
        """
        amount = f"The number of letters: {storage.get_letter_count()}"
        low_ids = f"The letters with the lowest ids: {list(storage.storage)[1:6]}"
        high_ids = f"The letters with the highest ids: {list(storage.storage)[-5:]}"

        return amount, low_ids, high_ids

    def score_6():
        """
        score 6
        """
        language_profile = LanguageProfile(storage, "en")
        language_profile.create_from_tokens(encoded_text, (2,))

        text_generator = NGramTextGenerator(language_profile)

        sent_one = text_generator.generate_decoded_sentence((1,), 5)
        sent_two = text_generator.generate_decoded_sentence((1,), 6)
        sent_three = text_generator.generate_decoded_sentence((1,), 7)

        return sent_one, sent_two, sent_three

    def score_8():
        """
        score 8
        """
        language_profile = LanguageProfile(storage, "en")
        language_profile.create_from_tokens(encoded_text, (2,))

        text_generator = LikelihoodBasedTextGenerator(language_profile)

        sent_one = text_generator.generate_decoded_sentence((1,), 5)
        sent_two = text_generator.generate_decoded_sentence((1,), 6)
        sent_three = text_generator.generate_decoded_sentence((1,), 7)

        return sent_one, sent_two, sent_three

    def score_10():
        """
        score 10
        """
        language_profile = PublicLanguageProfile(storage, 'ne')
        language_profile.open(os.path.join(PATH_TO_LAB_FOLDER, 'ne'))
        text_generator = BackOffGenerator(language_profile)

        sent = text_generator.generate_decoded_sentence((1,), 5)

        return sent

    RESULT_4 = score_4()
    RESULT_6 = score_6()
    RESULT_8 = score_8()
    RESULT_10 = score_10()

