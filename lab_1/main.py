"""
Lab 1
Language detection
"""
import json


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
        if i == " " or i.isalpha():
            text_without_symbols += i
    good_text = text_without_symbols.lower()
    tokens = good_text.split()
    return tokens


def remove_stop_words(tokens: list, stop_words: list) -> list or None:
    """
    Removes stop words
    :param tokens: a list of tokens
    :param stop_words: a list of stop words
    :return: a list of tokens without stop words
    """
    if not isinstance(tokens, list):
        return None
    if not isinstance(stop_words, list):
        return None
    blank_list = []
    for i in tokens:
        if i not in stop_words:
            blank_list.append(i)
    tokens = blank_list
    return tokens


def calculate_frequencies(tokens: list) -> dict or None:
    """
    Calculates frequencies of given tokens
    :param tokens: a list of tokens
    :return: a dictionary with frequencies
    """
    if not isinstance(tokens, list):
        return None
    freq_dict = {}
    for i in tokens:
        if isinstance(i, str):
            some_dict = {i: tokens.count(i)}
            freq_dict.update(some_dict)
    return freq_dict or None


def get_top_n_words(freq_dict: dict, top_n: int) -> list or None:
    """
    Returns the most common words
    :param freq_dict: a dictionary with frequencies
    :param top_n: a number of the most common words
    :return: a list of the most common words
    """
    if not isinstance(freq_dict, dict):
        return None
    if not isinstance(top_n, int):
        return None
    inf = list(freq_dict.items())
    inf = sorted(inf, key=lambda x: x[1], reverse=True)
    popular_words = []
    for val, key in inf:
        popular_words.append(val)
    if len(popular_words) >= top_n:
        return popular_words[:top_n]
    elif len(popular_words) < top_n:
        return popular_words
    return popular_words


def create_language_profile(language: str, text: str, stop_words: list) -> dict or None:
    """
    Creates a language profile
    :param language: a language
    :param text: a text
    :param stop_words: a list of stop words
    :return: a dictionary with three keys – name, freq, n_words
    """
    if not isinstance(language, str):
        return None
    if not isinstance(text, str):
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
    if not isinstance(unknown_profile, dict):
        return None
    if not isinstance(profile_to_compare, dict):
        return None
    if not isinstance(top_n, int):
        return None
    top_unknown_profile = get_top_n_words(unknown_profile["freq"], top_n)
    top_profile_to_compare = get_top_n_words(profile_to_compare["freq"], top_n)
    top_common = []
    for i in top_unknown_profile:
        if i in top_profile_to_compare:
            top_common.append(i)
    frequence = round(len(top_common) / len(top_unknown_profile), 2)
    return frequence


def detect_language(unknown_profile: dict, profile_1: dict, profile_2: dict, top_n: int) -> str or None:
    """
    Detects the language of an unknown profile
    :param unknown_profile: a dictionary
    :param profile_1: a dictionary
    :param profile_2: a dictionary
    :param top_n: a number of the most common words
    :return: a language
    """
    if not isinstance(unknown_profile, dict):
        return None
    if not isinstance(profile_1, dict):
        return None
    if not isinstance(profile_2, dict):
        return None
    if not isinstance(top_n, int):
        return None
    compare_with_1 = compare_profiles(unknown_profile, profile_1, top_n)
    compare_with_2 = compare_profiles(unknown_profile, profile_2, top_n)
    lang = ""
    if compare_with_1 > compare_with_2:
        lang += profile_1["name"]
    elif compare_with_1 < compare_with_2:
        lang += profile_2["name"]
    elif compare_with_1 == compare_with_2:
        lang += [profile_1["name"], profile_2["name"]].sort()
    if isinstance(lang, list):
        language = lang[0]
    else:
        language = lang
    return language


def compare_profiles_advanced(unknown_profile: dict, profile_to_compare: dict, top_n: int) -> list or None:
    """
    Compares profiles and calculates some advanced parameters
    :param unknown_profile: a dictionary
    :param profile_to_compare: a dictionary
    :param top_n: a number of the most common words
    :return: a dictionary with 7 keys – name, score, common, sorted_common, max_length_word,
    min_length_word, average_token_length
    """
    if not isinstance(unknown_profile, dict):
        return None
    if not isinstance(profile_to_compare, dict):
        return None
    if not isinstance(top_n, int):
        return None

    name_of_profile = profile_to_compare["name"]

    popular_words = get_top_n_words(profile_to_compare["freq"], top_n)
    popular_words_un = get_top_n_words(unknown_profile["freq"], top_n)

    top_common = []
    for i in popular_words:
        if i in popular_words_un:
            top_common.append(i)

    score_value = len(top_common) / len(popular_words_un)

    new_keys = list((profile_to_compare["freq"]).keys())
    len_of_words_dict = {}
    for i in new_keys:
        len_of_word_un = len(i)
        len_of_words_dict[len_of_word_un] = i
    max_len = max(list(len_of_words_dict.keys()))
    min_len = min(list(len_of_words_dict.keys()))
    max_len_word = len_of_words_dict[max_len]
    min_len_word = len_of_words_dict[min_len]

    l_summary = 0
    number_of_words = 0
    for i in new_keys:
        number_of_words += 1
        l_summary += len(i)
    average_token_length_value = l_summary / number_of_words
    common_value_actual = top_common
    top_common.sort()
    advanced = dict(name=name_of_profile, common=common_value_actual, score=score_value, max_length_word=max_len_word,
                    min_length_word=min_len_word, average_token_length=average_token_length_value,
                    sorted_common=top_common)

    return advanced


def detect_language_advanced(unknown_profile: dict, profiles: list, languages: list, top_n: int) -> str or None:
    """
    Detects the language of an unknown profile within the list of possible languages
    :param unknown_profile: a dictionary
    :param profiles: a list of dictionaries
    :param languages: a list of possible languages
    :param top_n: a number of the most common words
    :return: a language
    """
    if not isinstance(unknown_profile, dict):
        return None
    if not isinstance(profiles, list):
        return None
    if not isinstance(languages, list):
        return None
    if not isinstance(top_n, int):
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
        exact_language = (results[0])["name"]
    else:
        return None
    return exact_language


def load_profile(path_to_file: str) -> dict or None:
    """
    Loads a language profile
    :param path_to_file: a path
    :return: a dictionary with three keys – name, freq, n_words
    """
    if type(path_to_file) != str:
        return None
    try:
        file = open(path_to_file)
        file.close()
    except:
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
    if not isinstance(profile, dict):
        return 1
    if "name" in profile.keys() is False:
        return 1
    if "freq" in profile.keys() is False:
        return 1
    if "n_words" in profile.keys() is False:
        return 1
    path = "{}.json".format(profile["name"])
    with open(path, "w", encoding="utf-8") as new_profile:
        json.dump(profile, new_profile)
    return 0
