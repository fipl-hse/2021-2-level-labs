#coding=utf-8
"""
Lab 1
Language detection
"""


def tokenize(text: str) -> list or None:
    if type(text) != str:
        return None
    text = text.lower()
    preprocessed = ''
    for i in range(len(text)):
        if text[i].isalnum() or text[i] == ' ':
            preprocessed += text[i]
    tokens = preprocessed.split()
    return tokens
    """
    Splits a text into tokens, converts the tokens into lowercase,
    removes punctuation and other symbols from words
    :param text: a text
    :return: a list of lower-cased tokens without punctuation
    """
    pass


def remove_stop_words(tokens: list, stop_words: list) -> list or None:
    if type(tokens) != list:
            return None
    if type(stop_words) != list:
            return None
    tokens = [token for token in tokens if token not in stop_words]
    return tokens
stop_words = ['a','the','is','ein','eine','den','die','das','der']
    """
    Removes stop words
    :param tokens: a list of tokens
    :param stop_words: a list of stop words
    :return: a list of tokens without stop words
    """
    pass

def calculate_frequencies(tokens: list) -> dict or None:
    if type(tokens) != list:
        return None
    for x in tokens:
        if type(x) != str:
            return None
    freq_dict = {}
    for token in tokens:
        if token in freq_dict:
            freq_dict[token] += 1
        else:
            freq_dict[token] = 1
    print (freq_dict)
    return freq_dict
    """
    Calculates frequencies of given tokens
    :param tokens: a list of tokens
    :return: a dictionary with frequencies
    """
    pass

def get_top_n_words(freq_dict: dict, top_n: int) -> list or None:
    if type(freq_dict) != dict:
        return None
    freq_dict = list(freq_dict.items())
    freq_sort = sorted(freq_dict, key=lambda i: -i[1])
    top_words = freq_sort[:top_n]
    print (top_words)
    return top_words

#get_top_n_words(calculate_frequencies(remove_stop_words(tokenize(text),stop_words)),5)
    """
    Returns the most common words
    :param freq_dict: a dictionary with frequencies
    :param top_n: a number of the most common words
    :return: a list of the most common words
    """
    pass


def create_language_profile(language: str, text: str, stop_words: list) -> dict or None:
    """
    Creates a language profile
    :param language: a language
    :param text: a text
    :param stop_words: a list of stop words
    :return: a dictionary with three keys – name, freq, n_words
    """
    pass


def compare_profiles(unknown_profile: dict, profile_to_compare: dict, top_n: int) -> float or None:
    """
    Compares profiles and calculates the distance using top n words
    :param unknown_profile: a dictionary
    :param profile_to_compare: a dictionary
    :param top_n: a number of the most common words
    :return: the distance
    """
    pass


def detect_language(unknown_profile: dict, profile_1: dict, profile_2: dict, top_n: int) -> str or None:
    """
    Detects the language of an unknown profile
    :param unknown_profile: a dictionary
    :param profile_1: a dictionary
    :param profile_2: a dictionary
    :param top_n: a number of the most common words
    :return: a language
    """
    pass


def compare_profiles_advanced(unknown_profile: dict, profile_to_compare: dict, top_n: int) -> list or None:
    """
    Compares profiles and calculates some advanced parameters
    :param unknown_profile: a dictionary
    :param profile_to_compare: a dictionary
    :param top_n: a number of the most common words
    :return: a dictionary with 7 keys – name, score, common, sorted_common, max_length_word,
    min_length_word, average_token_length
    """
    pass


def detect_language_advanced(unknown_profile: dict, profiles: list, languages: list, top_n: int) -> str or None:
    """
    Detects the language of an unknown profile within the list of possible languages
    :param unknown_profile: a dictionary
    :param profiles: a list of dictionaries
    :param languages: a list of possible languages
    :param top_n: a number of the most common words
    :return: a language
    """
    pass


def load_profile(path_to_file: str) -> dict or None:
    """
    Loads a language profile
    :param path_to_file: a path
    :return: a dictionary with three keys – name, freq, n_words
    """
    pass


def save_profile(profile: dict) -> int:
    """
    Saves a language profile
    :param profile: a dictionary
    :return: 0 if everything is ok, 1 if not
    """
    pass
