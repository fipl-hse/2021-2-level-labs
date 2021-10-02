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

    text = re.split(r"[^\w\s]", text)
    text = "".join(text)
    text = text.lower()
    tokens = re.findall(r"\w+", text)
    return tokens


def remove_stop_words(tokens: list, stop_words: list) -> list or None:
    """
    Removes stop words
    :param tokens: a list of tokens
    :param stop_words: a list of stop words
    :return: a list of tokens without stop words
    """

    if not (isinstance(tokens, list) and isinstance(stop_words, list)):
        return None

    filt_tokens = []
    for token in tokens:
        if isinstance(token, str) and token not in stop_words:
            filt_tokens.append(token)
    return filt_tokens


def calculate_frequencies(tokens: list) -> dict or None:
    """
    Calculates frequencies of given tokens
    :param tokens: a list of tokens
    :return: a dictionary with frequencies
    """

    if not isinstance(tokens, list):
        return None

    for token in tokens:
        if not isinstance(token, str):
            return None

    freq_dict = {}
    for word in tokens:
        if word not in freq_dict:
            freq_dict[word] = 1
        else:
            freq_dict[word] += 1
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

    freq_items = dict(sorted(freq_dict.items(), key=lambda x: x[1], reverse=True))
    top_words = list(freq_items.keys())
    top_words = top_words[:top_n]
    return top_words


def create_language_profile(language: str, text: str, stop_words: list) -> dict or None:
    """
    Creates a language profile
    :param language: a language
    :param text: a text
    :param stop_words: a list of stop words
    :return: a dictionary with three keys – name, freq, n_words
    """

    if not (isinstance(language, str) and isinstance(text, str) and isinstance(stop_words, list)):
        return None

    freq_dict = calculate_frequencies(remove_stop_words(tokenize(text), stop_words))
    language_profile = {'name': language, 'freq': freq_dict, 'n_words': len(freq_dict)}
    return language_profile


def compare_profiles(unknown_profile: dict, profile_to_compare: dict, top_n: int) -> float or None:
    """
    Compares profiles and calculates the distance using top n words
    :param unknown_profile: a dictionary
    :param profile_to_compare: a dictionary
    :param top_n: a number of the most common words
    :return: the distance
    """

    if not (isinstance(unknown_profile, dict) and isinstance(profile_to_compare, dict) and isinstance(top_n, int)):
        return None

    top_unknown = get_top_n_words(unknown_profile['freq'], top_n)
    top_language_compare = get_top_n_words(profile_to_compare['freq'], top_n)

    compared_list = []
    for word in top_unknown:
        if word in top_language_compare:
            compared_list.append(word)


    score = round(len(compared_list)/len(top_unknown), 2)
    return score


def detect_language(unknown_profile: dict, profile_1: dict, profile_2: dict, top_n: int) -> str or None:
    """
    Detects the language of an unknown profile
    :param unknown_profile: a dictionary
    :param profile_1: a dictionary
    :param profile_2: a dictionary
    :param top_n: a number of the most common words
    :return: a language
    """

    if not (isinstance(unknown_profile, dict) and isinstance(profile_1, dict) \
            and isinstance(profile_2, dict) and isinstance(top_n, int)):
        return None

    score_en = compare_profiles(unknown_profile, profile_1, top_n)
    score_de = compare_profiles(unknown_profile, profile_2, top_n)

    if score_en > score_de:
        language_unknown = profile_1['name']
    elif score_en < score_de:
        language_unknown = profile_2['name']
    else:
        prof = [profile_1['name'], profile_2['name']]
        prof = sorted(prof)
        language_unknown = prof[0]
    return language_unknown