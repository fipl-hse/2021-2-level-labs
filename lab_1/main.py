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
    import re
    if isinstance(text, str) is False:
        return None
    text = text.split()
    punctuation = '[`|~|!|§|№|@|#|$|%|^|&|*|(|)|_|\-|=|+|\[|\{|\]|\}|;|:|\'|"|,|<|.|>|/|?|1|2|3|4|5|6|7|8|9|0]'
    for i in range(len(text)):
        text[i] = text[i].lower()
        text[i] = re.sub(punctuation, '', text[i])
    text = list(filter(None, text))
    return text


def remove_stop_words(text: list, stop_words: list):
    """
    Removes stop words
    :rtype: object
    :param tokens: a list of tokens
    :param stop_words: a list of stop words
    :return: a list of tokens without stop words
    """
    if isinstance(text, list) is False or isinstance(stop_words, list) is False or None in text:
        return None
    lent = len(text)
    i = 0
    for count in range(lent):
        if text[i] in stop_words:
            text.remove(text[i])
        else:
            i += 1
    return text


def calculate_frequencies(text: list) -> dict or None:
    """
    Calculates frequencies of given tokens
    :param tokens: a list of tokens
    :return: a dictionary with frequencies
    """
    if isinstance(text, list) is False or None in text:
        return None
    freq_dict = {}
    for char in text:
        if type(char) != str:
            return None
        freq_dict[char] = text.count(char)
    return freq_dict


def get_top_n_words(freq_dict: dict, top_n: int) -> list or None:
    """
    Returns the most common words
    :param freq_dict: a dictionary with frequencies
    :param top_n: a number of the most common words
    :return: a list of the most common words
    """
    if isinstance(freq_dict, dict) is False or isinstance(top_n, int) is False or None in freq_dict:
        return None
    top_dict = {}
    freq_list = sorted(freq_dict.values())
    freq_list = freq_list[::-1]
    for i in freq_list:
        for j in freq_dict.keys():
            if freq_dict[j] == i:
                top_dict[j] = freq_dict[j]
    top_list = list(top_dict.keys())
    top_list = top_list[:top_n]
    return top_list


def create_language_profile(language: str, text: str, stop_words: list) -> dict or None:
    """
    Creates a language profile
    :param language: a language
    :param text: a text
    :param stop_words: a list of stop words
    :return: a dictionary with three keys – name, freq, n_words
    """
    if isinstance(language, str) is False or isinstance(text, str) is False or isinstance(stop_words, list) is False:
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
    if isinstance(unknown_profile, dict) is False or isinstance(profile_to_compare, dict) is False:
        return None
    if isinstance(top_n, int) is False:
        return None
    unknown_profile_top = get_top_n_words(unknown_profile['freq'], top_n)
    profile_to_compare_top = get_top_n_words(profile_to_compare['freq'], top_n)
    count = 0
    for i in unknown_profile_top:
        if i in profile_to_compare_top:
            count += 1
    proportion = round(count/top_n, 2)
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
    if isinstance(unknown_profile, dict) is False or isinstance(profile_1, dict) is False:
        return None
    if isinstance(profile_2, dict) is False or isinstance(top_n, int) is False:
        return  None
    proportion_1 = compare_profiles(unknown_profile, profile_1, top_n)
    proportion_2 = compare_profiles(unknown_profile, profile_2, top_n)
    if proportion_2 > proportion_1:
        result = profile_2['name']
    elif proportion_1 > proportion_2:
        result = profile_1['name']
    else:
        result = sorted([profile_1['name'], profile_2['name']])
        result = result[:1]
    return result


def compare_profiles_advanced(unknown_profile: dict, profile_to_compare: dict, top_n: int) -> list or None:
    """
    Compares profiles and calculates some advanced parameters
    :param unknown_profile: a dictionary
    :param profile_to_compare: a dictionary
    :param top_n: a number of the most common words
    :return: a dictionary with 7 keys – name, score, common, sorted_common, max_length_word,
    min_length_word, average_token_length
    """
    if isinstance(unknown_profile, dict) is False or isinstance(profile_to_compare, dict) is False:
        return None
    if isinstance(top_n, int) is False:
        return None
    unknown_profile_top = get_top_n_words(unknown_profile['freq'], top_n)
    profile_to_compare_top = get_top_n_words(profile_to_compare['freq'], top_n)
    common = []
    for i in profile_to_compare_top:
        if i in unknown_profile_top:
            common.append(i)
    score = len(common)/top_n
    general = list(profile_to_compare['freq'].keys())
    max_len = 0
    min_len = 0
    for i in range(len(general)):
        if len(general[i]) > len(general[max_len]):
            max_len = i
        elif len(general[i]) < len(general[min_len]):
            min_len = i
    av = 0
    for i in general:
        av += len(i)
    average_token_length = av/len(general)
    compared_profile = {'name': profile_to_compare['name'],
                        'common': common,
                        'score': score,
                        'max_length_word': general[max_len],
                        'min_length_word': general[min_len],
                        'average_token_length': average_token_length,
                        'sorted_common': sorted(common)}
    return compared_profile


def detect_language_advanced(unknown_profile: dict, profiles: list, languages: list, top_n: int) -> str or None:
    """
    Detects the language of an unknown profile within the list of possible languages
    :param unknown_profile: a dictionary
    :param profiles: a list of dictionaries
    :param languages: a list of possible languages
    :param top_n: a number of the most common words
    :return: a language
    """
    if isinstance(unknown_profile, dict) is False or isinstance(profiles, list) is False:
        return None
    if isinstance(languages, list) is False or isinstance(top_n, int) is False:
        return None
    langvaga = {}
    if languages is []:
        for i in profiles:
            j = compare_profiles_advanced(unknown_profile, i, top_n)
            langvaga[j['name']] = j['score']
        maximum = max(langvaga, key=langvaga.get)
        for i in langvaga.keys():
            if langvaga[i] == maximum:
                result = langvaga[i]
    else:
        for i in profiles:
            if i['name'] in languages:
                j = compare_profiles_advanced(unknown_profile, i, top_n)
                langvaga[j['name']] = j['score']
            maximum = max(langvaga, key=langvaga.get)
            for i in langvaga.keys():
                if langvaga[i] == maximum:
                    result = i
    return result


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
