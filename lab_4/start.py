from lab_4.main import tokenize_by_letters, LetterStorage

with open('reference_text.txt', 'r', encoding='utf-8') as file_to_read:
    reference_text = file_to_read.read()
# score 4
preprocessed_text = tokenize_by_letters(reference_text)
storage = LetterStorage()
storage.update(preprocessed_text)

number_of_letters = storage.get_letter_count()

print('The number of letters is', number_of_letters)
print('Top 5 letters with the lowest id is', list(storage.storage.keys())[:5])
print('Top 5 letters with the highest id is', list(storage.storage.keys())[-5:])

# score 6
