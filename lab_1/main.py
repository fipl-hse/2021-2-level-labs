"""
Lab 1
Language detection
"""

import re
from typing import Optional, List, Any, Callable


def tokenize(text: str) -> list or None:
    """
    Splits a text into tokens, converts the tokens into lowercase,
    removes punctuation and other symbols from words
    :param text: a text
    :return: a list of lower-cased tokens without punctuation
    """
    if not isinstance(text, str):
        return None
    text_output = re.sub('[^a-zäöüß \n]', '', text.lower()).split()
    return text_output


def remove_stop_words(tokens: list, stop_words: list) -> list or None:
    """
    Removes stop words
    :param tokens: a list of tokens
    :param stop_words: a list of stop words
    :return: a list of tokens without stop words
    """
    if not isinstance(tokens, list) or not isinstance(stop_words, list):
        return None
    if len(tokens) == 0:
        return None
    filtered_word_list = []
    for word in tokens:
        if word not in stop_words:
            filtered_word_list.append(word)
    return filtered_word_list


def calculate_frequencies(tokens: list) -> dict or None:
    """
    Calculates frequencies of given tokens
    :param tokens: a list of tokens
    :return: a dictionary with frequencies
    """
    if not isinstance(tokens, list):
        return None
    if len(tokens) > 0 and not isinstance(tokens[0], str):
        return None
    set_words = set(tokens.copy())
    dict_freq = {word: tokens.count(word) for word in set_words}
    return dict_freq


def get_top_n_words(freq_dict: dict, top_n: int) -> list or None:
    """
    Returns the most common words
    :param freq_dict: a dictionary with frequencies
    :param top_n: a number of the most common words
    :return: a list of the most common words
    """
    if not isinstance(freq_dict, dict) or not isinstance(top_n, int):
        return None
    list_output = sorted(freq_dict, key=freq_dict.get, reverse=True)
    return list_output[:top_n]


def create_language_profile(language: str, text: str, stop_words: list) -> dict or None:
    """
    Creates a language profile
    :param language: a language
    :param text: a text
    :param stop_words: a list of stop words
    :return: a dictionary with three keys – name, freq, n_words
    """
    if not isinstance(language, str) or not isinstance(text, str) \
            or not isinstance(stop_words, list):
        return None
    language_profile = {
        "name": language,
        "freq": calculate_frequencies,
        "n_words": get_top_n_words
    }
    return language_profile


def compare_profiles(unknown_profile: dict, profile_to_compare: dict, top_n: int) -> float or None:
    """
    Compares profiles and calculates the distance using top n words
    :param unknown_profile: a dictionary
    :param profile_to_compare: a dictionary
    :param top_n: a number of the most common words
    :return: the distance
    """
    if not isinstance(unknown_profile, dict) or not isinstance(profile_to_compare, dict) \
            or not isinstance(top_n, int):
        return None
    top_n_unknown = get_top_n_words(unknown_profile, top_n)
    top_n_compare = get_top_n_words(profile_to_compare, top_n)
    common_words = []
    for i in top_n_compare:
        if i in top_n_unknown:
            common_words.append(i)
    compare_list = len(common_words) / len(top_n_unknown)
    return compare_list


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
    if not isinstance(unknown_profile, dict) or not isinstance(profile_1, dict) \
            or not isinstance(profile_2, dict) or not isinstance(top_n, int):
        return None
    compare_1 = compare_profiles(unknown_profile, profile_1, top_n)
    compare_2 = compare_profiles(unknown_profile, profile_2, top_n)
    if compare_1 > compare_2:
        return profile_1['name']
    elif compare_2 > compare_1:
        return profile_2['name']
    else:
        language_list = [profile_1['name'], profile_2['name']]
        language_list = sorted(language_list)
        return language_list[0]



def compare_profiles_advanced(unknown_profile: dict, profile_to_compare: dict,
                              top_n: int, ) -> list or None:
    """
    Compares profiles and calculates some advanced parameters
    :param unknown_profile: a dictionary
    :param profile_to_compare: a dictionary
    :param top_n: a number of the most common words
    :return: a dictionary with 7 keys – name, score, common, sorted_common, max_length_word,
    min_length_word, average_token_length
    """
    if not isinstance(unknown_profile, dict) or not isinstance(profile_to_compare, dict) \
            or not isinstance(top_n, int):
        return None
    tokens_profile_to_compare = tokenize(profile_to_compare['freq'])
    top_n_unknown = get_top_n_words(unknown_profile, top_n)
    top_n_compare = get_top_n_words(profile_to_compare, top_n)
    common_words = []
    for i in top_n_compare:
        if i in top_n_unknown:
            common_words.append(i)
    language_profile_advanced = {'name': profile_to_compare.get('name'),
                                 'common': common_words,
                                 'score': compare_profiles(unknown_profile, profile_to_compare, top_n),
                                 'max_length_word': max(tokens_profile_to_compare),
                                 'min_length_word': min(tokens_profile_to_compare),
                                 'average_token_length': sum(tokens_profile_to_compare) / len(
                                     tokens_profile_to_compare),
                                 'sorted_common': sorted(common_words)
                                 }
    return language_profile_advanced

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
    if not isinstance(unknown_profile, dict) or not isinstance(profiles, list) \
            or not isinstance(languages, list) or not isinstance(top_n, int):
        return None
    language_score = {}
    for profile_to_compare in profiles:
        if (profile_to_compare['name'] in languages) or not languages:
            comparison = compare_profiles_advanced(unknown_profile, profile_to_compare, top_n)
            language_score.update({comparison['name']: comparison['score']})
    if language_score == {}:
        return None
    else:
        name_of_language = []
        for name, score in language_score.items():
            if score == max(language_score.values()):
                name_of_language.append(name)
    name_of_language = sorted(name_of_language)
    return name_of_language[0]

