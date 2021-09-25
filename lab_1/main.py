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
    if type(text) == str:
        text = text.lower()
        for symbol in text:
            if symbol.isalpha() == False:
                text = text.replace(symbol, ' ')
        tokens = text.split()
        for word in tokens:
            word = word.strip()
        return tokens


def remove_stop_words(tokens: list, stop_words: list) -> list or None:
    """
    Removes stop words
    :param tokens: a list of tokens
    :param stop_words: a list of stop words
    :return: a list of tokens without stop words
    """
    for word in tokens:
        if word in stop_words:
            tokens.remove(word)
    return tokens
    pass


def calculate_frequencies(tokens: list) -> dict or None:
    """
    Calculates frequencies of given tokens
    :param tokens: a list of tokens
    :return: a dictionary with frequencies
    """
    t_dict = {}
    for word in tokens:
        if word in t_dict.keys():
            t_dict[word] += 1
        else:
            t_dict[word] = 1
    return t_dict
    pass


def get_top_n_words(freq_dict: dict, top_n: int) -> list or None:
    """
    Returns the most common words
    :param freq_dict: a dictionary with frequencies
    :param top_n: a number of the most common words
    :return: a list of the most common words
    """
    top = []
    if top_n > len(freq_dict):
        top_n = len(freq_dict)
    freq_dict = sorted(freq_dict.items(), key=lambda x: (-x[1], x[0]))
    for i in range(top_n):
        top.append(freq_dict[i][0])
    return top
    pass


def create_language_profile(language: str, text: str, stop_words: list) -> dict or None:
    """
    Creates a language profile
    :param language: a language
    :param text: a text
    :param stop_words: a list of stop words
    :return: a dictionary with three keys – name, freq, n_words
    """
    l_profile = {}
    l_profile['name'] = language
    l_profile['freq'] = calculate_frequencies(remove_stop_words(tokenize(text), stop_words))
    l_profile['n_words'] = len(l_profile['freq'])
    return l_profile
    pass


def calculate_distance(profile_1: dict, profile_2: dict, top_n: int) -> float or None:
    """
    Calculates the distance using top n words
    :param profile_1: a dictionary
    :param profile_2: a dictionary
    :param top_n: a number of the most common words
    :return: a proportion
    """
    match = 0
    for word in get_top_n_words(profile_1['freq'], top_n):
        if word in get_top_n_words(profile_2['freq'], top_n):
            match += 1
    return round(match / top_n, 3)
    pass


def detect_language(unknown_profile: dict, profile_1: dict, profile_2: dict, top_n: int) -> str or None:
    """
    Detects the language of an unknown profile
    :param unknown_profile: a dictionary
    :param profile_1: a dictionary
    :param profile_2: a dictionary
    :return: a language
    """
    detect_dict = {}
    detect_dict[calculate_distance(profile_1, unknown_profile, top_n)] = profile_1['name']
    detect_dict[calculate_distance(profile_2, unknown_profile, top_n)] = profile_2['name']
    return detect_dict[max(detect_dict.keys())]
    pass


def detect_language_advanced(unknown_profile: dict, profiles: list, languages: list) -> str or None:
    """
    Detects the language of an unknown profile within the list of possible languages
    :param unknown_profile: a dictionary
    :param profiles: a list of dictionaries
    :param languages: a list of possible languages
    :return: a language
    """
    pass


def create_report(unknown_profile: dict, profiles: list, languages: list) -> list or None:
    """
    Creates a report on language detection
    :param unknown_profile: a dictionary
    :param profiles: a list of dictionaries
    :param languages: a list of possible languages
    :return: a list of dictionaries with two keys – name, score
    """
    pass


def load_profile(path_to_file: str) -> dict or None:
    """
    Loads a language profile
    :param path_to_file: a path
    :return: a dictionary with three keys – name, freq, n_words
    """
    pass


def save_profile(profile: dict) -> int:
    """
    Saves a language profile
    :param profile: a dictionary
    :return: 0 if everything is ok, 1 if not
    """
    pass
