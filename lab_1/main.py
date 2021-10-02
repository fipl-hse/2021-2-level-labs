"""
Lab 1
Language detection
"""

import re

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
        "freq": calculate_frequencies(),
        "n_words": get_top_n_words()
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
    top_n_unknown = get_top_n_words()
    top_n_compare = get_top_n_words()
    common_words = []
    for i in top_n_compare:
        if i in top_n_unknown:
            common_words.append(i)
    compare_list = len(common_words)/len(top_n_unknown)
    return compare_list