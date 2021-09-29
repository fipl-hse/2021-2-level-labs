"""
Lab 1
Language detection
"""
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
    text_without_symbols = ""
    for i in text:
        if i.isspace() or i.isalpha():
            text_without_symbols += i
    tokens = text_without_symbols.lower().split()
    return tokens


def remove_stop_words(tokens: list, stop_words: list) -> list or None:
    """
    Removes stop words
    :param tokens: a list of tokens
    :param stop_words: a list of stop words
    :return: a list of tokens without stop words
    """
    if not isinstance(tokens, list) or \
            not isinstance(stop_words, list):
        return None
    blank_list = []
    for i in tokens:
        if i not in stop_words:
            blank_list.append(i)
    return blank_list


def calculate_frequencies(blank_list: list) -> dict or None:
    """
    Calculates frequencies of given tokens
    :param blank_list: a list of tokens
    :return: a dictionary with frequencies
    """
    if not isinstance(blank_list, list):
        return None
    freq_dict = {}
    for i in blank_list:
        if isinstance(i, str):
            freq_dict.update({i: blank_list.count(i)})
    if freq_dict == {}:
        return None
    return freq_dict


def get_top_n_words(freq_dict: dict, top_n: int) -> list or None:
    """
    Returns the most common words
    :param freq_dict: a dictionary with frequencies
    :param top_n: a number of the most common words
    :return: a list of the most common words
    """
    if not isinstance(freq_dict, dict) or \
            not isinstance(top_n, int):
        return None
    popular_words = sorted(freq_dict, key=freq_dict.get, reverse=True)
    if len(popular_words) >= top_n:
        popular_words = popular_words[:top_n]
    return popular_words


def create_language_profile(language: str, text: str, stop_words: list) -> dict or None:
    """
    Creates a language profile
    :param language: a language
    :param text: a text
    :param stop_words: a list of stop words
    :return: a dictionary with three keys – name, freq, n_words
    """
    if not isinstance(language, str) or \
            not isinstance(text, str) or \
            not isinstance(stop_words, list):
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
    if not isinstance(unknown_profile, dict) or \
            not isinstance(profile_to_compare, dict) or \
            not isinstance(top_n, int):
        return None
    top_unknown_profile = get_top_n_words(unknown_profile["freq"], top_n)
    top_profile_to_compare = get_top_n_words(profile_to_compare["freq"], top_n)
    top_common = []
    for i in top_unknown_profile:
        if i in top_profile_to_compare:
            top_common.append(i)
    frequence = round(len(top_common) / len(top_unknown_profile), 2)
    return frequence


def detect_language(unknown_profile: dict, profile_1: dict, profile_2: dict, top_n: int) \
        -> str or None:

    """
    Detects the language of an unknown profile
    :param unknown_profile: a dictionary
    :param profile_1: a dictionary
    :param profile_2: a dictionary
    :param top_n: a number of the most common words
    :return: a language
    """
    if not isinstance(unknown_profile, dict) or \
            not isinstance(profile_1, dict) or \
            not isinstance(profile_2, dict) or \
            not isinstance(top_n, int):
        return None
    compare_with_1 = compare_profiles(unknown_profile, profile_1, top_n)
    compare_with_2 = compare_profiles(unknown_profile, profile_2, top_n)
    lang = []
    if compare_with_1 > compare_with_2:
        lang.append(profile_1["name"])
    elif compare_with_1 < compare_with_2:
        lang.append(profile_2["name"])
    elif compare_with_1 == compare_with_2:
        lang.append(profile_1["name"], profile_2["name"]).sort()
    return lang[0]


def compare_profiles_advanced(unknown_profile: dict, profile_to_compare: dict, top_n: int) \
        -> list or None:
    """
    Compares profiles and calculates some advanced parameters
    :param unknown_profile: a dictionary
    :param profile_to_compare: a dictionary
    :param top_n: a number of the most common words
    :return: a dictionary with 7 keys – name, score, common, sorted_common, max_length_word,
    min_length_word, average_token_length
    """
    if not isinstance(unknown_profile, dict) or \
            not isinstance(profile_to_compare, dict) or \
            not isinstance(top_n, int):
        return None

    popular_words = get_top_n_words(profile_to_compare["freq"], top_n)
    popular_words_un = get_top_n_words(unknown_profile["freq"], top_n)

    top_common = []
    for i in popular_words:
        if i in popular_words_un:
            top_common.append(i)

    score = len(top_common) / len(popular_words_un)

    new_keys = list((profile_to_compare["freq"]).keys())
    len_of_words_dict = {}
    for i in new_keys:
        len_of_words_dict[i] = len(i)
    len_of_words_dict_val = list(len_of_words_dict.values())
    max_len_word = \
        list(len_of_words_dict.keys())[len_of_words_dict_val.index(max(len_of_words_dict_val))]
    min_len_word = \
        list(len_of_words_dict.keys())[len_of_words_dict_val.index(min(len_of_words_dict_val))]

    l_summary = []
    for i in new_keys:
        l_summary.append(len(i))
    advanced = dict(name=profile_to_compare["name"], common=top_common,
                    score=score, max_length_word=max_len_word,
                    min_length_word=min_len_word,
                    average_token_length=sum(l_summary) / len(l_summary),
                    sorted_common=sorted(top_common))

    return advanced


def detect_language_advanced(unknown_profile: dict, profiles: list, languages: list, top_n: int) \
        -> str or None:
    """
    Detects the language of an unknown profile within the list of possible languages
    :param unknown_profile: a dictionary
    :param profiles: a list of dictionaries
    :param languages: a list of possible languages
    :param top_n: a number of the most common words
    :return: a language
    """
    if not isinstance(unknown_profile, dict) or \
            not isinstance(profiles, list) or \
            not isinstance(languages, list) or \
            not isinstance(top_n, int):
        return None

    actual_profiles = []
    if len(languages) == 0:
        actual_profiles = profiles
    for i in profiles:
        if i["name"] in languages:
            actual_profiles.append(i)

    results = []
    for profile in actual_profiles:
        results.append(compare_profiles_advanced(unknown_profile, profile, top_n))

    results = sorted(results, key=lambda x: x["name"])
    results = sorted(results, key=lambda x: x["score"], reverse=True)
    if len(results) >= 1:
        exact_language = results[0]["name"]
    else:
        return None
    return exact_language


def load_profile(path_to_file: str) -> dict or None:
    """
    Loads a language profile
    :param path_to_file: a path
    :return: a dictionary with three keys – name, freq, n_words
    """
    if not isinstance(path_to_file, str) or \
        os.path.exists(path_to_file) == False:
        return None
    with open(path_to_file, "r", encoding="utf-8") as json_file:
        imported_profile = json.load(json_file)
    return imported_profile


def save_profile(profile: dict) -> int:
    """
    Saves a language profile
    :param profile: a dictionary
    :return: 0 if everything is ok, 1 if not
    """
    if not isinstance(profile, dict) or \
        "name" not in profile.keys() or \
        "freq" not in profile.keys() or \
        "n_words" not in profile.keys():
        return 1
    path = "{}.json".format(profile["name"])
    with open(path, "w", encoding="utf-8") as new_profile:
        json.dump(profile, new_profile)
    return 0
