"""
Lab 1
Language detection
"""


def tokenize(text: str) -> list or None:
    """
    Splits a text into tokens, converts the tokens into lowercase,
    removes punctuation and other symbols from words
    :param text: a text
    :return: a list of lower-cased tokens without punctuation
    """

    if not isinstance(text, str):
        return None
    tokens = ''
    for i in text:
        if i.isalpha() or i.isspace():
            tokens += i
    return tokens.lower().split()

def remove_stop_words(tokens: list, stop_words: list) -> list or None:
    """
    Removes stop words
    :param tokens: a list of tokens
    :param stop_words: a list of stop words
    :return: a list of tokens without stop words
    """

    if not isinstance(tokens, list) or not isinstance(stop_words, list):
        return None
    tokens_list = []
    for i in tokens:
        if isinstance(i, str) and i not in stop_words:
            tokens_list.append(i)
    return tokens_list

def calculate_frequencies(tokens: list) -> dict or None:
    """
    Calculates frequencies of given tokens
    :param tokens: a list of tokens
    :return: a dictionary with frequencies
    """

    if not isinstance(tokens, list):
        return None
    for i in tokens:
        if not isinstance(i, str):
            return None

    freq_dict = {}
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

    if not isinstance(freq_dict, dict) or not isinstance(top_n, int):
        return None

    freq_dict_sort = sorted(freq_dict.items(), key = lambda x: x[1], reverse=True)
    top_n_words = []
    values = []

    for key, value in freq_dict_sort:
        top_n_words.append(key)
        values.append(value)
    if len(top_n_words) >= top_n:
        top_n_words = top_n_words[:top_n]
    return top_n_words

def create_language_profile(language: str, text: str, stop_words: list) -> dict or None:
    """
    Creates a language profile
    :param language: a language
    :param text: a text
    :param stop_words: a list of stop words
    :return: a dictionary with three keys – name, freq, n_words
    """

    if not isinstance(language, str) or not isinstance(text, str) or not isinstance(stop_words, list):
        return None

    freq_dict = calculate_frequencies(remove_stop_words(tokenize(text), stop_words))
    language_profile = dict(name = language, freq = freq_dict, n_words = len(freq_dict))
    return language_profile

def compare_profiles(unknown_profile: dict, profile_to_compare: dict, top_n: int) -> float or None:
    """
    Compares profiles and calculates the distance using top n words
    :param unknown_profile: a dictionary
    :param profile_to_compare: a dictionary
    :param top_n: a number of the most common words
    :return: the distance
    """

    if not isinstance(unknown_profile, dict) or not isinstance(profile_to_compare, dict) or not isinstance(top_n, int):
        return None

    common_words = []
    top_unknown = get_top_n_words(unknown_profile["freq"], top_n)
    top_compare = get_top_n_words(profile_to_compare["freq"], top_n)
    for i in top_unknown:
        if i in top_compare:
            common_words.append(i)
    distance = round(len(common_words) / len(top_unknown), 2)
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

    if not isinstance(unknown_profile, dict) or not isinstance(profile_1, dict) or not isinstance(profile_2, dict) or not isinstance(top_n, int):
        return None
    first_compare = compare_profiles(unknown_profile, profile_1, top_n)
    second_compare = compare_profiles(unknown_profile, profile_2, top_n)
    language = ''
    if first_compare > second_compare:
        language += profile_1["name"]
    elif second_compare > first_compare:
        language += profile_2["name"]
    if first_compare == second_compare:
        language += sorted([profile_1["name"], profile_2["name"]])
    return language

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

    if not isinstance(unknown_profile, dict) or not isinstance(profile_to_compare, dict) or not isinstance(top_n, int):
        return None

    top_n_words_unknown = get_top_n_words(unknown_profile["freq"], top_n)
    top_n_words_compare = get_top_n_words(profile_to_compare["freq"], top_n)
    tokens = list(profile_to_compare["freq"].keys())

    top_n_words_common = []
    for i in top_n_words_compare:
        if i in top_n_words_unknown:
            top_n_words_common.append(i)

    score = len(top_n_words_common) / len(top_n_words_compare)
    word_length = 0
    for i in tokens:
        word_length += len(i)
    average_token_length = word_length / len(tokens)
    sorted_common = sorted(top_n_words_common)
    max_length_word = max(tokens, key=len)
    min_length_word = min(tokens, key=len)
    full_language_profile = dict(name=profile_to_compare["name"],
                                 common=top_n_words_common, score=score,
                                 max_length_word=max_length_word,
                                 min_length_word=min_length_word,
                                 average_token_length=average_token_length,
                                 sorted_common=sorted_common)
    return full_language_profile

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

    if not isinstance(unknown_profile, dict) or not isinstance(profiles, list) or not isinstance(languages, list) or not isinstance(top_n, int):
        return None

    available_profiles = []
    if len(languages) == 0:
        available_profiles = profiles
    for profile in profiles:
        if profile["name"] in languages:
            available_profiles.append(profile)

    lang_list = []
    for profile in available_profiles:
        lang_list.append(compare_profiles_advanced(unknown_profile, profile, top_n))

    lang_list = sorted(lang_list, key=lambda x: x["name"])
    lang_list = sorted(lang_list, key=lambda x: x["score"], reverse=True)
    if len(lang_list) >= 1:
        language = (lang_list[0])["name"]
    else:
        return None
    return language

def load_profile(path_to_file: str) -> dict or None:
    """
    Loads a language profile
    :param path_to_file: a path
    :return: a dictionary with three keys – name, freq, n_words
    """
    if not isinstance(path_to_file, str):
        return None
    return path_to_file

def save_profile(profile: dict) -> int:
    """
    Saves a language profile
    :param profile: a dictionary
    :return: 0 if everything is ok, 1 if not
    """
    if not isinstance(profile, dict):
        return None
    return profile
