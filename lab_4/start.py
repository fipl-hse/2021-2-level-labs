
from lab_4.main import tokenize_by_letters, LetterStorage

with open('reference_text.txt', 'r', encoding='utf-8') as file_to_read:
    reference_text = file_to_read.read()

tokenized_text = tokenize_by_letters(reference_text)
storage = LetterStorage()
storage.update(tokenized_text)

num_of_letters = storage.get_letter_count()
lowest_id = list(storage.storage.keys())
highest_id = list(storage.storage.keys())

print('The number of letters is:', num_of_letters)
print('5 letters with the lowest id:', lowest_id[:5])
print('5 letters with the highest id:', highest_id[-5:])
