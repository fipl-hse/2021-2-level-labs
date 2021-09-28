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
    pass
    if not isinstance(text, str):
        return None
    text = text.lower()
    text_tokenized = ''
    for symbol in text:
        if symbol.isalpha() or symbol.isspace():
            text_tokenized += symbol
    return text_tokenized.split()

def remove_stop_words(tokens: list, stop_words: list) -> list or None:
    """
    Removes stop words
    :param tokens: a list of tokens
    :param stop_words: a list of stop words
    :return: a list of tokens without stop words
    """
    pass
    if not isinstance(tokens, list) or not isinstance(stop_words, list):
        return None
    text_cleaned = []
    #[t for t in tokens if t not in stop_words]
    for t in tokens:
        if t not in stop_words:
            text_cleaned.append(t)
    return text_cleaned



def calculate_frequencies(tokens: list) -> dict or None:
    """
    Calculates frequencies of given tokens
    :param tokens: a list of tokens
    :return: a dictionary with frequencies
    """
    pass
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
    pass
    if not isinstance(freq_dict, dict) or not isinstance(top_n, int):
        return None
    sorted_dict = dict(sorted(freq_dict.items(), key=lambda x: -x[1]))
    return list(sorted_dict)[:top_n]

def create_language_profile(language: str, text: str, stop_words: list) -> dict or None:
    """
    Creates a language profile
    :param language: a language
    :param text: a text
    :param stop_words: a list of stop words
    :return: a dictionary with three keys – name, freq, n_words
    """
    pass
    if not isinstance(language, str) or not isinstance(text, str) or not isinstance(stop_words, list):
        return None
    text = tokenize(text)
    tokens = remove_stop_words(text, stop_words)
    freq_dict = calculate_frequencies(tokens)
    profile = {"name": language, "freq": freq_dict, "n_words": len(freq_dict)}
    return profile

def compare_profiles(unknown_profile: dict, profile_to_compare: dict, top_n: int) -> float or None:
    """
    Compares profiles and calculates the distance using top n words
    :param unknown_profile: a dictionary
    :param profile_to_compare: a dictionary
    :param top_n: a number of the most common words
    :return: the distance
    """
    pass
    if not isinstance(unknown_profile, dict) or not isinstance(profile_to_compare, dict) or not (top_n, int):
        return None
    top_unknown = get_top_n_words(unknown_profile["freq"], top_n)
    top_compare = get_top_n_words(profile_to_compare["freq"], top_n)
    shared_tokens = 0
    for w in top_compare:
        if w in top_unknown:
            shared_tokens += 1
    distance = round(shared_tokens/len(top_unknown), 2)
    return distance

def detect_language(unknown_profile: dict, profile_1: dict, profile_2: dict, top_n: int) -> str or None:
    """
    Detects the language of an unknown profile
    :param unknown_profile: a dictionary
    :param profile_1: a dictionary
    :param profile_2: a dictionary
    :return: a language
    """
    pass
    if not isinstance(unknown_profile, dict) or not isinstance(profile_1, dict) or not isinstance(profile_2, dict or not isinstance(top_n, int)):
        return None
    distance_1 = compare_profiles(unknown_profile, profile_1, top_n)
    distance_2 = compare_profiles(unknown_profile, profile_2, top_n)
    if distance_1 == distance_2:
        names = sorted([profile_1['name'], profile_2['name']])
        language = names[0]
    elif distance_1 > distance_2:
        language = profile_1['name']
    elif distance_1 < distance_2:
        language = profile_2['name']
    return language


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
