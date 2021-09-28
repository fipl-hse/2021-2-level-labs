"""
Lab 1
Language detection
"""
import json
from os.path import exists


def tokenize(text: str) -> list or None:
    """
    Splits a text into tokens, converts the tokens into lowercase,
    removes punctuation and other symbols from words
    :param text: a text
    :return: a list of lower-cased tokens without punctuation
    """
    if not isinstance(text, str):
        return None

    low_text = text.lower()
    clean_text = ''
    for i in low_text:
        if i.isalpha() or i.isspace():
            clean_text += i

    tokens = clean_text.split()
    return tokens


def remove_stop_words(tokens: list, stop_words: list) -> list or None:
    """
    Removes stop words
    :param tokens: a list of tokens
    :param stop_words: a list of stop words
    :return: a list of tokens without stop words
    """
    if not isinstance(tokens, list) or not tokens:
        return None
    if not isinstance(stop_words, list):
        return tokens

    for i in stop_words:
        for k in tokens:
            if i == k:
                tokens.remove(k)
    return tokens


def calculate_frequencies(tokens: list) -> dict or None:
    """
    Calculates frequencies of given tokens
    :param tokens: a list of tokens
    :return: a dictionary with frequencies
    """
    if not isinstance(tokens, list):
        return None
    for i in tokens:
        if not i:
            return None

    freq_dict = {i: tokens.count(i) for i in tokens}
    return freq_dict


def get_top_n_words(freq_dict: dict, top_n: int) -> list or None:
    """
    Returns the most common words
    :param freq_dict: a dictionary with frequencies
    :param top_n: a number of the most common words
    :return: a list of the most common words
    """
    if not isinstance(freq_dict, dict) or not isinstance(top_n, int):
        return None
    if not freq_dict or top_n <= 0:
        return []

    sort_dict = sorted(freq_dict, key=freq_dict.get, reverse=True)
    top_n_words = sort_dict[:top_n]
    return top_n_words


def create_language_profile(language: str, text: str, stop_words: list) -> dict or None:
    """
    Creates a language profile
    :param language: a language
    :param text: a text
    :param stop_words: a list of stop words
    :return: a dictionary with three keys – name, freq, n_words
    """
    if not isinstance(language, str) or not isinstance(text, str):
        return None
    if not isinstance(stop_words, list):
        return None

    freq_dict = calculate_frequencies(remove_stop_words(tokenize(text), stop_words))

    language_profile = dict(name=language, freq=freq_dict, n_words=len(freq_dict))
    return language_profile


def compare_profiles(unknown_profile: dict, profile_to_compare: dict, top_n: int) -> float or None:
    """
    Compares profiles and calculates the distance using top n words
    :param unknown_profile: a dictionary
    :param profile_to_compare: a dictionary
    :param top_n: a number of the most common words
    :return: the distance
    """
    if not isinstance(unknown_profile, dict) or not isinstance(profile_to_compare, dict):
        return None
    if not isinstance(top_n, int):
        return None

    top_n_words_unk = get_top_n_words(unknown_profile['freq'], top_n)
    top_n_words = get_top_n_words(profile_to_compare['freq'], top_n)

    count_common = 0
    for i in top_n_words_unk:
        for k in top_n_words:
            if i == k:
                count_common += 1

    distance = round(count_common / len(top_n_words_unk), 2)
    return distance


def detect_language(unknown_profile: dict, profile_1: dict,
                    profile_2: dict, top_n: int) -> str or None:
    """
    Detects the language of an unknown profile
    :param unknown_profile: a dictionary
    :param profile_1: a dictionary
    :param profile_2: a dictionary
    :param top_n: a number of the most common words
    :return: a language
    """
    if not isinstance(profile_1, dict) or not isinstance(profile_2, dict):
        return None
    if not isinstance(unknown_profile, dict) or not isinstance(top_n, int):
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


def compare_profiles_advanced(unknown_profile: dict, profile_to_compare: dict,
                              top_n: int) -> list or None:
    """
    Compares profiles and calculates some advanced parameters
    :param unknown_profile: a dictionary
    :param profile_to_compare: a dictionary
    :param top_n: a number of the most common words
    :return: a dictionary with 7 keys – name, score, common, sorted_common, max_length_word,
    min_length_word, average_token_length
    """
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
              'max_length_word': max_len, 'min_length_word': min_len,
              'average_token_length': average_len, 'sorted_common': sorted_common}
    return report


def detect_language_advanced(unknown_profile: dict, profiles: list,
                             languages: list, top_n: int) -> str or None:
    """
    Detects the language of an unknown profile within the list of possible languages
    :param unknown_profile: a dictionary
    :param profiles: a list of dictionaries
    :param languages: a list of possible languages
    :param top_n: a number of the most common words
    :return: a language
    """
    if not isinstance(unknown_profile, dict) or not isinstance(top_n, int) or \
            not isinstance(profiles, list) or not isinstance(languages, list):
        return None

    all_languages = [i['name'] for i in profiles]
    for i in languages:
        if i not in all_languages:
            return None

    reports = []
    for i in profiles:
        if i['name'] in languages or not languages:
            reports.append(compare_profiles_advanced(unknown_profile, i, top_n))

    scores = []
    possible_languages = []
    for i in reports:
        scores.append(i['score'])
    for i in reports:
        if i['score'] == max(scores):
            possible_languages.append(i['name'])

    language = sorted(possible_languages)[0]
    return language


def load_profile(path_to_file: str) -> dict or None:
    """
    Loads a language profile
    :param path_to_file: a path
    :return: a dictionary with three keys – name, freq, n_words
    """
    if not isinstance(path_to_file, str):
        return None
    if not exists(path_to_file):
        return None

    with open(path_to_file, encoding='utf-8') as file:
        language_profile = json.load(file)
    return language_profile


def save_profile(profile: dict) -> int:
    """
    Saves a language profile
    :param profile: a dictionary
    :return: 0 if everything is ok, 1 if not
    """
    if not isinstance(profile, dict):
        return 1
    if ('name' or 'freq' or 'n_words') not in profile.keys():
        return 1
    file_name = '{}.json'.format(profile['name'])
    with open(file_name, 'w', encoding='utf-8') as file:
        json.dump(profile, file)
    return 0
