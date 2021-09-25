"""
Lab 1
Language detection
"""


def tokenize(text: str) -> list or None:

    if not isinstance(text, str):
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

    if not isinstance(tokens, list) or not tokens:
        return None
    if not isinstance(stop_words, list):
        return tokens

    for i in stop_words:
        for n in tokens:
            if i == n:
                tokens.remove(n)
    return tokens


def calculate_frequencies(tokens: list) -> dict or None:

    if not isinstance(tokens, list):
        return None
    for i in tokens:
        if not i:
            return None

    freq_dict = {i: tokens.count(i) for i in tokens}
    return freq_dict


def get_top_n_words(freq_dict: dict, top_n: int) -> list or None:

    if not isinstance(freq_dict, dict):
        return None
    if not isinstance(top_n, int):
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
                dict_keys.remove(k)
                # удаляет использованный ключ из списка, чтобы чтобы ключ с повторяющимся значением не игнорировался

    freq_list = list(sort_dict.keys())

    if top_n > len(freq_list):
        return freq_list
    else:
        top_n_words = freq_list[:top_n]
    return top_n_words


def create_language_profile(language: str, text: str, stop_words: list) -> dict or None:

    if not isinstance(language, str) or not isinstance(text, str):
        return None
    if not isinstance(stop_words, list):
        return None

    freq_dict = calculate_frequencies(remove_stop_words(tokenize(text), stop_words))

    language_profile = dict(name=language, freq=freq_dict, n_words=len(freq_dict))
    return language_profile


def compare_profiles(unknown_profile: dict, profile_to_compare: dict, top_n: int) -> float or None:

    if not isinstance(unknown_profile, dict) or not isinstance(profile_to_compare, dict):
        return None
    if not isinstance(top_n, int):
        return None

    freq_dict_unk = unknown_profile['freq']
    freq_dict = profile_to_compare['freq']

    top_n_words_unk = get_top_n_words(freq_dict_unk, top_n)
    top_n_words = get_top_n_words(freq_dict, top_n)

    count_common = 0
    for i in top_n_words_unk:
        for k in top_n_words:
            if i == k:
                count_common += 1

    distance = round(count_common / len(top_n_words_unk), 2)
    return distance


def detect_language(unknown_profile: dict, profile_1: dict, profile_2: dict, top_n: int) -> str or None:

    if not isinstance(unknown_profile, dict) or not isinstance(profile_1, dict) or not isinstance(profile_2, dict):
        return None
    if not isinstance(top_n, int):
        return None

    distance_1 = compare_profiles(unknown_profile, profile_1, top_n)
    distance_2 = compare_profiles(unknown_profile, profile_2, top_n)

    if distance_1 > distance_2:
        language = profile_1['name']
    elif distance_1 == distance_2:
        names = [profile_1['name'], profile_2['name']]
        language = sorted(names)[0]
    else:
        language = profile_2['name']
    return language


def compare_profiles_advanced(unknown_profile: dict, profile_to_compare: dict, top_n: int) -> list or None:

    if not isinstance(unknown_profile, dict) or not isinstance(profile_to_compare, dict):
        return None
    if not isinstance(top_n, int):
        return None

    top_n_words = get_top_n_words(profile_to_compare['freq'], top_n)
    top_n_words_unk = get_top_n_words(unknown_profile['freq'], top_n)

    top_n_common = []
    for i in top_n_words:
        if i in top_n_words_unk:
            top_n_common.append(i)
    score = len(top_n_common) / len(top_n_words_unk)
    sorted_common = sorted(top_n_common)

    tokens = list(profile_to_compare['freq'].keys())
    max_len = max(tokens, key=len)
    min_len = min(tokens, key=len)
    tokens_len = []
    for i in tokens:
        tokens_len.append(len(i))
    average_len = sum(tokens_len) / len(tokens)

    report = {'name': profile_to_compare['name'], 'common': top_n_common, 'score': score,
              'max_length_word': max_len, 'min_length_word': min_len, 'average_token_length': average_len,
              'sorted_common': sorted_common}
    return report


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
