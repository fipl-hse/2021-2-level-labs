import os
from lab_4.main import tokenize_by_letters, LetterStorage

"""
Mark 4
Токенизируйте текст, который хранится в файле reference_text.txt.
Заполните хранилище класса LetterStorage буквами.
Выведите количество букв в вашем хранилище.
Выведите 5 букв с наименьшим идентификатором,
а также 5 букв с наибольшим идентификатором.
"""

PATH_TO_LAB_FOLDER = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(PATH_TO_LAB_FOLDER, 'reference_text.txt'),
          'r', encoding='utf-8') as file_to_read:
    reference_text = file_to_read.read()

reference_text_tokens = tokenize_by_letters(reference_text)
storage = LetterStorage()
storage.update(reference_text_tokens)
letters_id = list(storage.storage.keys())

print("The № of letters:", storage.get_letter_count())
print("Top-5 of the lowest id numbers:", letters_id[:5])
print("Top-5 of the highest id numbers:", letters_id[-5:])


