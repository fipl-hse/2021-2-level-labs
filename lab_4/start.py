from lab_4.main import tokenize_by_letters, LetterStorage

with open('reference_text.txt', 'r', encoding='utf-8') as file_to_read:
    REFERENCE_TEXT = file_to_read.read()

TOKENIZED_TEXT = tokenize_by_letters(REFERENCE_TEXT)
storage = LetterStorage()
storage.update(TOKENIZED_TEXT)

# SCORE 4
print('the number of letters in the storage:', storage.get_letter_count())
print('top 5 with lowest id:', list(storage.storage.keys())[:5])
print('top 5 with highest id:', list(storage.storage.keys())[-5:])