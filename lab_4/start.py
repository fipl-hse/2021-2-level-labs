from lab_4.main import tokenize_by_letters, LetterStorage

with open('reference_text.txt', 'r', encoding='utf-8') as fin:
    INPUT_TEXT = fin.read()


storage = LetterStorage()
TOKENIZED_TEXT = tokenize_by_letters(INPUT_TEXT)
storage.update(TOKENIZED_TEXT)

letters_count = storage.get_letter_count()
storage_keys_list = list(storage.storage.keys())


print("Letters  count: {letters_count}")
print("5 lowest letters id: {storage_keys_list[:5]}")
print("5 highest letters id: {storage_keys_list[-5:]}")
