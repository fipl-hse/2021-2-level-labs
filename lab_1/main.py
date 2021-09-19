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
    # Check for bad input
    if not isinstance(text, str):
        return None

    # Remove non-alphabetic characters
    text = ''.join([i for i in text if i.isalpha() or i.isspace()])

    # Convert to lowercase and split into tokens
    text = text.lower()
    text = text.split()
    return text


def remove_stop_words(tokens: list, stop_words: list) -> list or None:
    """
    Removes stop words
    :param tokens: a list of tokens
    :param stop_words: a list of stop words
    :return: a list of tokens without stop words
    """
    # Check for bad input
    if not isinstance(tokens, list):
        return None
    if not len(tokens):
        return None
    if not isinstance(stop_words, list):
        return tokens

    # Remove stop words from tokens
    tokens = [token for token in tokens if token not in stop_words]
    return tokens


def calculate_frequencies(tokens: list) -> dict or None:
    """
    Calculates frequencies of given tokens
    :param tokens: a list of tokens
    :return: a dictionary with frequencies
    """
    # Check for bad input
    if not isinstance(tokens, list):
        return None

    # Record the frequency of tokens in a dictionary
    frequencies = {}
    for token in tokens:
        # Check for bad list contents
        if not isinstance(token, str):
            return None
        
        if token not in frequencies:
            frequencies[token] = 0
        frequencies[token] += 1
    return frequencies


def get_top_n_words(freq_dict: dict, top_n: int) -> list or None:
    """
    Returns the most common words
    :param freq_dict: a dictionary with frequencies
    :param top_n: a number of the most common words
    :return: a list of the most common words
    """
    # Check for bad input
    if (not isinstance(freq_dict, dict)
            or not isinstance(top_n, int)):
        return None
    # Convert frequency dictionary to list of tuples
    tokens = freq_dict.items()
    # Sort list by frequency
    tokens = sorted(tokens, key=lambda x: x[1], reverse=True)
    # Drop frequency data
    tokens = [token for token, freq in tokens]
    # Only include the first N elements
    tokens = tokens[:top_n]
    return tokens


def create_language_profile(language: str,
                            text: str,
                            stop_words: list) -> dict or None:
    """
    Creates a language profile
    :param language: a language
    :param text: a text
    :param stop_words: a list of stop words
    :return: a dictionary with three keys – name, freq, n_words
    """
    # Check for bad input
    if (not isinstance(language, str)
            or not isinstance(text, str)
            or not isinstance(stop_words, list)):
        return None
    # Get frequencies
    tokens = tokenize(text)
    tokens = remove_stop_words(tokens, stop_words)
    frequencies = calculate_frequencies(tokens)
    # Get n_words
    n_words = len(frequencies.keys())
    # Assemble language profile
    profile = {"name": language, "freq": frequencies, "n_words": n_words}
    return profile


def compare_profiles(unknown_profile: dict,
                     profile_to_compare: dict,
                     top_n: int) -> float or None:
    """
    Compares profiles and calculates the distance using top n words
    :param unknown_profile: a dictionary
    :param profile_to_compare: a dictionary
    :param top_n: a number of the most common words
    :return: the distance
    """
    # Check for bad input
    if (not isinstance(unknown_profile, dict)
            or not isinstance(profile_to_compare, dict)
            or not isinstance(top_n, int)):
        return None
    # Get sets of top N tokens of given profiles
    compare_top = set(get_top_n_words(profile_to_compare["freq"], top_n))
    unknown_top = set(get_top_n_words(unknown_profile["freq"], top_n))
    # Find set of shared tokens
    shared = compare_top.intersection(unknown_top)
    # Find distance between profiles
    distance = round(len(shared) / len(unknown_top), 2)
    return distance


def detect_language(unknown_profile: dict,
                    profile_1: dict,
                    profile_2: dict,
                    top_n: int) -> str or None:
    """
    Detects the language of an unknown profile
    :param unknown_profile: a dictionary
    :param profile_1: a dictionary
    :param profile_2: a dictionary
    :param top_n: a number of the most common words
    :return: a language
    """
    # Check for bad input
    if (not isinstance(unknown_profile, dict)
            or not isinstance(profile_1, dict)
            or not isinstance(profile_2, dict)
            or not isinstance(top_n, int)):
        return None
    distance_1 = compare_profiles(unknown_profile, profile_1, top_n)
    distance_2 = compare_profiles(unknown_profile, profile_2, top_n)
    if distance_1 == distance_2:
        first_name_alphabetically = min(profile_1["name"], profile_2["name"])
        return first_name_alphabetically
    elif distance_1 > distance_2:
        return profile_1["name"]
    else:
        return profile_2["name"]


def compare_profiles_advanced(unknown_profile: dict,
                              profile_to_compare: dict,
                              top_n: int) -> list or None:
    """
    Compares profiles and calculates some advanced parameters
    :param unknown_profile: a dictionary
    :param profile_to_compare: a dictionary
    :param top_n: a number of the most common words
    :return: a dictionary with 7 keys – name, score, common, sorted_common, max_length_word,
    min_length_word, average_token_length
    """
    pass


def detect_language_advanced(unknown_profile: dict,
                             profiles: list,
                             languages: list,
                             top_n: int) -> str or None:
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
