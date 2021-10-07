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
    text = text.lower()
    gaps = """1234567890-=!@#$%^&*()_+{};:[]'"№,./<>?\|~`"""
    for i in text:
        if i in gaps:
            text = text.replace(i, '')
    tokens = text.split()
    return tokens


def remove_stop_words(tokens: list, stop_words: list):
    """
    Removes stop words
    :param tokens: a list of tokens
    :param stop_words: a list of stop words
    :return: a list of tokens without stop words
    """
    if not isinstance(tokens, list) or not isinstance(stop_words, list):
        return None
    tokens_list = []
    for i in tokens:
        if isinstance(i, str) and i not in stop_words:
            tokens_list.append(i)
    return tokens_list


def calculate_frequencies(tokens: list) -> dict or None:
    """
    Calculates frequencies of given tokens
    :param tokens: a list of tokens
    :return: a dictionary with frequencies
    """
    if not isinstance(tokens, list):
        return None
    for i in tokens:
        if not isinstance(i, str):
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
    if not isinstance(freq_dict, dict) or not isinstance(top_n, int):
        return None
    top_n_words = []
    '''freq_keys = [key for key in freq_dict]'''
    top_n_words = sorted(freq_dict, key=freq_dict.get, reverse=True)[:top_n]
    return top_n_words


def create_language_profile(language: str, text: str, stop_words: list) -> dict or None:
    """
    Creates a language profile
    :param language: a language
    :param text: a text
    :param stop_words: a list of stop words
    :return: a dictionary with three keys – name, freq, n_words
    """
    if not isinstance(language, str) or not isinstance(text, str):
        return None
    if not isinstance(stop_words, list):
        return None
    tokens = tokenize(text)
    tokens = remove_stop_words(tokens, stop_words)
    freq_dic = calculate_frequencies(tokens)
    language_profile = {'name': language, 'freq': freq_dic, 'n_words': len(freq_dic)}
    return language_profile


def compare_profiles(unknown_profile: dict, profile_to_compare: dict, top_n: int) -> float or None:
    """
    Compares profiles and calculates the distance using top n words
    :param unknown_profile: a dictionary
    :param profile_to_compare: a dictionary
    :param top_n: a number of the most common words
    :return: the distance
    """
    if not isinstance(unknown_profile, dict) or not isinstance(profile_to_compare, dict) or \
            not isinstance(top_n, int):
        return None
    top_unknown_profile = get_top_n_words(unknown_profile['freq'], top_n)
    top_profile_to_compare = get_top_n_words(profile_to_compare['freq'], top_n)
    common_words = []
    for profile_word in top_profile_to_compare:
        if profile_word in top_unknown_profile:
            common_words.append(profile_word)
    distance = round(len(common_words) / len(top_unknown_profile), 2)
    return distance


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
    compare_with_1 = compare_profiles(unknown_profile, profile_1, top_n)
    compare_with_2 = compare_profiles(unknown_profile, profile_2, top_n)
    name_1 = profile_1['name']
    name_2 = profile_2['name']
    if compare_with_1 > compare_with_2:
        return name_1
    if compare_with_2 > compare_with_1:
        return name_2

def compare_profiles_advanced(unknown_profile: dict, profile_to_compare: dict, top_n: int) -> list or None:
    """
    Compares profiles and calculates some advanced parameters
    :param unknown_profile: a dictionary
    :param profile_to_compare: a dictionary
    :param top_n: a number of the most common words
    :return: a dictionary with 7 keys – name, score, common, sorted_common, max_length_word,
    min_length_word, average_token_length
    """
    if not isinstance(unknown_profile, dict) or not isinstance(profile_to_compare, dict):
        return None
    if not isinstance(top_n, int):
        return None

    top_unknown = get_top_n_words(unknown_profile["freq"], top_n)
    top_compare = get_top_n_words(profile_to_compare["freq"], top_n)

    cross = 0
    common = []
    for token in top_compare:
        if token in top_unknown:
            cross += 1
            common.append(token)

    tokens_length = 0
    max_l = len(list(profile_to_compare["freq"].keys())[0])
    min_l = max_l
    for word in profile_to_compare["freq"]:
        if len(word) >= max_l:
            max_w = word
        if len(word) <= min_l:
            min_w = word
        tokens_length += len(word)

    report = {"name": profile_to_compare["name"],
             "score": round(cross / top_n, 2),
             "common": common,
             "sorted_common": sorted(common),
             "min_length_word": min_w,
             "max_length_word": max_w,
             "average_token_length": tokens_length / len(profile_to_compare["freq"])}
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
    if not isinstance(unknown_profile, dict) or not isinstance(profiles, list) \
            or not isinstance(languages, list) or not \
            isinstance(top_n, int):
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