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
    if not isinstance(text, str):
        return None
    skip_signs = ['`', '~', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '-', '+',
                        '=', '{', '[', ']', '}', '|', ':', ';', '"', "'", '<', ',', '>',
                        '.', '?', '/']
    text = text.lower()
    for symbol in skip_signs:
        text = text.replace(symbol, '')
    tokens = text.split()
    return tokens


def remove_stop_words(tokens: list, stop_words: list) -> list or None:
    """
    Removes stop words
    :param tokens: a list of tokens
    :param stop_words: a list of stop words
    :return: a list of tokens without stop words
    """
    if not isinstance(tokens, list) or not isinstance(stop_words, list):
        return None
    tokens_without_stop_words = []
    for word in tokens:
        if word not in stop_words:
            tokens_without_stop_words.append(word)
    return tokens_without_stop_words


def calculate_frequencies(tokens: list) -> dict or None:
    """
    Calculates frequencies of given tokens
    :param tokens: a list of tokens
    :return: a dictionary with frequencies
    """
    if not isinstance(tokens, list):
        return None
    freq_dict = {}
    for token in tokens:
        if isinstance(token, str):
            if token not in freq_dict:
                freq_dict[token] = 1
            else:
                freq_dict[token] += 1
        else:
            return None
    return freq_dict


def get_top_n_words(freq_dict: dict, top_n: int) -> list or None:
    """
    Returns the most common words
    :param freq_dict: a dictionary with frequencies
    :param top_n: a number of the most common words
    :return: a list of the most common words
    """
    if not isinstance(freq_dict, dict) or not isinstance(top_n, int):
        return None
    top_n_words = sorted(freq_dict, key=freq_dict.get, reverse=True)
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
    if not isinstance(language, str)\
            or not isinstance(text, str)\
            or not isinstance(stop_words, list):
        return None
    tokens = tokenize(text)
    tokens = remove_stop_words(tokens, stop_words)
    freq_dict = calculate_frequencies(tokens)
    n_words = len(freq_dict.keys())
    return {"name": language, "freq": freq_dict, "n_words": n_words}


def compare_profiles(unknown_profile: dict, profile_to_compare: dict, top_n: int) -> float or None:
    """
    Compares profiles and calculates the distance using top n words
    :param unknown_profile: a dictionary
    :param profile_to_compare: a dictionary
    :param top_n: a number of the most common words
    :return: the distance
    """
    if (not isinstance(unknown_profile, dict)
            or not isinstance(profile_to_compare, dict)
            or not isinstance(top_n, int)):
        return None
    profile_to_compare_tokens = get_top_n_words(profile_to_compare['freq'], top_n)
    unknown_profile_tokens = get_top_n_words(unknown_profile['freq'], top_n)
    common_tokens = 0
    for i in unknown_profile_tokens:
        if i in profile_to_compare_tokens:
            common_tokens += 1
    common_freq_words = common_tokens / len(unknown_profile_tokens)
    common_freq_words = round(common_freq_words, 2)
    return common_freq_words


def detect_language(unknown_profile: dict,
                    profile_1: dict,
                    profile_2: dict, top_n: int) -> str or None:
    """
    Detects the language of an unknown profile
    :param unknown_profile: a dictionary
    :param profile_1: a dictionary
    :param profile_2: a dictionary
    :param top_n: a number of the most common words
    :return: a language
    """
    if (not isinstance(unknown_profile, dict)
            or not isinstance(profile_1, dict)
            or not isinstance(profile_2, dict)
            or not isinstance(top_n, int)):
        return None
    profile_1_words = compare_profiles(unknown_profile, profile_1, top_n)
    profile_2_words = compare_profiles(unknown_profile, profile_2, top_n)
    name1 = profile_1['name']
    name2 = profile_2['name']
    if profile_1_words > profile_2_words:
        return_name = name1
    elif profile_2_words > profile_1_words:
        return_name = name2
    else:
        names = [name1, name2]
        names.sort()
        return_name = names[0]
        return return_name


def compare_profiles_advanced(unknown_profile: dict,
                              profile_to_compare: dict,
                              top_n: int) -> dict or None:
    """
    Compares profiles and calculates some advanced parameters
    :param unknown_profile: a dictionary
    :param profile_to_compare: a dictionary
    :param top_n: a number of the most common words
    :return: a dictionary with 7 keys – name, score, common, sorted_common, max_length_word,
    min_length_word, average_token_length
    """
    if (not isinstance(unknown_profile, dict)
            or not isinstance(profile_to_compare, dict)
            or not isinstance(top_n, int)):
        return None
    shared_tokens = []
    for comp_top_word in get_top_n_words(profile_to_compare['freq'], top_n):
        if comp_top_word in get_top_n_words(unknown_profile['freq'], top_n):
            shared_tokens.append(comp_top_word)
    score = compare_profiles(unknown_profile, profile_to_compare, top_n)
    words = list(profile_to_compare['freq'].keys())
    max_length_word = 'a'
    for word_for_max in words:
        if len(word_for_max) > len(max_length_word):
            max_length_word = word_for_max
    min_length_word = 100 * 'a'
    for word_for_min in words:
        if len(word_for_min) < len(min_length_word):
            min_length_word = word_for_min
    sum_letters = 0
    for word_for_sum in words:
        sum_letters += len(word_for_sum)
    sorted_common = shared_tokens.copy()
    sorted_common.sort()
    report = {'name': profile_to_compare['name'],
              'common': shared_tokens,
              'score': score,
              'max_length_word': max_length_word,
              'min_length_word': min_length_word,
              'average_token_length': sum_letters / len(words),
              'sorted_common': sorted_common}
    return report


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
    if (not isinstance(unknown_profile, dict)
            or not isinstance(profiles, list)
            or not isinstance(languages, list)
            or not isinstance(top_n, int)):
        return None
    list_of_languages = []
    for profile in profiles:
        if profile['name'] in languages or languages == []:
            compared_profile = compare_profiles_advanced(unknown_profile, profile, top_n)
            list_of_languages.append(compared_profile)
    list_of_languages = sorted(list_of_languages, reverse=True, key=lambda x: x['score'])
    if not list_of_languages:
        return None
    if len(list_of_languages) > 1:
        if list_of_languages[0]['score'] == list_of_languages[1]['score']:
            equal_scores = []
            for i in list_of_languages:
                if i['score'] == list_of_languages[0]:
                    equal_scores.append(i)
            list_of_languages = sorted(equal_scores, reverse=True, key=lambda x: x['score'])
    return list_of_languages[0]['name']


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
