import os
from lab_4.main import LetterStorage, tokenize_by_letters, encode_corpus,\
    LanguageProfile, NGramTextGenerator, \
    decode_sentence, translate_sentence_to_plain_text

PATH_TO_LAB_FOLDER = os.path.dirname(os.path.abspath(__file__))
PATH_TO_TEXT_FOLDER = os.path.join(PATH_TO_LAB_FOLDER)

if __name__ == '__main__':
    with open('reference_text.txt', 'r', encoding='utf-8') as text_to_read:
        reference_text = text_to_read.read()

# score 4
tokenized_text = tokenize_by_letters(reference_text)
storage = LetterStorage()
storage.update(tokenized_text)

letters = storage.get_letter_count()
letter_id = list(storage.storage.keys())

print('the number of letters is', letters)
print('5 letters with the highest id is', letter_id[-5:])
print('5 letters with the lowest id is', letter_id[:5])

# for score 6
profile = LanguageProfile(storage, 'en')
encoded_text = encode_corpus(storage, tokenized_text)
profile.create_from_tokens(encoded_text, (2,))
generator = NGramTextGenerator(profile)
generated_sent = generator.generate_sentence((1,), 5)
decoded_sent = decode_sentence(storage, generated_sent)
RESULT = translate_sentence_to_plain_text(decoded_sent)
print(RESULT)

# DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
assert RESULT, 'Detection not working'
