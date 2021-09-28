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
    if isinstance(text, str):
        text = text.lower()
        list_of_punctuation = ["'", "-", "%", ">", "<", "$", "@", "#", "&", "*", ",", ".", "!", ":", "º"]
        for punct in text:
            if punct in list_of_punctuation:
                text = text.replace(punct, '')
        text = re.sub(r"\d+", "", text)
        tokens = re.split(r"\s", text)
        for token in tokens:
            if token == '':
                tokens.remove(token)
        return tokens
    return None


def remove_stop_words(tokens: list, stop_words: list) -> list or None:
    """
    Removes stop words
    :param tokens: a list of tokens
    :param stop_words: a list of stop words
    :return: a list of tokens without stop words
    """
    if isinstance(tokens, list) and isinstance(stop_words, list):
        if tokens:
            for token in enumerate(tokens):
                if token[1] in stop_words:
                    tokens[token[0]] = ' '
            while ' ' in tokens:
                tokens.remove(' ')
            return tokens
        return None
    return None


def calculate_frequencies(tokens: list) -> dict or None:
    """
    Calculates frequencies of given tokens
    :param tokens: a list of tokens
    :return: a dictionary with frequencies
    """
    if isinstance(tokens, list):
        for token in tokens:
            if isinstance(token, str):
                freq_dict = {}
                for n in tokens:
                    if n in freq_dict:
                        freq_dict[n] += 1
                    else:
                        freq_dict[n] = 1
                return freq_dict
            return None
    return None


def get_top_n_words(freq_dict: dict, top_n: int) -> list or None:
    """
    Returns the most common words
    :param freq_dict: a dictionary with frequencies
    :param top_n: a number of the most common words
    :return: a list of the most common words
    """
    if isinstance(freq_dict, dict) and isinstance(top_n, int):
        sorted_dict = dict(sorted(freq_dict.items(), key = lambda x: x[1], reverse = True))
        freq_list = list(sorted_dict)
        return freq_list[:top_n]
    return None

def create_language_profile(language: str, text: str, stop_words: list) -> dict or None:
    """
    Creates a language profile
    :param language: a language
    :param text: a text
    :param stop_words: a list of stop words
    :return: a dictionary with three keys – name, freq, n_words
    """
    if isinstance(language, str) and isinstance(text, str) and isinstance(stop_words, list):
        tokens = tokenize(text)
        tokens = remove_stop_words(tokens, stop_words)
        freq_dict = calculate_frequencies(tokens)
        language_profile = {'name':language, 'freq':freq_dict, "n_words": len(freq_dict)}
        return language_profile
    return None

def compare_profiles(unknown_profile: dict, profile_to_compare: dict, top_n: int) -> float or None:
    """
    Compares profiles and calculates the distance using top n words
    :param unknown_profile: a dictionary
    :param profile_to_compare: a dictionary
    :param top_n: a number of the most common words
    :return: the distance
    """
    if isinstance(unknown_profile, dict) and isinstance(profile_to_compare, dict)\
            and isinstance(top_n, int):
        top_n_words_unk = get_top_n_words(unknown_profile['freq'], top_n)
        top_n_words_comp = get_top_n_words(profile_to_compare['freq'], top_n)
        common_elements = 0
        for element in top_n_words_unk:
            if element in top_n_words_comp:
                common_elements += 1
        freq_common = common_elements / len(top_n_words_unk)
        return round(freq_common, 2)
    return None




def detect_language(unknown_profile: dict, profile_1: dict, profile_2: dict, top_n: int) -> str or None:
    """
    Detects the language of an unknown profile
    :param unknown_profile: a dictionary
    :param profile_1: a dictionary
    :param profile_2: a dictionary
    :param top_n: a number of the most common words
    :return: a language
    """
    if isinstance(unknown_profile, dict) and isinstance(profile_1, dict)\
            and isinstance(profile_2, dict) and isinstance(top_n, int):
        freq_common1 = compare_profiles(unknown_profile, profile_1, top_n)
        freq_common2 = compare_profiles(unknown_profile, profile_2, top_n)
        if freq_common1 > freq_common2:
            return profile_1['name']
        if freq_common2 > freq_common1:
            return profile_2['name']
        if freq_common1 == freq_common2:
            languages_names = [profile_1['name'], profile_2['name']]
            languages_names.sort()
            return languages_names[0]
    return None
