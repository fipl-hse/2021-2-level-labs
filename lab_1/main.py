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
    symbols = """".,!?/'"-&@#№$%^<>;:*()[]{}|`1234567890"""
    text = text.lower()
    for symbol in symbols:
        text = text.replace(symbol, '')
    tokens = text.split()
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
    tokens = [token for token in tokens if token not in stop_words]
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
    for token in tokens:
        if not isinstance(token, str):
            return None
        if token in freq_dict:
            freq_dict[token] += 1
        else:
            freq_dict[token] = 1
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
    if not top_n > 0 or freq_dict == {}:
        return None
    for i in list(freq_dict.keys()):
        top_words = sorted(freq_dict, key=freq_dict.get, reverse=True) #по убыванию
        top_words = top_words[:top_n] #срез по листу
    return top_words


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
    lang_profile = {'name': language, 'freq': freq_dict, 'n_words': len(freq_dict)}
    return lang_profile


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
    top_of_unknown_profile = get_top_n_words(unknown_profile['frequency'], top_n)
    top_of_profile_to_compare = get_top_n_words(profile_to_compare['frequency'], top_n)
    shared_words = []
    for word in top_of_unknown_profile:
        if word in top_of_profile_to_compare:
            shared_words.append(word)
    distance = len(shared_words) / len(top_of_unknown_profile)
    distance = round(distance, 2)
    return distance


def detect_language(unknown_profile: dict, profile_1: dict, profile_2: dict, top_n: int) -> str or None:
    """
    Detects the language of an unknown profile
    :param unknown_profile: a dictionary
    :param profile_1: a dictionary
    :param profile_2: a dictionary
    :param top_n: a number of the most common words
    :return: a language
    """
    if not isinstance(unknown_profile, dict) or not isinstance(profile_1, dict) or not isinstance(profile_2, dict)or not isinstance(top_n, int):
        return None
    first_distance = compare_profiles(profile_1, unknown_profile, top_n) # -> int
    second_distance = compare_profiles(profile_2, unknown_profile, top_n) # -> int
    if first_distance > second_distance:
        language = profile_1['language name']
    elif second_distance > first_distance:
        language = profile_2['language name']
    return language