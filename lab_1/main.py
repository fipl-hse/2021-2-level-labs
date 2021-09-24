"""
Lab 1
Language detection
"""


def tokenize(text: str):
    """
    Splits a text into tokens, converts the tokens into lowercase,
    removes punctuation and other symbols from words
    :param text: a text
    :return: a list of lower-cased tokens without punctuation
    """
    pass

    import re

    if type(text) != str:
        return None
        text = text.lower()
        text = re.sub(r'[^a-zäöüß ]', '', str(text))
        tokens = text.split()

        return tokens


def remove_stop_words(tokens: list, stop_words: list):
    """
        Removes stop words
        :param tokens: a list of tokens
        :param stop_words: a list of stop words
        :return: a list of tokens without stop words
        """
    pass

    if type(tokens) != list:
        return None
    if type(stop_words) != list:
        return None
    for token in tokens:
        if token in stop_words:
            tokens.remove(token)
            return tokens


def calculate_frequencies(tokens: list):
    """
        Calculates frequencies of given tokens
        :param tokens: a list of tokens
        :return: a dictionary with frequencies
        """
    pass

    freq_dict = {}

    if type(tokens) != list:
        return None
    for i in tokens:
        if type(i) != str:
            return None
    for token in tokens:
        if token not in freq_dict:
            freq_dict[token] = 1
        else:
            freq_dict[token] += 1
    print(freq_dict)
    return freq_dict

def get_top_n_words(freq_dict: str, top_n: int):
    """
    Returns the most common words
    :param freq_dict: a dictionary with frequencies
    :param top_n: a number of the most common words
    :return: a list of the most common words
    """
    pass

    if type(freq_dict) != dict:
        return None
    if type(top_n) != int:
        return None

    freq_dict = list(freq_dict.items())

    freq_dict_sorted = sorted(freq_dict, key=lambda x: (-x[1], x[0]))
    print('Words sorted by frequency:', freq_dict_sorted)

    top_n = freq_dict_sorted[:5]

    for k, v in top_n:
        print('{}: {} time(s)'.format(k, v))
    return top_n


def create_language_profile(language: str, text: str, stop_words: list):
    """
    Creates a language profile
    :param language: a language
    :param text: a text
    :param stop_words: a list of stop words
    :return: a dictionary with three keys – name, freq, n_words
    """
    pass


def compare_profiles(unknown_profile: dict, profile_to_compare: dict, top_n: int):
    """
    Compares profiles and calculates the distance using top n words
    :param unknown_profile: a dictionary
    :param profile_to_compare: a dictionary
    :param top_n: a number of the most common words
    :return: the distance
    """
    pass


def detect_language(unknown_profile: dict, profile_1: dict, profile_2: dict, top_n: int):
    """
    Detects the language of an unknown profile
    :param unknown_profile: a dictionary
    :param profile_1: a dictionary
    :param profile_2: a dictionary
    :param top_n: a number of the most common words
    :return: a language
    """
    pass


def compare_profiles_advanced(unknown_profile: dict, profile_to_compare: dict, top_n: int):
    """
    Compares profiles and calculates some advanced parameters
    :param unknown_profile: a dictionary
    :param profile_to_compare: a dictionary
    :param top_n: a number of the most common words
    :return: a dictionary with 7 keys – name, score, common, sorted_common, max_length_word,
    min_length_word, average_token_length
    """
    pass


def detect_language_advanced(unknown_profile: dict, profiles: list, languages: list, top_n: int):
    """
    Detects the language of an unknown profile within the list of possible languages
    :param unknown_profile: a dictionary
    :param profiles: a list of dictionaries
    :param languages: a list of possible languages
    :param top_n: a number of the most common words
    :return: a language
    """
    pass


def load_profile(path_to_file: str):
    """
    Loads a language profile
    :param path_to_file: a path
    :return: a dictionary with three keys – name, freq, n_words
    """
    pass


def save_profile(profile: dict):
    """
    Saves a language profile
    :param profile: a dictionary
    :return: 0 if everything is ok, 1 if not
    """
    pass
