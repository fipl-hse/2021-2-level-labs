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
    if type(text) != str:
        return None
    text = text.lower()
    marks = '''1234567890!()-§[]{};?@#$%:'"/\\.,^&*_<>№'''
    for i in text:
        if i in marks:
            text = text.replace(i, '')
    tokens = text.split()
    return tokens


def remove_stop_words(tokens: list, stop_words: list) -> list or None:
    """
    Removes stop words
    :param tokens: a list of tokens
    :param stop_words: a list of stop words
    :return: a list of tokens without stop words
    """
    tokens_right = []
    if type(tokens) != list or None in tokens:
        return None
    if type(stop_words) != list:
        return None
    for i in tokens:
        if i not in stop_words:
            tokens_right.append(i)
    return tokens_right


def calculate_frequencies(tokens: list) -> dict or None:
    """
    Calculates frequencies of given tokens
    :param tokens: a list of tokens
    :return: a dictionary with frequencies
    """
    dictionary = {}
    if type(tokens) != list or None in tokens:
        return None
    for i in tokens:
        if type(i) != str:
            return None
        if i not in dictionary:
            dictionary[i] = 1
        else:
            dictionary[i] = dictionary[i]+1
    return dictionary


def get_top_n_words(freq_dict: dict, top_n: int) -> list or None:
    """
    Returns the most common words
    :param freq_dict: a dictionary with frequencies
    :param top_n: a number of the most common words
    :return: a list of the most common words
    """
    if type(freq_dict) != dict:
        return None
    sorted_freq_list = sorted(freq_dict.values())
    sorted_dict_n = {}
    sorted_freq_list = sorted_freq_list[::-1]
    for i in sorted_freq_list:
        for k in freq_dict.keys():
            if freq_dict[k] == i:
                sorted_dict_n[k] = freq_dict[k]
    top_n_list = sorted_dict_n.keys()
    top_n_list = list(top_n_list)
    top_n_list = top_n_list[:top_n]
    return top_n_list


def create_language_profile(language: str, text: str, stop_words: list) -> dict or None:
    """
    Creates a language profile
    :param language: a language
    :param text: a text
    :param stop_words: a list of stop words
    :return: a dictionary with three keys – name, freq, n_words
    """
    if type(language) != str or type(text) != str or type(stop_words) != list:
        return None
    tokens = tokenize(text)
    tokens = remove_stop_words(tokens, stop_words)
    freq_dict = calculate_frequencies(tokens)
    language_profile = {'name': language, 'freq': freq_dict, 'n_words': len(freq_dict)}
    return language_profile


def compare_profiles(unknown_profile: dict, profile_to_compare: dict, top_n: int) -> float or None:
    """
    Compares profiles and calculates the distance using top n words
    :param unknown_profile: a dictionary
    :param profile_to_compare: a dictionary
    :param top_n: a number of the most common words
    :return: the distance
    """
    if type(unknown_profile) != dict or type(profile_to_compare) != dict or type(top_n) != int:
        return None
    unknown_profile_top_n = get_top_n_words(unknown_profile['freq'], top_n)
    profile_to_compare_top_n = get_top_n_words(profile_to_compare['freq'], top_n)
    common_top_n = 0
    for i in unknown_profile_top_n:
        if i in profile_to_compare_top_n:
            common_top_n = common_top_n + 1
    proportion = common_top_n/len(profile_to_compare_top_n)
    proportion = round(proportion, 2)
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
    if type(unknown_profile) != dict or type(profile_1) != dict or type(profile_2) != dict or type(top_n) != int:
        return None
    profile_1_tokens = compare_profiles(unknown_profile, profile_1, top_n)
    profile_2_tokens = compare_profiles(unknown_profile, profile_2, top_n)
    name_1 = profile_1['name']
    name_2 = profile_2['name']
    if profile_1_tokens > profile_2_tokens:
        return name_1
    elif profile_2_tokens > profile_1_tokens:
        return name_2
    elif profile_1_tokens == profile_2_tokens:
        names = [name_1, name_2]
        names = sorted(names)
        return names


def compare_profiles_advanced(unknown_profile: dict, profile_to_compare: dict, top_n: int) -> list or None:
    """
    Compares profiles and calculates some advanced parameters
    :param unknown_profile: a dictionary
    :param profile_to_compare: a dictionary
    :param top_n: a number of the most common words
    :return: a dictionary with 7 keys – name, score, common, sorted_common, max_length_word,
    min_length_word, average_token_length
    """
    if type(unknown_profile) != dict or type(profile_to_compare) != dict or type(top_n) != int:
        return None
    unknown_top_n = get_top_n_words(unknown_profile['freq'], top_n)
    compare_top_n = get_top_n_words(profile_to_compare['freq'], top_n)
    common_top_n = []
    for i in compare_top_n:
        if i in unknown_top_n:
            common_top_n.append(i)  # common
    score = len(common_top_n)/top_n  # score
    all_words_compare = list(profile_to_compare['freq'].keys())
    all_words_unknown = list(unknown_profile['freq'].keys())
    max_length_word = max(all_words_compare, key=len)  # max
    min_length_word = min(all_words_compare, key=len)  # min
    sum_of_letters = 0
    for x in range(len(all_words_compare)):
        sum_of_letters += len(all_words_compare[x])
    average_token_length = sum_of_letters / len(all_words_compare)
    sorted_common = sorted(common_top_n)
    report = {'name': profile_to_compare['name'],
              'common': common_top_n,
              'score': score,
              'max_length_word': max_length_word,
              'min_length_word': min_length_word,
              'average_token_length': average_token_length,
              'sorted_common': sorted_common}
    return report


def detect_language_advanced(unknown_profile: dict, profiles: list, languages: list, top_n: int) -> str or None:
    """
    Detects the language of an unknown profile within the list of possible languages
    :param unknown_profile: a dictionary
    :param profiles: a list of dictionaries
    :param languages: a list of possible languages
    :param top_n: a number of the most common words
    :return: a language
    """


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
