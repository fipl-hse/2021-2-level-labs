"""Lab 1
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
    else:
        puncs = """'!@#$%^&*()-_=+/|"№;%:?><,.`~’…—[]{}1234567890\t"""
        for symbol in text:
            if symbol in puncs:
                text = text.replace(symbol, '')
        tokens = text.lower().split()
        return tokens
    pass


def remove_stop_words(tokens: list, stop_words: list) -> list or None:
    """
    Removes stop words
    :param tokens: a list of tokens
    :param stop_words: a list of stop words
    :return: a list of tokens without stop words
    """
    if not isinstance(tokens, list) or not tokens:
        return None
    else:
        tokens_copy = list(tokens)
        for token in tokens:
            if token in stop_words:
                tokens_copy.remove(token)
        return tokens_copy
    pass


def calculate_frequencies(tokens: list) -> dict or None:
    """
    Calculates frequencies of given tokens
    :param tokens: a list of tokens
    :return: a dictionary with frequencies
    """
    frequencies = {}
    if not isinstance(tokens, list):
        return None
    else:
        for token in tokens:
            if not isinstance(token, str):
                return None
            elif not token in frequencies.keys():
                frequencies[token] = 1
            else:
                frequency = frequencies.get(token)
                frequency += 1
                frequencies.update({token: frequency})
        return frequencies
    pass


def get_top_n_words(freq_dict: dict, top_n: int) -> list or None:
    """
    Returns the most common words
    :param freq_dict: a dictionary with frequencies
    :param top_n: a number of the most common words
    :return: a list of the most common words
    """
    if not isinstance(freq_dict, dict) or not isinstance(top_n, int):
        return None
    elif not freq_dict.keys() or top_n <= 0:
        return []
    else:
        top_words = []
        freq_words = sorted(freq_dict.items(), key=lambda x: x[1], reverse=True)
        for element in freq_words[:top_n]:
            top_words.append(element[0])
        return top_words
    pass


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
    else:
        freq_dict = calculate_frequencies(remove_stop_words(tokenize(text), stop_words))
        lang_profile = {'name': language,
                        'freq': freq_dict,
                        'n_words': len(freq_dict.keys())}
        return lang_profile
    pass


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
    else:
        unknown_top_words = get_top_n_words(unknown_profile.get('freq'), top_n)
        compare_top_words = get_top_n_words(profile_to_compare.get('freq'), top_n)
        shared_top_words = [word for word in unknown_top_words if word in compare_top_words]
        intersections_proportions = round(len(shared_top_words) / len(unknown_top_words), 2)
        return intersections_proportions
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
