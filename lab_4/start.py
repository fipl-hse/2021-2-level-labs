
from lab_4.main import tokenize_by_letters, LetterStorage, LanguageProfile, \
    NGramTextGenerator, decode_sentence, encode_corpus, \
    translate_sentence_to_plain_text

with open('reference_text.txt', 'r', encoding='utf-8') as file_to_read:
    REFERENCE_TEXT = file_to_read.read()

TOKENIZED_TEXT = tokenize_by_letters(REFERENCE_TEXT)
storage = LetterStorage()
storage.update(TOKENIZED_TEXT)

# SCORE 4
print('the number of letters in the storage:', storage.get_letter_count())
print('top 5 with lowest id:', list(storage.storage.keys())[:5])
print('top 5 with highest id:', list(storage.storage.keys())[-5:])

# SCORE 6
encoded = encode_corpus(storage, TOKENIZED_TEXT)
profile = LanguageProfile(storage, 'en')
profile.create_from_tokens(encoded, (2,))

text_generator = NGramTextGenerator(profile)
generated_sentence = text_generator.generate_sentence((1,), 7)
decoded = decode_sentence(storage, generated_sentence)

RESULT_6 = translate_sentence_to_plain_text(decoded)
print('generated sentence:', RESULT_6)

