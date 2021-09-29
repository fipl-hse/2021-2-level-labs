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
