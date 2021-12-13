from main import LetterStorage,tokenize_by_letters


with open("reference_text.txt",'r', encoding='utf-8') as f:
    text = str(f)
    storage = LetterStorage()
    storage.update(tokenize_by_letters(text))
    print(storage.get_letter_count())
    index_dict = sorted(storage.storage.items(), key=lambda x: x[1])
    print(index_dict[0:5])
    print(index_dict[-1:-6:-1])


