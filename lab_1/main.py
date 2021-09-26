"""
Lab 1
Language detection
"""
import re
import json
import os.path


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
    text = re.split(r"[^\w\s]", text)
    text = "".join(text)
    tokens = re.findall(r"\w+", text)
    return tokens


def remove_stop_words(tokens: list, stop_words: list) -> list or None:
    """
    Removes stop words
    :param tokens: a list of tokens
    :param stop_words: a list of stop words
    :return: a list of tokens without stop words
    """

    tokens_n = []
    if not isinstance(stop_words, list) or not isinstance(tokens, list):
        return None
    for token in tokens:
        if token not in stop_words:
            tokens_n.append(token)
    return tokens_n


def calculate_frequencies(tokens: list) -> dict or None:
    """
    Calculates frequencies of given tokens
    :param tokens: a list of tokens
    :return: a dictionary with frequencies
    """

    freq_dict = {}
    if not isinstance(tokens, list):
        return None
    for i in tokens:
        if not isinstance(i, str):
            return None

    for i in tokens:
        if i in freq_dict:
            freq_dict[i] += 1
        else:
            freq_dict[i] = 1
    return freq_dict


def get_top_n_words(freq_dict: dict, top_n: int) -> list or None:
    """
    Returns the most common words
    :param freq_dict: a dictionary with frequencies
    :param top_n: a number of the most common words
    :return: a list of the most common words
    """

    if not isinstance(freq_dict, dict):
        return None
    freq_dict = sorted(freq_dict.items(), key=lambda x: -x[1])
    if len(freq_dict) == 0:
        return []
    freq_n = []
    for word in freq_dict:
        freq_n.append(word[0])
    return list(freq_n[:top_n])


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
    tokens = tokenize(text)
    cleaned_tokens = remove_stop_words(tokens, stop_words)
    freq_dict = calculate_frequencies(cleaned_tokens)
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

    if isinstance(unknown_profile, dict) and isinstance(profile_to_compare, dict):
        if isinstance(top_n, int):
            freq_dict_2 = unknown_profile['freq']  # new
            get_top_n_words_2 = get_top_n_words(freq_dict_2, top_n)  # new
            new_freq_dict_3 = profile_to_compare['freq']  # new
            new_get_top_n_words_3 = get_top_n_words(new_freq_dict_3, top_n)  # new
            common_words = 0
            for word in get_top_n_words_2:
                if word in new_get_top_n_words_3:
                    common_words += 1
            proportion = round(common_words / top_n, 2)
            return proportion
    return None


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

    if isinstance(unknown_profile, dict) and isinstance(profile_1, dict):
        if isinstance(profile_2, dict) and isinstance(top_n, int):
            comparison = compare_profiles(unknown_profile, profile_1, top_n)  # proportion_2
            comparison_2 = compare_profiles(unknown_profile, profile_2, top_n)  # proportion_3
            if comparison > comparison_2:
                return profile_1['name']
            if comparison_2 > comparison:
                return profile_2['name']
            return max(profile_1['name'], profile_2['name'])
    return None


def compare_profiles_advanced(unknown_profile: dict,
                              profile_to_compare: dict, top_n: int) -> list or None:
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
    top_n_words_2 = get_top_n_words(unknown_profile['freq'], top_n)  # unknown text

    top_n_common = []
    for i in top_n_words:
        if i in top_n_words_2:
            top_n_common.append(i)
    score = len(top_n_common) / len(top_n_words_2)
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

    if not isinstance(unknown_profile, dict) or not isinstance(profiles, list):
        return None
    if not isinstance(languages, list) or not isinstance(top_n, int):
        return None
    dict_scores = {}
    for profile in profiles:
        if len(languages) == 0 or profile['name'] in languages:
            profile_3 = compare_profiles_advanced(unknown_profile, profile, top_n)
            score = profile_3['score']
            dict_scores[profile['name']] = score
    sorted_dict_scores = sorted(dict_scores.items(), key=lambda x: x[1])
    if len(sorted_dict_scores) == 0:
        return None
    common_profiles = []
    highest_score = sorted_dict_scores[len(sorted_dict_scores) - 1][1]
    for language in sorted_dict_scores:
        if language[1] >= highest_score:
            common_profiles.append(language[0])

    common_profiles.sort()
    return common_profiles[0]


def load_profile(path_to_file: str) -> dict or None:
    """
    Loads a language profile
    :param path_to_file: a path
    :return: a dictionary with three keys – name, freq, n_words
    """

    if isinstance(path_to_file, str):
        if os.path.exists(path_to_file):
            with open(path_to_file, 'r', encoding='UTF-8') as file:
                profile = json.load(file)
                return profile
    return None


def save_profile(profile: dict) -> int:
    """
    Saves a language profile
    :param profile: a dictionary
    :return: 0 if everything is ok, 1 if not
    """

    if not isinstance(profile, dict):
        return 1
    profile_dict = '{}.json'.format(profile['name'])
    with open(profile_dict, 'w', encoding='UTF-8') as file:
        json.dump(profile, file)
        return 0
