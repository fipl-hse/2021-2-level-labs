"""
Lab 1
Language detection
"""


def tokenize(text: str) -> list or None:
    """
    Splits a text into tokens, converts the tokens into lowercase,
    removes punctuation and other symbols from words
    :param text: a text
    :return: a list of lower-cased tokens without punctuation
    """

    if isinstance(text, str):  # text является экземпляром классом str
        text = text.lower()  # перевод строки в нижний регистр
        for char in text:
            if char != ' ' and not (char.isalpha()):  # проверка то,что символ не пробел и не является буквой
                text = text.replace(char, "")  # удаление этого символа

        tokens = text.split()
        if tokens:  # если массив не пустой
            return tokens
        else:
            return None


def remove_stop_words(tokens: list, stop_words: list):
    """
    Removes stop words
    :param tokens: a list of tokens
    :param stop_words: a list of stop words
    :param stop_words.words(language): a list of stop words
    :return: a list of tokens without stop words
    """
    if isinstance(tokens, list) and isinstance(stop_words, list):
        if tokens:  # проверка на то что список tokens не пустой
            for j in range(len(tokens)):  # иттерация по индексам элементов списка tokens
                if tokens[j] in stop_words:  # проверка является ли элемент стоп словом
                    tokens[j] = ''  # замена этого элемента на пустую строку

            while '' in tokens:  # удаление пустых строк из списка
                tokens.remove('')
            return tokens
        else:
            return None
    else:
        return None


def calculate_frequencies(tokens: list) -> dict or None:
    """
      Calculates frequencies of given tokens
      :param tokens: a list of tokens
      :return: a dictionary with frequencies
      """
    if isinstance(tokens, list):
        dict_frequencies = {}
        for token in tokens:  # иттерация по элементам списка tokens
            if isinstance(token, str):  # проверка является ли token строкой
                if token in dict_frequencies:  # если token есть в словаре, то добавляю один
                    dict_frequencies[token] += 1
                else:  # иначе присваиваю один
                    dict_frequencies[token] = 1
        if dict_frequencies:
            return dict_frequencies
        else:
            return None
    else:
        return None


def get_top_n_words(freq_dict: dict, top_n: int) -> list or None:
    """
    Returns the most common words
    :param freq_dict: a dictionary with frequencies
    :param top_n: a number of the most common words
    :return: a list of the most common words
    """
    if isinstance(freq_dict, dict) and isinstance(top_n, int):
        # сортировка словаря в обратном порядке, по второму элементу
        freq_dict = dict(sorted(freq_dict.items(), reverse=True, key=lambda value: value[1]))
        most_common_words = list(
            freq_dict)  # превращение словаря в список, который будет состоять только из ключей словаря
        most_common_words = most_common_words[:top_n]  # выборка первых top_n элементов из списка
        return most_common_words
    else:
        return None
