"""
Language generation starter
"""

import os
from lab_4.main import (tokenize_by_letters,
                        encode_corpus,
                        decode_sentence,
                        LetterStorage,
                        LanguageProfile,
                        NGramTextGenerator)

PATH_TO_LAB_FOLDER = os.path.dirname(os.path.abspath(__file__))

if __name__ == '__main__':
    with open(os.path.join(PATH_TO_LAB_FOLDER, 'reference_text.txt'), 'r', encoding="utf-8") \
            as text:
        text = text.read()
    tokenised_text = tokenize_by_letters(text)
    letter_storage = LetterStorage()
    letter_storage.update(tokenised_text)
    encoded = encode_corpus(letter_storage, tokenised_text)
    profile = LanguageProfile(letter_storage, 'en')
    profile.create_from_tokens(encoded, (2,))
    def function_for_grade4():
        '''Токенизируйте текст, который хранится в файле reference_text.txt.
        Заполните хранилище класса LetterStorage буквами.
        Выведите количество букв в вашем хранилище.
        Выведите 5 букв с наименьшим идентификатором,
        а также 5 букв с наибольшим идентификатором.'''
        sorted_letter_storage = sorted(letter_storage.storage, key=letter_storage.storage.get, reverse=True)
        print(letter_storage.get_letter_count())
        print('Top 5 min ids:', sorted_letter_storage[-5:])
        print('Top 5 max ids:', sorted_letter_storage[:5])
        
    def function_for_grade6():
        '''Создайте экземпляр класса LanguageProfile, основанный на обработанном тексте.
        Сгенерируйте несколько предложений длиной по 5-10 слов.
        Декодируйте предложения и сконвертируйте их в строковый формат.'''
        text_generator = NGramTextGenerator(profile)
        for i in range(5, 10):
            generated_sentence = text_generator.generate_sentence((1,), i)
            decoded = decode_sentence(letter_storage, generated_sentence)
            print(translate_sentence_to_plain_text(decoded))

    # find the appropriate start.py task in your lab_4 description file
    # your code goes here

    RESULT = ''
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT, 'Detection not working'
