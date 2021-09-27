"""
Lab 1
Language detection
"""
import re  # импортируем модуль re для последующей работы с регулярными выражениями


def tokenize(text: str) -> list or None:
    """
    Splits a text into tokens, converts the tokens into lowercase,
    removes punctuation and other symbols from words
    :param text: a text
    :return: a list of lower-cased tokens without punctuation
    """

    if not isinstance(text, str):
        return None
    text = text.lower()
    text = re.sub('[^a-zäöüß ]', '', str(text))   # заменяем символы (кроме букв) на пробел
    text = text.split()   # с помощью split разбиваем строку на части

    return text


def remove_stop_words(tokens: list, stop_words: list) -> list or None:
    """
    Removes stop words
    :param tokens: a list of tokens
    :param stop_words: a list of stop words
    :return: a list of tokens without stop words
    """

    if not isinstance(tokens, list) or not isinstance(stop_words, list):
        return None
    tokens = [token for token in tokens if token not in stop_words]

    return tokens


def calculate_frequencies(tokens: list) -> dict or None:
    """
    Calculates frequencies of given tokens
    :param tokens: a list of tokens
    :return: a dictionary with frequencies
    """

    if not isinstance(tokens, list):
        return None
    freq_dict = {}  # создаем частотный словарь
    for token in tokens:
        if not isinstance(token, str):
            return None
        if token not in freq_dict:
            freq_dict[token] = 1
        else:
            freq_dict[token] += 1
    return freq_dict


def get_top_n_words(freq_dict: dict, top_n: int) -> list or None:
    """
    Returns the most common words
    :param freq_dict: a dictionary with frequencies
    :param top_n: a number of the most common words
    :return: a list of the most common words
    """

    if not isinstance(freq_dict, dict):
        return None

    freq_dict_sorted = dict(sorted(freq_dict.items(), key=lambda x: -x[1]))
    # с помощью items возвращаем k и v
    # key позволяет уточнить критерий,
    # по которому происходит сортировка, x - это элемент списка
    # x[1] - частота токена
    # поскольку по умолчанию сортировка идет по возрастанию, необходимо поставить "-"
    most_common_words = list(freq_dict_sorted)
    most_common_words = most_common_words[:top_n]
    # с помощью среза выбираем топ-n по популярности слов
    return most_common_words


def create_language_profile(language: str, text: str, stop_words: list) -> dict or None:
    """
    Creates a language profile
    :param language: a language
    :param text: a text
    :param stop_words: a list of stop words
    :return: a dictionary with three keys – name, freq, n_words
    """

    if not (isinstance(language, str)
            and isinstance(text, str)
            and isinstance(stop_words, list)):
        return None
    language_profile = {}  # создаем словарь - профиль языка
    frequencies = calculate_frequencies(remove_stop_words(tokenize(text), stop_words))
    # получаем частотный словарь
    n_words = len(frequencies)   # получаем количество токенов в словаре
    language_profile['freq'] = frequencies   # ключ - freq, значение - частотный словарь
    language_profile['name'] = language   # ключ - name, значение - конкретный язык
    language_profile['n_words'] = n_words   # ключ - n_words, значение - количество токенов
    return language_profile


def compare_profiles(unknown_profile: dict, profile_to_compare: dict, top_n: int) -> float or None:
    """
    Compares profiles and calculates the distance using top n words
    :param unknown_profile: a dictionary
    :param profile_to_compare: a dictionary
    :param top_n: a number of the most common words
    :return: the distance
    """

    if not (isinstance(unknown_profile, dict)
            and isinstance(profile_to_compare, dict)
            and isinstance(top_n, int)):
        return None

    compare_top = get_top_n_words(profile_to_compare['freq'], top_n)  # получаем топ-n слов известного языка
    unknown_top = get_top_n_words(unknown_profile['freq'], top_n)  # получаем топ-n слов на неизвестном языке
    unknown_top_len = len(unknown_top)   # получаем длину списка токенов на неизвестном языке

    count = 0
    if compare_top == unknown_top:
        top_common_words = float(1)   # если топ-n слов у этих языков совпадают, доля пересекающихся слов равна 1
    else:
        for word in compare_top:
            if word in unknown_top:
                count += 1   # если слово присутствует в топ-n словах двух языков, то прибавляем 1
        top_common_words = round(count / unknown_top_len)    # делим общие слова на длину списка токенов
        #  на неизвестном языке
    return top_common_words


def detect_language(unknown_profile: dict, profile_1: dict, profile_2: dict, top_n: int) -> str or None:
    """
    Detects the language of an unknown profile
    :param unknown_profile: a dictionary
    :param profile_1: a dictionary
    :param profile_2: a dictionary
    :param top_n: a number of the most common words
    :return: a language
    """
    if not isinstance(unknown_profile, dict) or not isinstance(profile_1, dict):
        return None
    if not isinstance(profile_2, dict) or not isinstance(top_n, int):
        return None

    compare_1 = compare_profiles(profile_1, unknown_profile, top_n)
    compare_2 = compare_profiles(profile_2, unknown_profile, top_n)   # сравниваем известный и неизвестный языки
    # по топ-n слов

    if compare_1 > compare_2:
        language = profile_1['name']
    elif compare_1 < compare_2:
        language = profile_2['name']
    else:
        languages = [profile_1['name'], profile_2['name']]
        language_sorted = sorted(languages, key=lambda x: (x[0]))
        language = language_sorted[:1]  # если значения доли пересекающихся частотных слов совпадают,
        # сортируем языки в алфавитном порядке и с помощью срезов возьмем первый язык
    return language


def compare_profiles_advanced(unknown_profile: dict, profile_to_compare: dict, top_n: int):
    """
    Compares profiles and calculates some advanced parameters
    :param unknown_profile: a dictionary
    :param profile_to_compare: a dictionary
    :param top_n: a number of the most common words
    :return: a dictionary with 7 keys – name, score, common, sorted_common, max_length_word,
    min_length_word, average_token_length
    """


def detect_language_advanced(unknown_profile: dict, profiles: list, languages: list, top_n: int):
    """
    Detects the language of an unknown profile within the list of possible languages
    :param unknown_profile: a dictionary
    :param profiles: a list of dictionaries
    :param languages: a list of possible languages
    :param top_n: a number of the most common words
    :return: a language
    """


def load_profile(path_to_file: str):
    """
    Loads a language profile
    :param path_to_file: a path
    :return: a dictionary with three keys – name, freq, n_words
    """


def save_profile(profile: dict):
    """
    Saves a language profile
    :param profile: a dictionary
    :return: 0 if everything is ok, 1 if not
    """
