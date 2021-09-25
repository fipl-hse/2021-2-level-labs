#coding=utf-8
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
    if type(text) != str:
        return None
    text = text.lower()
    preprocessed = ''
    for i in range(len(text)):
        if text[i].isalnum() or text[i] == ' ':
            preprocessed += text[i]
    tokens = preprocessed.split()
    return tokens



def remove_stop_words(tokens: list, stop_words: list) -> list or None:
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
    tokens = [token for token in tokens if token not in stop_words]
    return tokens


def calculate_frequencies(tokens: list) -> dict or None:
    """
        Calculates frequencies of given tokens
        :param tokens: a list of tokens
        :return: a dictionary with frequencies
        """
    pass
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


def get_top_n_words(freq_dict: dict, top_n: int) -> list or None:
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
    freq_dict_sort = sorted(freq_dict, key=lambda i: -i[1])
    if len(freq_dict_sort) == 0:
        return []
    new_freq_list = []
    for t in freq_dict_sort:
        new_freq_list.append(t[0])
        top_words = new_freq_list[:top_n]
    print (top_words)
    return top_words


def create_language_profile(language: str, text: str, stop_words: list) -> dict or None:
    """
        Creates a language profile
        :param language: a language
        :param text: a text
        :param stop_words: a list of stop words
        :return: a dictionary with three keys – name, freq, n_words
        """
    pass
    if type(language) != str:
        return None
    if type(text) != str:
        return None
    if len(text) == 0:
        return None
    if type(stop_words) != list:
        return None
    profile = {}
    profile['name'] = language
    freq = calculate_frequencies(remove_stop_words(tokenize(text),stop_words))
    profile['freq'] = freq
    n_words = len(freq)
    profile['n_words'] = n_words

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
    if type(unknown_profile) != dict:
        return None
    if type(profile_to_compare) != dict:
        return None
    if type(top_n) != int:
        return None
    count = 0
    top_n_words_profile_to_compare = get_top_n_words(profile_to_compare['freq'],top_n)
    top_n_words_unknown_profile = get_top_n_words(unknown_profile['freq'], top_n)
    len_top_n_words_unknown_profile = len(unknown_profile['freq'])
    if top_n_words_profile_to_compare == top_n_words_unknown_profile:
        return float(1)
    else:
        for word_profile_to_compare in top_n_words_profile_to_compare:
            for word_unknown_profile in top_n_words_unknown_profile:
                if word_profile_to_compare == word_unknown_profile:
                    count += 1
        share_of_common_frequency_words = round(float(count / len_top_n_words_unknown_profile),2)
        return share_of_common_frequency_words


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
