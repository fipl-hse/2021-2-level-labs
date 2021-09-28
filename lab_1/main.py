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
    if isinstance(text, str) is False:
        return None
    text = text.lower()
    punctuation = '''`~!§№@º#$%^&|*()_-=+[{]};:'"\\,<.>/?1234567890'''
    for char in text:
        if char in punctuation:
            text = text.replace(char, '')
    text = text.split()
    text = list(filter(None, text))
    return text


def remove_stop_words(tokens: list, stop_words: list) -> list or None:
    """
    Removes stop words
    :rtype: object
    :param tokens: a list of tokens
    :param stop_words: a list of stop words
    :return: a list of tokens without stop words
    """
    if isinstance(tokens, list) is False or isinstance(stop_words, list) is False or None in tokens:
        return None
    tokens_normalno = []
    for item in tokens:
        if item not in stop_words:
            tokens_normalno.append(item)
    return tokens_normalno


def calculate_frequencies(tokens: list) -> dict or None:
    """
    Calculates frequencies of given tokens
    :param tokens: a list of tokens
    :return: a dictionary with frequencies
    """
    if isinstance(tokens, list) is False or None in tokens:
        return None
    freq_dict = {}
    for char in tokens:
        if isinstance(char, str) is False:
            return None
        freq_dict[char] = tokens.count(char)
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
    for value in freq_list:
        for key in freq_dict.keys():
            if freq_dict[key] == value:
                top_dict[key] = freq_dict[key]
    top_list = list(top_dict.keys())
    top_list = top_list[:top_n]
    return top_list


def create_language_profile(language: str, text: str,
                            stop_words: list) -> dict or None:
    """
    Creates a language profile
    :param language: a language
    :param text: a text
    :param stop_words: a list of stop words
    :return: a dictionary with three keys – name, freq, n_words
    """
    if isinstance(language, str) is False or isinstance(text, str) is False:
        return None
    if isinstance(stop_words, list) is False:
        return None
    tokens = tokenize(text)
    tokens = remove_stop_words(tokens, stop_words)
    freq_dict = calculate_frequencies(tokens)
    language_profile = {'name': language, 'freq': freq_dict, 'n_words': len(freq_dict)}
    return language_profile


def compare_profiles(unknown_profile: dict, profile_to_compare: dict,
                     top_n: int) -> float or None:
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
    for item in unknown_profile_top:
        if item in profile_to_compare_top:
            count += 1
    proportion = round(count/top_n, 2)
    return proportion


def detect_language(unknown_profile: dict, profile_1: dict, profile_2: dict,
                    top_n: int) -> str or None:
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
        return None
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


def compare_profiles_advanced(unknown_profile: dict, profile_to_compare: dict,
                              top_n: int) -> list or None:
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
    for item in profile_to_compare_top:
        if item in unknown_profile_top:
            common.append(item)
    score = len(common)/top_n
    general = list(profile_to_compare['freq'].keys())
    max_len = general[0]
    min_len = general[0]
    average = 0
    for item in general:
        average += len(item)
        if len(item) > len(max_len):
            max_len = item
        elif len(item) < len(min_len):
            min_len = item
    average_token_length = average/len(general)
    compared_profile = {'name': profile_to_compare['name'],
                        'common': common,
                        'score': score,
                        'max_length_word': max_len,
                        'min_length_word': min_len,
                        'average_token_length': average_token_length,
                        'sorted_common': sorted(common)}
    return compared_profile


def detect_language_advanced(unknown_profile: dict, profiles: list, languages: list,
                             top_n: int) -> str or None:
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
    bibs = []
    for item in profiles:
        if not languages or item['name'] in languages:
            profile_comp = compare_profiles_advanced(unknown_profile, item, top_n)
            bibs.append(profile_comp)
    bibs = sorted(bibs, reverse=True, key=lambda x: x['score'])
    if len(bibs) == 0:
        return None
    if len(bibs) > 1:
        if bibs[0]['score'] == bibs[1]['score']:
            max_scores = []
            for item in bibs:
                if item['score'] == bibs[0]['score']:
                    max_scores.append(item)
            bibs = sorted(max_scores, reverse=True, key=lambda x: x['score'])
    result = bibs[0]['name']
    return result
