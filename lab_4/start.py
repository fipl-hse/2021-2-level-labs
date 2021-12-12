from lab_4.main import LetterStorage, tokenize_by_letters

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

