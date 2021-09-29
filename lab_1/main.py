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

    alphabet = 'abcdefghijklmnopqrstuvwxyzäöüßāīūēō'

    if type(text) != str:
        return None
    if text == '':
        return None

    text = text.lower()
    tokens = text.split()
    new_tokens = []

    for i in tokens:
        temp = str(i)
        for j in temp:
            if j not in alphabet:
                temp = temp.replace(j, '')
        new_tokens.append(temp)

    while '' in new_tokens:
        new_tokens.remove('')

    if new_tokens != []:
        return new_tokens
    else:
        return None

def remove_stop_words(tokens: list, stop_words: list) -> list or None:
    """
    Removes stop words
    :param tokens: a list of tokens
    :param stop_words: a list of stop words
    :return: a list of tokens without stop words
    """

    if type(tokens) != list:
        return None
    if tokens == []:
        return None
    if type(stop_words) != list:
        return tokens

    for i in stop_words:
        while i in tokens:
            tokens.remove(i)

    return tokens

def calculate_frequencies(tokens: list) -> dict or None:
    """
    Calculates frequencies of given tokens
    :param tokens: a list of tokens
    :return: a dictionary with frequencies
    """

    if type(tokens) != list:
        return None
    if tokens == [None]:
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

    if type(freq_dict) != dict:
        return None
    if freq_dict == {}:
        return []
    if top_n <= 0:
        return []

    top_n_freqs = freq_dict.values()
    top_n_freqs = sorted(top_n_freqs, reverse=True)
    top_n_words = []

    for i in range(len(top_n_freqs)):
        for key in freq_dict:
            if freq_dict[key] == top_n_freqs[i]:
                    top_n_words.append(key)

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

    if type(language) != str:
        return None
    if type(text) != str:
        return None
    if (not stop_words) and (stop_words != []):
        return None

    lang_profile = {'name':'', 'freq':{}, 'n_words':0}

    tokens = tokenize(text)
    tokens = remove_stop_words(tokens, stop_words)

    lang_profile['name'] = language
    lang_profile['freq'] = calculate_frequencies(tokens)
    lang_profile['n_words'] = len(lang_profile['freq'].keys())

    return lang_profile


def compare_profiles(unknown_profile: dict, profile_to_compare: dict, top_n: int) -> float or None:
    """
    Compares profiles and calculates the distance using top n words
    :param unknown_profile: a dictionary
    :param profile_to_compare: a dictionary
    :param top_n: a number of the most common words
    :return: the distance
    """

    if not unknown_profile or not profile_to_compare:
        return None
    if type(top_n) != int:
        return None

    same_tokens = 0
    proportion = float()

    top1 = get_top_n_words(unknown_profile['freq'], top_n)
    top2 = get_top_n_words(profile_to_compare['freq'], top_n)

    for i in top1:
        for j in top2:
            if i == j:
                same_tokens += 1

    proportion = round(same_tokens / top_n, 2)

    return proportion


def detect_language(unknown_profile: dict, profile_1: dict, profile_2: dict, top_n: int) -> str or None:
    """
    Detects the language of an unknown profile
    :param unknown_profile: a dictionary
    :param profile_1: a dictionary
    :param profile_2: a dictionary
    :param top_n: a number of the most common words
    :return: a language
    """

    if type(unknown_profile) != dict:
        return None
    if type(profile_1) != dict:
        return None
    if type(profile_2) != dict:
        return None
    if type(top_n) != int:
        return None

    prop01 = compare_profiles(unknown_profile, profile_1, top_n)
    prop02 = compare_profiles(unknown_profile, profile_2, top_n)

    if prop01 > prop02:
        unknown_profile['name'] = profile_1['name']
    else:
        unknown_profile['name'] = profile_2['name']

    return unknown_profile['name']


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
