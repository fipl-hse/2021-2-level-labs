"""
Lab 1
Language detection
"""

def tokenize(text: str) -> list or None:

    if type(text) != str:
        return None

    low_text = text.lower()
    clean_text = ''
    for i in low_text:
        if i.isalpha():
            clean_text += i
        elif i.isspace():
            clean_text += i
    clean_text = clean_text.replace('\n', ' ')
    tokens = clean_text.split()
    return tokens


def remove_stop_words(tokens: list, stop_words: list) -> list or None:

    if type(tokens) != list or not tokens:
        return None
    if type(stop_words) != list:
        return tokens

    for i in stop_words:
        for n in tokens:
            if i == n:
                tokens.remove(i)
    return tokens


def calculate_frequencies(tokens: list) -> dict or None:

    if type(tokens) != list:
        return None
    for i in tokens:
        if not i:
            return None

    freq_dict = {i: tokens.count(i) for i in tokens}
    return freq_dict


def get_top_n_words(freq_dict: dict, top_n: int) -> list or None:

    if type(freq_dict) != dict:
        return None
    if type(top_n) != int:
        return None
    if not freq_dict or top_n <= 0:
        return []

    sort_values = sorted(freq_dict.values(), reverse=True)  # составляет список значений и сортирует его
    dict_keys = list(freq_dict.keys())  # составляет список ключей
    sort_dict = {}

    for i in sort_values:
        for k in dict_keys:
            if freq_dict[k] == i:  # вызывает значение из словаря по ключу и сравнивает его со значением из sort_values
                sort_dict[k] = freq_dict[k]  # добавляет пару в новый отсортированный словарь
                dict_keys.remove(k)  # удаляет использованный ключ из списка, чтобы чтобы ключ с повторяющимся значением не игнорировался

    freq_list = list(sort_dict.keys())

    if top_n > len(freq_list):
        return freq_list
    else:
        top_n_words = freq_list[:top_n]
    return top_n_words


def create_language_profile(language: str, text: str, stop_words: list) -> dict or None:
    """
    Creates a language profile
    :param language: a language
    :param text: a text
    :param stop_words: a list of stop words
    :return: a dictionary with three keys – name, freq, n_words
    """
    pass


def compare_profiles(unknown_profile: dict, profile_to_compare: dict, top_n: int) -> float or None:
    """
    Compares profiles and calculates the distance using top n words
    :param unknown_profile: a dictionary
    :param profile_to_compare: a dictionary
    :param top_n: a number of the most common words
    :return: the distance
    """
    pass


def detect_language(unknown_profile: dict, profile_1: dict, profile_2: dict, top_n: int) -> str or None:
    """
    Detects the language of an unknown profile
    :param unknown_profile: a dictionary
    :param profile_1: a dictionary
    :param profile_2: a dictionary
    :param top_n: a number of the most common words
    :return: a language
    """
    pass


def compare_profiles_advanced(unknown_profile: dict, profile_to_compare: dict, top_n: int) -> list or None:
    """
    Compares profiles and calculates some advanced parameters
    :param unknown_profile: a dictionary
    :param profile_to_compare: a dictionary
    :param top_n: a number of the most common words
    :return: a dictionary with 7 keys – name, score, common, sorted_common, max_length_word,
    min_length_word, average_token_length
    """
    pass


def detect_language_advanced(unknown_profile: dict, profiles: list, languages: list, top_n: int) -> str or None:
    """
    Detects the language of an unknown profile within the list of possible languages
    :param unknown_profile: a dictionary
    :param profiles: a list of dictionaries
    :param languages: a list of possible languages
    :param top_n: a number of the most common words
    :return: a language
    """
    pass


def load_profile(path_to_file: str) -> dict or None:
    """
    Loads a language profile
    :param path_to_file: a path
    :return: a dictionary with three keys – name, freq, n_words
    """
    pass


def save_profile(profile: dict) -> int:
    """
    Saves a language profile
    :param profile: a dictionary
    :return: 0 if everything is ok, 1 if not
    """
    pass
