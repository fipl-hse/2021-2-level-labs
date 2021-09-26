"""
Lab 1
Language detection
"""
import json


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

    if not isinstance(unknown_profile, dict):
        return None
    if not isinstance(profiles, list) or not isinstance(languages, list):
        return None
    if not isinstance(top_n, int):
        return None
    all_languages = [i['name'] for i in profiles]
    for i in languages:
        if i not in all_languages:
            return None

    scores = []
    possible_profiles = []
    possible_languages = []

    if not languages:
        for i in profiles:
            report = compare_profiles_advanced(unknown_profile, i, top_n)
            scores.append(report['score'])
        for i in profiles:
            report = compare_profiles_advanced(unknown_profile, i, top_n)
            if report['score'] == max(scores):
                possible_languages.append(report['name'])
    else:
        for i in profiles:
            if i['name'] in languages:
                possible_profiles.append(i)
        for i in possible_profiles:
            report = compare_profiles_advanced(unknown_profile, i, top_n)
            scores.append(report['score'])
        for i in possible_profiles:
            report = compare_profiles_advanced(unknown_profile, i, top_n)
            if report['score'] == max(scores):
                possible_languages.append(report['name'])

    if len(possible_languages) > 1:
        language = sorted(possible_languages)[0]
    else:
        language = possible_languages[0]
    return language


def load_profile(path_to_file: str) -> dict or None:
    """
    Loads a language profile
    :param path_to_file: a path
    :return: a dictionary with three keys – name, freq, n_words
    """
    if not isinstance(path_to_file, str):
        return None
    try:
        with open(path_to_file, encoding='utf-8') as file:
            language_profile = json.load(file)
    except FileNotFoundError:
        return None
    return language_profile


def save_profile(profile: dict) -> int:

    if not isinstance(profile, dict):
        return 1
    if ('name' or 'freq' or 'n_words') not in profile.keys():
        return 1
    profile_file = '{} profile.json'.format(profile['name'])
    with open(profile_file, 'w', encoding='utf-8') as file:
        json.dump(profile, file)
    return 0
