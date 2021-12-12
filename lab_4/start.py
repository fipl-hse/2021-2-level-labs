from lab_4.main import tokenize_by_letters, LetterStorage

with open('reference_text.txt', 'r', encoding='utf-8') as file_to_read:
    text = file_to_read.read()

tokenized_text = tokenize_by_letters(text)

storage = LetterStorage()
storage.update(tokenized_text)

# score 4
print('The number of letters in storage:', storage.get_letter_count())
print('Top 5 letters with the lowest id:', list(storage.storage.keys())[:5])
print('Top 5 letters with the highest id:', list(storage.storage.keys())[-5:])
