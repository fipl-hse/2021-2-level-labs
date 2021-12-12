import main

with open('reference_text.txt', 'r', encoding='UTF-8') as read_text:
    CORPUS = read_text.read()

# for score 4

TOKENIZED_CORPUS = main.tokenize_by_letters(CORPUS)

ENG_STORAGE = main.LetterStorage()
ENG_STORAGE.update(TOKENIZED_CORPUS)

print('the number of letters is: ', ENG_STORAGE.get_letter_count())
print('first five letters are: ', list(ENG_STORAGE.storage)[:5])
print('last five letters are: ', list(ENG_STORAGE.storage)[-5:])
