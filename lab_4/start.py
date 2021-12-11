from lab_4.main import (tokenize_by_letters, LetterStorage)

with open('reference_text.txt', 'r', encoding='utf-8') as file_to_read:
    REFERENCE_TEXT = file_to_read.read()

tokenized = tokenize_by_letters(REFERENCE_TEXT)
storage = LetterStorage()
LetterStorage.update(storage, tokenized)

print('The number of letters in the storage:', storage.get_letter_count())
print('Top 5 letters with the lowest ids:', list(storage.storage.keys())[:5])
print('Top 5 letters with the highest ids:', list(storage.storage.keys())[-5:])



