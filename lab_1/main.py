"""
Lab 1
Language detection
"""

import json
import os
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
    text = text.lower()
    string_with_tokens = ""
    for i in text:
        if i.isalpha() or i.isspace():
            string_with_tokens += i
    tokens = string_with_tokens.split()
    return tokens


def remove_stop_words(tokens: list, stop_words: list) -> list or None:
    """
    Removes stop words
    :param tokens: a list of tokens
    :param stop_words: a list of stop words
    :return: a list of tokens without stop words
    """
    if not isinstance(tokens, list) or not isinstance(stop_words, list):
        return None
    tokens = [i for i in tokens if i not in stop_words]
    return tokens


def calculate_frequencies(tokens: list) -> dict or None:
    """
    Calculates frequencies of given tokens
    :param tokens: a list of tokens
    :return: a dictionary with frequencies
    """
    if not (isinstance(tokens, list) and all(isinstance(i, str) for i in tokens)):
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
    if not (isinstance(freq_dict, dict) and isinstance(top_n, int)):
        return None
    if freq_dict != {} and top_n > 0:
        top_list = []
        sorted_keys = sorted(freq_dict, key=freq_dict.get, reverse=True)
        count = 1
        for i in sorted_keys:
            if count <= top_n:
                top_list.append(i)
                count += 1
            if count > top_n:
                break
        return top_list
    return []


def create_language_profile(language: str, text: str, stop_words: list) -> dict or None:
    """
    Creates a language profile
    :param language: a language
    :param text: a text
    :param stop_words: a list of stop words
    :return: a dictionary with three keys – name, freq, n_words
    """
    first_step = tokenize(text)
    second_step = remove_stop_words(first_step, stop_words)
    freq_dict = calculate_frequencies(second_step)
    if not (isinstance(language, str) and isinstance(text, str) and isinstance(stop_words, list)):
        return None
    language_profile = {"name": language,
                        "freq": freq_dict,
                        "n_words": len(freq_dict)}
    return language_profile


def compare_profiles(unknown_profile: dict, profile_to_compare: dict, top_n: int) -> float or None:
    """
    Compares profiles and calculates the distance using top n words
    :param unknown_profile: a dictionary
    :param profile_to_compare: a dictionary
    :param top_n: a number of the most common words
    :return: the distance
    """
    if not (isinstance(unknown_profile, dict) \
            and isinstance(profile_to_compare, dict) \
            and isinstance(top_n, int)):
        return None
    top_n_common_words = []
    top_n_words_unknown_profile = get_top_n_words(unknown_profile['freq'], top_n)
    top_n_words_known_profile = get_top_n_words(profile_to_compare['freq'], top_n)
    for i in top_n_words_unknown_profile:
        if i in top_n_words_known_profile:
            top_n_common_words.append(i)
    distance = len(top_n_common_words) / len(top_n_words_unknown_profile)
    return round(float(distance), 2)


def detect_language(unknown_profile: dict,
                    profile_1: dict,
                    profile_2: dict,
                    top_n: int) -> str or None:
    """
    Detects the language of an unknown profile
    :param unknown_profile: a dictionary
    :param profile_1: a dictionary
    :param profile_2: a dictionary
    :param top_n: a number of the most common words
    :return: a language
    """
    if not (isinstance(unknown_profile, dict)
            and isinstance(profile_1, dict)
            and isinstance(profile_2, dict)
            and isinstance(top_n, int)):
        return None
    first_intersecting_words = compare_profiles(unknown_profile, profile_1, top_n)
    second_intersecting_words = compare_profiles(unknown_profile, profile_2, top_n)
    if first_intersecting_words > second_intersecting_words:
        return profile_1['name']
    if second_intersecting_words > first_intersecting_words:
        return profile_2['name']
    return [[profile_1['name'], profile_2['name']].sort()][0]


def compare_profiles_advanced(unknown_profile: dict,
                              profile_to_compare: dict,
                              top_n: int) -> dict or None:
    """
    Compares profiles and calculates some advanced parameters
    :param unknown_profile: a dictionary
    :param profile_to_compare: a dictionary
    :param top_n: a number of the most common words
    :return: a dictionary with 7 keys – name, score, common, sorted_common, max_length_word,
    min_length_word, average_token_length
    """
    if not (isinstance(unknown_profile, dict)
            and isinstance(profile_to_compare, dict)
            and isinstance(top_n, int)):
        return None
    common = []
    top_n_words_unknown_profile = get_top_n_words(unknown_profile['freq'], top_n)
    top_n_words_known_profile = get_top_n_words(profile_to_compare['freq'], top_n)
    for i in top_n_words_known_profile:
        if i in top_n_words_unknown_profile:
            common.append(i)
    sorted_common = sorted(common)
    score = len(common) / len(top_n_words_known_profile)
    profile_to_compare_keys = list(profile_to_compare['freq'].keys())
    sorted_keys = sorted(profile_to_compare_keys, key=len)
    max_length_word = sorted_keys[-1]
    min_length_word = sorted_keys[0]
    average_token_length = len(''.join(profile_to_compare_keys)) / len(profile_to_compare_keys)
    full_profile = {'name': profile_to_compare['name'],
                    'common': common,
                    'score': score,
                    'max_length_word': max_length_word,
                    'min_length_word': min_length_word,
                    'average_token_length': average_token_length,
                    'sorted_common': sorted_common}
    return full_profile


def detect_language_advanced(unknown_profile: dict,
                             profiles: list,
                             languages: list,
                             top_n: int) -> str or None:
    """
    Detects the language of an unknown profile within the list of possible languages
    :param unknown_profile: a dictionary
    :param profiles: a dictionary
    :param languages: a list of possible languages
    :param top_n: a number of the most common words
    :return: a language
    """
    if not (isinstance(unknown_profile, dict)
            and isinstance(profiles, list)
            and isinstance(languages, list)
            and isinstance(top_n, int)):
        return None
    if languages or not languages:
        score = {}
        if not languages:
            for i in profiles:
                languages.append(i['name'])
        for language in profiles:
            if language['name'] in languages:
                full_profile = compare_profiles_advanced(unknown_profile, language, top_n)
                score.update({language['name']: full_profile['score']})
        if not score:
            return None
        score_sorted = (sorted(score, key=score.get, reverse=True))[0]
        return score_sorted
    return None

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
    with open(path_to_file, 'r', encoding='utf-8') as file:
        opened_file = json.load(file)
        return opened_file


def save_profile(profile: dict) -> int:
    """
    Saves a language profile
    :param profile: a dictionary
    :return: 0 if everything is ok, 1 if not
    """
    if isinstance(profile, dict):
        if isinstance(profile['name'], str) \
                and isinstance(profile['freq'], dict) \
                and isinstance(profile['n_words'], int):
            path = 'D:\\projects\\2021-2-level-labs\\lab_1\\profiles'
            with open(os.path.join(path, "{}.json".format(profile['name'])),
                      "w", encoding="utf-8") as file:
                json.dump(profile, file)
                return 0
        else:
            return 1
    else:
        return 1
