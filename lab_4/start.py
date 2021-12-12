from lab_4.main import (tokenize_by_letters,
                        LetterStorage,
                        encode_corpus,
                        decode_sentence,
                        LanguageProfile,
                        NGramTextGenerator,
                        translate_sentence_to_plain_text)

with open('reference_text.txt', 'r', encoding='utf-8') as file_to_read:
    reference_text = file_to_read.read()

tokenized = tokenize_by_letters(reference_text)
storage = LetterStorage()
storage.update(tokenized)

# score 4
print('The number of letters in the storage:', storage.get_letter_count())
print('Top 5 letters with the lowest ids:', list(storage.storage.keys())[:5])
print('Top 5 letters with the highest ids:', list(storage.storage.keys())[-5:])

encoded = encode_corpus(storage, tokenized)
en_profile = LanguageProfile(storage, 'en')
en_profile.create_from_tokens(encoded, (2,))

text_generator = NGramTextGenerator(en_profile)
generated = text_generator.generate_sentence((4,), 8)

decoded = decode_sentence(storage, generated)
final_sentence = translate_sentence_to_plain_text(decoded)

# score 6
print('Generated sentence:', final_sentence)




