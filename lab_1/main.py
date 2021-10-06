"""
Lab 1
Language detection
"""

en_alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
               'u', 'v', 'w', 'x', 'y', 'z']
de_alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
               'u', 'v', 'w', 'x', 'y', 'z', 'ß', 'ö', 'ü', 'ä']
stop_words = ['the', 'a', 'is']


def tokenize(text):
    """
    Splits a text into tokens, converts the tokens into lowercase,
    removes punctuation and other symbols from words
    :param text: a text
    :return: a list of lower-cased tokens without punctuation
    """

    # Validate input
    if type(text) != str:
        return None

    result = []
    word = ''
    for char in text.lower():
        if char in de_alphabet:
            word = word + char
        elif char == ' ':
            if len(word) > 0:
                result.append(word)
                word = ''

    if len(word) > 0:
        result.append(word)

    if len(result) > 0:
        return result
    else:
        return None


def remove_stop_words(tokens, st_words):
    """
    Removes stop words
    :param tokens: a list of tokens
    :param st_words: a list of stop words
    :return: a list of tokens without stop words
    """

    # Check stop words
    st_word_valid = []
    if type(st_words) == list:
        for stop_word in st_words:
            if type(stop_word) == str:
                if stop_word in stop_words:
                    st_word_valid.append(stop_word)

    # Check tokens
    if type(tokens) != list or len(tokens) == 0:
        return None

    tokens_valid = []
    for word in tokens:
        if type(word) != str:
            return None

        if word not in st_word_valid:
            tokens_valid.append(word)

    return tokens_valid


def calculate_frequencies(tokens):
    """
    Calculates frequencies of given tokens
    :param tokens: a list of tokens
    :return: a dictionary with frequencies
    """

    # Check tokens validity
    if type(tokens) == list:
        for word in tokens:
            if type(word) != str:
                return None
    else:
        return None

    # Creation of dictionary [token, freq]
    token_dict = {}
    for key in tokens:
        key = key.lower()
        if key in token_dict:
            value = token_dict[key]
            token_dict[key] = value + 1
        else:
            token_dict[key] = 1

    return token_dict


def get_top_n_words(freq_dict, top_n):
    """
    Returns the most common words
    :param freq_dict: a dictionary with frequencies
    :param top_n: a number of the most common words
    :return: a list of the most common words
    """
    if not isinstance(freq_dict, dict):
        return None

    top_list = []
    if top_n > 0:
        ind = 0
        for i in sorted(freq_dict.items(), reverse=True, key=lambda pair: pair[1]):
            top_list.append(i[0])
            ind = ind + 1
            if ind == top_n:
                return top_list

    return top_list

'''
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
'''